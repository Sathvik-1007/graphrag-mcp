import { hashTypeToColor } from "./GraphView";
import type { SearchResponse } from "../types/graph";

interface SearchBarProps {
  query: string;
  results: SearchResponse | null;
  loading: boolean;
  onSearch: (q: string) => void;
  onClear: () => void;
  onSelectResult: (name: string) => void;
}

export function SearchBar({
  query,
  results,
  loading,
  onSearch,
  onClear,
  onSelectResult,
}: SearchBarProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      onClear();
    } else if (e.key === "Enter" && results?.results.length) {
      const first = results.results[0];
      if (first) {
        onSelectResult(first.name);
        onClear();
      }
    }
  };

  return (
    <div className="relative">
      <input
        type="text"
        value={query}
        onChange={(e) => onSearch(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search entities..."
        className="w-full px-3 py-2 text-sm rounded-md border border-[var(--color-border)] bg-[var(--color-bg)] text-[var(--color-text)] placeholder:text-[var(--color-text-secondary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-accent)]"
      />
      {loading && (
        <div className="absolute right-3 top-2.5 text-xs text-[var(--color-text-secondary)]">
          ...
        </div>
      )}
      {results && results.results.length > 0 && (
        <div className="absolute z-10 top-full left-0 right-0 mt-1 max-h-64 overflow-auto rounded-md border border-[var(--color-border)] bg-[var(--color-surface)] shadow-lg">
          {results.results.map((r) => (
            <button
              key={r.name}
              onClick={() => {
                onSelectResult(r.name);
                onClear();
              }}
              className="w-full text-left px-3 py-2 hover:bg-[var(--color-border)] transition-colors cursor-pointer border-b border-[var(--color-border)] last:border-b-0"
            >
              <div className="flex items-center gap-2">
                <span className="font-medium text-sm">{r.name}</span>
                <span
                  className="text-xs px-1.5 py-0.5 rounded text-white"
                  style={{ backgroundColor: hashTypeToColor(r.entity_type) }}
                >
                  {r.entity_type}
                </span>
                <span className="ml-auto text-xs text-[var(--color-text-secondary)]">
                  {r.score.toFixed(2)}
                </span>
              </div>
              {r.matched_observations.length > 0 && (
                <p className="text-xs text-[var(--color-text-secondary)] mt-1 truncate">
                  {r.matched_observations[0]}
                </p>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
