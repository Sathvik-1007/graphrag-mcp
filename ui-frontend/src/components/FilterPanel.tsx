import { hashTypeToColor } from "./GraphView";

interface FilterPanelProps {
  entityTypes: Array<{ type: string; count: number }>;
  visibleTypes: Set<string>;
  showEdgeLabels: boolean;
  onToggleType: (type: string) => void;
  onSelectAll: () => void;
  onClearAll: () => void;
  onToggleEdgeLabels: () => void;
}

export function FilterPanel({
  entityTypes,
  visibleTypes,
  showEdgeLabels,
  onToggleType,
  onSelectAll,
  onClearAll,
  onToggleEdgeLabels,
}: FilterPanelProps) {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-sm">Entity Types</h3>
        <div className="flex gap-2">
          <button
            onClick={onSelectAll}
            className="text-xs text-[var(--color-accent)] hover:underline cursor-pointer"
          >
            All
          </button>
          <button
            onClick={onClearAll}
            className="text-xs text-[var(--color-accent)] hover:underline cursor-pointer"
          >
            None
          </button>
        </div>
      </div>
      <div className="flex flex-col gap-1">
        {entityTypes.map(({ type, count }) => (
          <label
            key={type}
            className="flex items-center gap-2 text-sm cursor-pointer py-0.5"
          >
            <input
              type="checkbox"
              checked={visibleTypes.has(type)}
              onChange={() => onToggleType(type)}
              className="accent-[var(--color-accent)]"
            />
            <span
              className="inline-block w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: hashTypeToColor(type) }}
            />
            <span className="truncate">{type}</span>
            <span className="text-[var(--color-text-secondary)] ml-auto text-xs">
              {count}
            </span>
          </label>
        ))}
      </div>
      <hr className="border-[var(--color-border)]" />
      <label className="flex items-center gap-2 text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={showEdgeLabels}
          onChange={onToggleEdgeLabels}
          className="accent-[var(--color-accent)]"
        />
        Show edge labels
      </label>
    </div>
  );
}
