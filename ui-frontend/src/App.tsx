import { useCallback } from "react";
import { useGraph } from "./hooks/useGraph";
import { useSearch } from "./hooks/useSearch";
import { useTheme } from "./hooks/useTheme";
import { StatsBar } from "./components/StatsBar";
import { ThemeToggle } from "./components/ThemeToggle";
import { GraphView } from "./components/GraphView";
import { SearchBar } from "./components/SearchBar";
import { EntityPanel } from "./components/EntityPanel";
import { FilterPanel } from "./components/FilterPanel";

export default function App() {
  const {
    state,
    selectEntity,
    clearEntity,
    toggleEntityType,
    selectAllTypes,
    clearAllTypes,
    toggleEdgeLabels,
    entityTypes,
  } = useGraph();

  const { query, results, loading: searchLoading, search, clearSearch } = useSearch();
  const { theme, toggleTheme } = useTheme();

  const handleNodeClick = useCallback(
    (name: string) => {
      void selectEntity(name);
    },
    [selectEntity]
  );

  const handleSearchSelect = useCallback(
    (name: string) => {
      void selectEntity(name);
    },
    [selectEntity]
  );

  if (state.loading) {
    return (
      <div className="flex items-center justify-center h-screen text-[var(--color-text-secondary)]">
        <div className="text-center">
          <div className="text-2xl mb-2">Loading graph...</div>
          <div className="text-sm">Connecting to GraphRAG API</div>
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div className="flex items-center justify-center h-screen text-red-400">
        <div className="text-center max-w-md">
          <div className="text-xl mb-2">Connection Error</div>
          <div className="text-sm mb-4">{state.error}</div>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Make sure the GraphRAG API server is running on port 8080
          </p>
        </div>
      </div>
    );
  }

  return (
    <>
      <StatsBar stats={state.stats}>
        <ThemeToggle theme={theme} onToggle={toggleTheme} />
      </StatsBar>
      <div className="flex flex-1 overflow-hidden">
        {/* Graph area */}
        <div className="flex-1 min-w-0">
          <GraphView
            data={state.graph}
            visibleTypes={state.visibleEntityTypes}
            showEdgeLabels={state.showEdgeLabels}
            selectedNode={state.selectedEntity?.name ?? null}
            theme={theme}
            onNodeClick={handleNodeClick}
          />
        </div>

        {/* Sidebar */}
        <div className="w-80 flex-shrink-0 border-l border-[var(--color-border)] bg-[var(--color-surface)] flex flex-col overflow-hidden">
          {/* Search */}
          <div className="p-3 border-b border-[var(--color-border)]">
            <SearchBar
              query={query}
              results={results}
              loading={searchLoading}
              onSearch={search}
              onClear={clearSearch}
              onSelectResult={handleSearchSelect}
            />
          </div>

          {/* Entity detail or filters */}
          <div className="flex-1 overflow-auto p-3">
            {state.selectedEntity ? (
              <EntityPanel
                entity={state.selectedEntity}
                onClose={clearEntity}
                onNavigate={handleNodeClick}
              />
            ) : (
              <FilterPanel
                entityTypes={entityTypes}
                visibleTypes={state.visibleEntityTypes}
                showEdgeLabels={state.showEdgeLabels}
                onToggleType={toggleEntityType}
                onSelectAll={selectAllTypes}
                onClearAll={clearAllTypes}
                onToggleEdgeLabels={toggleEdgeLabels}
              />
            )}
          </div>
        </div>
      </div>
    </>
  );
}
