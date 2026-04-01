import type { StatsResponse } from "../types/graph";

interface StatsBarProps {
  stats: StatsResponse | null;
  children?: React.ReactNode;
}

export function StatsBar({ stats, children }: StatsBarProps) {
  return (
    <div className="flex items-center justify-between px-4 py-2 border-b border-[var(--color-border)] bg-[var(--color-surface)]">
      <div className="flex items-center gap-6 text-sm">
        <span className="font-semibold text-[var(--color-accent)]">
          GraphRAG Explorer
        </span>
        {stats && (
          <>
            <span>
              Entities:{" "}
              <strong>{stats.entity_count.toLocaleString()}</strong>
            </span>
            <span>
              Relationships:{" "}
              <strong>{stats.relationship_count.toLocaleString()}</strong>
            </span>
            <span>
              Observations:{" "}
              <strong>{stats.observation_count.toLocaleString()}</strong>
            </span>
          </>
        )}
      </div>
      <div>{children}</div>
    </div>
  );
}
