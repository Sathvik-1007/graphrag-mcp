---
name: graph-mem
description: >-
  Persistent knowledge graph memory for AI agents via MCP. Use when agents need
  to remember facts across sessions, track decisions, build knowledge graphs,
  manage project context, or maintain structured long-term memory. Triggers on:
  remember this, store fact, what do we know about, search memory, knowledge graph,
  graph memory, add entity, find connections, cross-session memory, recall,
  semantic search, entity relationships, persistent memory, structured recall.
license: MIT
metadata:
  author: Sathvik
  version: 2.1.0
  created: 2025-03-15
  last_reviewed: 2026-04-04
  review_interval_days: 30
---

# graph-mem — Persistent Knowledge Graph Memory

You have a persistent, structured knowledge graph via MCP. It survives across
sessions. Runs entirely locally — SQLite with hybrid semantic + full-text search.
No API keys required.

## The Core Contract

**You extract and store knowledge from every conversation turn.** Not when asked.
Not when it seems important. Every turn. The graph's value comes from completeness.

After responding to the user, you shift into extraction mode: identify what was
discussed, check what already exists, store what's new, connect what's related,
and verify nothing was missed. Details in `workflows.md`.

## The Three Primitives

| Primitive | What It Is | Store With |
|-----------|-----------|------------|
| **Entity** | A named node — a person, system, concept, decision, anything worth tracking | `add_entities` |
| **Observation** | An atomic fact attached to an entity — one sentence, one fact | `add_observations` |
| **Relationship** | A typed, directional edge between two entities | `add_relationships` |

Entities give you nodes to search for. Observations give you facts to recall.
Relationships give you structure to traverse. All three matter.

## MCP Tools

### Creating and Updating

| Tool | What It Does |
|------|-------------|
| `add_entities` | Create entities with name, type, description, and initial observations |
| `add_relationships` | Create directed edges between entities (source → type → target) |
| `add_observations` | Attach new facts to an existing entity |
| `update_entity` | Change an entity's description, type, or properties |
| `update_relationship` | Modify an edge's weight, type, or properties |
| `update_observation` | Edit observation text (re-embeds automatically) |
| `delete_entities` | Remove entities — cascades to their observations and relationships |
| `delete_relationships` | Remove edges between entities |
| `delete_observations` | Remove specific observations by ID |
| `merge_entities` | Combine duplicates — source is absorbed into target |

### Searching and Navigating

| Tool | When to Reach For It |
|------|---------------------|
| `search_nodes` | You have a concept and want to find matching entities |
| `search_observations` | You need a specific fact buried in observation text |
| `get_entity` | You know the entity name and want its full context |
| `find_connections` | You want to explore what's connected to an entity (multi-hop) |
| `find_paths` | You need to understand how two entities relate |
| `get_subgraph` | You want the neighborhood around one or more seed entities |
| `read_graph` | You want a bird's-eye view — counts, types, most connected |
| `list_entities` | You want to browse entities with pagination |

### Multiple Graphs

| Tool | Purpose |
|------|---------|
| `list_graphs` | Show all graphs in .graphmem/ |
| `create_graph` | Create a new named graph |
| `switch_graph` | Change which graph is active |
| `delete_graph` | Remove a named graph |

## Session Lifecycle

**Starting a session** — warm up before doing work:

```
read_graph              → what's in the graph?
search_nodes("topic")   → what do we already know?
get_entity("Name")      → load full context for key entities
```

**During a session** — extract after every response (see `workflows.md`).

**Ending a session** — sweep for anything unstored, update stale descriptions,
verify with `read_graph`.

## MCP Configuration

```json
{
  "mcpServers": {
    "graphmem-mcp": {
      "command": "graph-mem",
      "args": ["server"]
    }
  }
}
```

Project-scoped: `"args": ["server", "--project-dir", "/path/to/project"]`
Named graph: `"args": ["server", "--graph", "my-project"]`

## Reference Files

| File | What's In It |
|------|-------------|
| `conventions.md` | Naming rules for entities, types, relationships, observations |
| `workflows.md` | The extraction pipeline — how to capture knowledge each turn |
| `best-practices.md` | Quality standards, common mistakes, and self-correction |
| `domains/` | Domain-specific entity types and relationship types |
