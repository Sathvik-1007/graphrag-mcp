import { hashTypeToColor } from "./GraphView";
import type { EntityResponse } from "../types/graph";

interface EntityPanelProps {
  entity: EntityResponse;
  onClose: () => void;
  onNavigate: (name: string) => void;
}

export function EntityPanel({ entity, onClose, onNavigate }: EntityPanelProps) {
  const outgoing = entity.relationships.filter((r) => r.direction === "outgoing");
  const incoming = entity.relationships.filter((r) => r.direction === "incoming");
  const sortedObs = [...entity.observations].sort((a, b) => {
    if (!a.created_at) return 1;
    if (!b.created_at) return -1;
    return b.created_at.localeCompare(a.created_at);
  });

  const propEntries = Object.entries(entity.properties).filter(
    ([, v]) => v !== null && v !== undefined && v !== ""
  );

  return (
    <div className="flex flex-col gap-4 overflow-auto">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-lg font-bold">{entity.name}</h2>
          <span
            className="inline-block text-xs px-2 py-0.5 rounded text-white mt-1"
            style={{ backgroundColor: hashTypeToColor(entity.entity_type) }}
          >
            {entity.entity_type}
          </span>
        </div>
        <button
          onClick={onClose}
          className="text-[var(--color-text-secondary)] hover:text-[var(--color-text)] text-lg leading-none cursor-pointer"
        >
          &times;
        </button>
      </div>

      {entity.description && (
        <p className="text-sm text-[var(--color-text-secondary)]">
          {entity.description}
        </p>
      )}

      {propEntries.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold uppercase text-[var(--color-text-secondary)] mb-1">
            Properties
          </h3>
          <table className="text-sm w-full">
            <tbody>
              {propEntries.map(([k, v]) => (
                <tr key={k} className="border-b border-[var(--color-border)]">
                  <td className="py-1 pr-2 font-medium">{k}</td>
                  <td className="py-1 text-[var(--color-text-secondary)]">
                    {String(v)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {sortedObs.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold uppercase text-[var(--color-text-secondary)] mb-1">
            Observations ({sortedObs.length})
          </h3>
          <ul className="flex flex-col gap-2">
            {sortedObs.map((obs, i) => (
              <li
                key={i}
                className="text-sm p-2 rounded bg-[var(--color-bg)] border border-[var(--color-border)]"
              >
                <p>{obs.content}</p>
                <div className="flex gap-2 mt-1 text-xs text-[var(--color-text-secondary)]">
                  {obs.source && <span>Source: {obs.source}</span>}
                  {obs.created_at && (
                    <span>{new Date(obs.created_at).toLocaleDateString()}</span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {(outgoing.length > 0 || incoming.length > 0) && (
        <div>
          <h3 className="text-xs font-semibold uppercase text-[var(--color-text-secondary)] mb-1">
            Relationships
          </h3>
          {outgoing.length > 0 && (
            <div className="mb-2">
              <p className="text-xs font-medium text-[var(--color-text-secondary)] mb-1">
                Outgoing ({outgoing.length})
              </p>
              {outgoing.map((r, i) => (
                <button
                  key={i}
                  onClick={() => onNavigate(r.target)}
                  className="w-full text-left text-sm px-2 py-1 rounded hover:bg-[var(--color-border)] transition-colors cursor-pointer flex items-center gap-1"
                >
                  <span className="text-[var(--color-accent)]">→</span>
                  <span className="text-[var(--color-text-secondary)]">
                    {r.relationship_type}
                  </span>
                  <span className="font-medium ml-1">{r.target}</span>
                </button>
              ))}
            </div>
          )}
          {incoming.length > 0 && (
            <div>
              <p className="text-xs font-medium text-[var(--color-text-secondary)] mb-1">
                Incoming ({incoming.length})
              </p>
              {incoming.map((r, i) => (
                <button
                  key={i}
                  onClick={() => onNavigate(r.source)}
                  className="w-full text-left text-sm px-2 py-1 rounded hover:bg-[var(--color-border)] transition-colors cursor-pointer flex items-center gap-1"
                >
                  <span className="text-[var(--color-accent)]">←</span>
                  <span className="text-[var(--color-text-secondary)]">
                    {r.relationship_type}
                  </span>
                  <span className="font-medium ml-1">{r.source}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
