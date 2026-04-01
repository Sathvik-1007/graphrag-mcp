import { useRef, useEffect, useCallback, useState } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import forceAtlas2 from "graphology-layout-forceatlas2";
import type { GraphResponse } from "../types/graph";

// ── Deterministic color from entity type ──

export function hashTypeToColor(type: string): string {
  let hash = 0;
  for (let i = 0; i < type.length; i++) {
    hash = type.charCodeAt(i) + ((hash << 5) - hash);
    hash = hash & hash;
  }
  const hue = ((hash % 360) + 360) % 360;
  return `hsl(${hue}, 70%, 50%)`;
}

// ── Graph building ──

function buildGraph(
  data: GraphResponse,
  visibleTypes: Set<string>,
): Graph {
  const graph = new Graph();

  // Calculate connection counts for node sizing
  const connectionCounts = new Map<string, number>();
  for (const rel of data.relationships) {
    connectionCounts.set(rel.source, (connectionCounts.get(rel.source) ?? 0) + 1);
    connectionCounts.set(rel.target, (connectionCounts.get(rel.target) ?? 0) + 1);
  }
  const maxConns = Math.max(1, ...connectionCounts.values());

  for (const entity of data.entities) {
    if (!visibleTypes.has(entity.entity_type)) continue;
    const conns = connectionCounts.get(entity.name) ?? 0;
    const size = 4 + (conns / maxConns) * 16;
    graph.addNode(entity.name, {
      label: entity.name,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size,
      color: hashTypeToColor(entity.entity_type),
      type: "circle",
      entityType: entity.entity_type,
    });
  }

  for (const rel of data.relationships) {
    if (!graph.hasNode(rel.source) || !graph.hasNode(rel.target)) continue;
    // Avoid duplicate edges
    if (graph.hasEdge(rel.source, rel.target)) continue;
    graph.addEdge(rel.source, rel.target, {
      label: rel.relationship_type,
      size: Math.max(1, rel.weight * 3),
      color: "var(--color-border)",
    });
  }

  // Apply ForceAtlas2 layout synchronously (good for <500 nodes)
  if (graph.order > 0) {
    forceAtlas2.assign(graph, {
      iterations: 100,
      settings: {
        gravity: 1,
        scalingRatio: 10,
        barnesHutOptimize: graph.order > 100,
        strongGravityMode: true,
      },
    });
  }

  return graph;
}

// ── Component ──

interface GraphViewProps {
  data: GraphResponse | null;
  visibleTypes: Set<string>;
  showEdgeLabels: boolean;
  selectedNode: string | null;
  theme: "light" | "dark";
  onNodeClick: (name: string) => void;
}

export function GraphView({
  data,
  visibleTypes,
  showEdgeLabels,
  selectedNode,
  theme,
  onNodeClick,
}: GraphViewProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const graphRef = useRef<Graph | null>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  // Build/rebuild sigma instance
  useEffect(() => {
    if (!containerRef.current || !data) return;

    // Cleanup previous instance
    if (sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }

    const graph = buildGraph(data, visibleTypes);
    graphRef.current = graph;

    const bgColor = theme === "dark" ? "#0f0f23" : "#f1f5f9";
    const labelColor = theme === "dark" ? "#e2e8f0" : "#0f172a";
    const edgeLabelColor = theme === "dark" ? "#94a3b8" : "#64748b";

    const renderer = new Sigma(graph, containerRef.current, {
      renderEdgeLabels: showEdgeLabels,
      defaultNodeColor: "#6366f1",
      defaultEdgeColor: theme === "dark" ? "#2d3561" : "#cbd5e1",
      labelColor: { color: labelColor },
      edgeLabelColor: { color: edgeLabelColor },
      labelRenderedSizeThreshold: 8,
      stagePadding: 40,
    });

    // Set background
    const canvases = containerRef.current.querySelectorAll("canvas");
    canvases.forEach((c) => {
      c.style.background = bgColor;
    });

    // Hover handler
    renderer.on("enterNode", ({ node }) => {
      setHoveredNode(node);
    });
    renderer.on("leaveNode", () => {
      setHoveredNode(null);
    });

    // Click handler
    renderer.on("clickNode", ({ node }) => {
      onNodeClick(node);
    });

    sigmaRef.current = renderer;

    return () => {
      renderer.kill();
      sigmaRef.current = null;
    };
  }, [data, visibleTypes, showEdgeLabels, theme, onNodeClick]);

  // Highlight selected node
  useEffect(() => {
    const sigma = sigmaRef.current;
    const graph = graphRef.current;
    if (!sigma || !graph) return;

    sigma.setSetting("nodeReducer", (node, attrs) => {
      if (selectedNode && node !== selectedNode) {
        const isNeighbor = graph.hasEdge(node, selectedNode) || graph.hasEdge(selectedNode, node);
        if (!isNeighbor) {
          return { ...attrs, color: "#666", label: "" };
        }
      }
      return attrs;
    });

    sigma.setSetting("edgeReducer", (edge, attrs) => {
      if (selectedNode) {
        const src = graph.source(edge);
        const tgt = graph.target(edge);
        if (src !== selectedNode && tgt !== selectedNode) {
          return { ...attrs, color: "#333", hidden: false };
        }
      }
      return attrs;
    });

    sigma.refresh();
  }, [selectedNode]);

  // Focus camera on selected node
  const focusNode = useCallback(
    (name: string) => {
      const sigma = sigmaRef.current;
      const graph = graphRef.current;
      if (!sigma || !graph || !graph.hasNode(name)) return;
      const attrs = graph.getNodeAttributes(name);
      sigma.getCamera().animate(
        { x: attrs.x as number, y: attrs.y as number, ratio: 0.3 },
        { duration: 500 }
      );
    },
    []
  );

  useEffect(() => {
    if (selectedNode) focusNode(selectedNode);
  }, [selectedNode, focusNode]);

  return (
    <div className="relative w-full h-full">
      <div ref={containerRef} className="w-full h-full" />
      {hoveredNode && (
        <div className="absolute top-3 left-3 px-3 py-1.5 text-sm rounded-md bg-[var(--color-surface)] border border-[var(--color-border)] shadow-md pointer-events-none">
          <strong>{hoveredNode}</strong>
          {data && (
            <span className="ml-2 text-[var(--color-text-secondary)]">
              {data.entities.find((e) => e.name === hoveredNode)?.entity_type}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
