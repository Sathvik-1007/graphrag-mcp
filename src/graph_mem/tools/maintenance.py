"""Maintenance tools — graph_health, compact_observations, suggest_connections."""

from __future__ import annotations

import contextlib
from typing import Any

from graph_mem.models import Observation
from graph_mem.utils import GraphMemError

from ._core import (
    _embed_observations,
    _error_response,
    _require_state,
    mcp,
)


@mcp.tool()
async def graph_health() -> dict[str, Any]:
    """Get maintenance-oriented health stats for the knowledge graph.

    Returns entity/relationship/observation counts, top observation hotspots
    (entities with the most observations), entities missing descriptions,
    entity type distribution (top 10), and suggested maintenance actions.

    Use this at session start or periodically to decide whether cleanup,
    compaction, or pruning is needed.
    """
    try:
        state = _require_state()
        storage = state.storage

        entity_count = await storage.count_entities()
        rel_count = await storage.count_relationships()
        obs_count = await storage.count_observations()
        type_dist = await storage.entity_type_distribution()

        # Cap type distribution to top 10
        sorted_types = sorted(type_dist.items(), key=lambda x: x[1], reverse=True)
        type_dist_capped = dict(sorted_types[:10])

        # Top 5 observation hotspots — entities with most observations
        hotspot_rows = await storage.fetch_all(
            """
            SELECT e.id, e.name, e.entity_type, COUNT(o.id) AS obs_count
            FROM entities e
            JOIN observations o ON o.entity_id = e.id
            GROUP BY e.id
            ORDER BY obs_count DESC
            LIMIT 5
            """,
        )
        hotspots = [
            {
                "name": str(r["name"]),
                "entity_type": str(r["entity_type"]),
                "observation_count": int(r["obs_count"]),
            }
            for r in hotspot_rows
        ]

        # Entities missing descriptions (top 10)
        no_desc_rows = await storage.fetch_all(
            """
            SELECT name, entity_type
            FROM entities
            WHERE description IS NULL OR description = ''
            ORDER BY updated_at DESC
            LIMIT 10
            """,
        )
        missing_descriptions = [
            {"name": str(r["name"]), "entity_type": str(r["entity_type"])} for r in no_desc_rows
        ]

        # Count entities with empty descriptions
        no_desc_count_row = await storage.fetch_one(
            "SELECT COUNT(*) AS cnt FROM entities WHERE description IS NULL OR description = ''",
        )
        no_desc_count = int(no_desc_count_row["cnt"]) if no_desc_count_row else 0

        # Build suggested actions
        actions: list[str] = []
        if entity_count > 500:
            actions.append(
                f"Graph has {entity_count} entities — consider pruning stale or low-value entries"
            )
        if hotspots and hotspots[0]["observation_count"] > 15:
            actions.append(
                f"Entity '{hotspots[0]['name']}' has {hotspots[0]['observation_count']} "
                f"observations — consider compacting with compact_observations"
            )
        if no_desc_count > 0:
            actions.append(
                f"{no_desc_count} entities have empty descriptions — use update_entity to add them"
            )
        if obs_count > 0 and entity_count > 0:
            avg_obs = obs_count / entity_count
            if avg_obs > 10:
                actions.append(
                    f"Average {avg_obs:.1f} observations per entity — consider consolidating"
                )

        return {
            "counts": {
                "entities": entity_count,
                "relationships": rel_count,
                "observations": obs_count,
            },
            "entity_types": type_dist_capped,
            "observation_hotspots": hotspots,
            "missing_descriptions": missing_descriptions,
            "missing_description_count": no_desc_count,
            "suggested_actions": actions,
        }

    except GraphMemError as exc:
        return _error_response(exc, tool_name="graph_health")


@mcp.tool()
async def compact_observations(
    entity_name: str,
    keep_ids: list[str],
    new_observations: list[str],
) -> dict[str, Any]:
    """Atomic observation compaction — delete old observations and add new ones in one step.

    Use this to consolidate many observations into fewer, denser ones.
    You decide what to merge — this tool makes it atomic so no data is lost.

    Workflow: get_entity → read observations → decide which to keep vs merge →
    call compact_observations with keep_ids (observations to preserve unchanged)
    and new_observations (your merged/summarized replacements).

    Args:
        entity_name: Name of the entity to compact.
        keep_ids: Observation IDs to preserve unchanged. All others are deleted.
        new_observations: New observation texts to add (your merged summaries).
    """
    try:
        state = _require_state()

        # Resolve entity and get current observations
        entity = await state.graph.resolve_entity(entity_name)
        current_obs = await state.storage.get_observations_for_entity(entity.id)

        # Determine which IDs to delete (everything not in keep_ids)
        keep_set = set(keep_ids)
        delete_ids = [str(obs["id"]) for obs in current_obs if str(obs["id"]) not in keep_set]

        # Validate keep_ids all belong to this entity
        current_ids = {str(obs["id"]) for obs in current_obs}
        invalid_keeps = keep_set - current_ids
        if invalid_keeps:
            return _error_response(
                GraphMemError(
                    f"Observation IDs not found on entity '{entity_name}': "
                    f"{', '.join(sorted(invalid_keeps))}"
                ),
                tool_name="compact_observations",
            )

        # Delete observations not in keep list
        deleted_count = 0
        for obs_id in delete_ids:
            was_deleted = await state.storage.delete_observation(obs_id)
            if was_deleted:
                deleted_count += 1
                # Clean up embedding
                if state.embeddings.available:
                    with contextlib.suppress(GraphMemError):
                        await state.embeddings.delete_observation_embedding(obs_id)

        # Add new observations
        added_results = []
        if new_observations:
            obs_objs = [Observation.pending(text) for text in new_observations]
            added_results = await state.graph.add_observations(entity_name, obs_objs)
            await _embed_observations(added_results)

        # Final count
        remaining = len(keep_ids) + len(added_results)

        return {
            "entity_name": entity_name,
            "before": len(current_obs),
            "deleted": deleted_count,
            "kept": len(keep_ids),
            "added": len(added_results),
            "after": remaining,
            "status": "compacted",
        }

    except GraphMemError as exc:
        return _error_response(exc, tool_name="compact_observations")


@mcp.tool()
async def suggest_connections(
    entity_name: str,
    limit: int = 10,
) -> dict[str, Any]:
    """Find potential relationships for an entity by semantic similarity.

    Solves the "large graph" problem: when you add a new entity, you can't
    read the whole graph to know what to connect it to. This tool searches
    for semantically related entities and shows which ones already have
    relationships vs which are unconnected — giving you concrete suggestions.

    Args:
        entity_name: Name of the entity to find connections for.
        limit: Max suggestions to return (default 10).
    """
    try:
        state = _require_state()

        # Resolve the entity
        entity = await state.graph.resolve_entity(entity_name)

        # Search for semantically similar entities using the entity's own text
        query = f"{entity.name} {entity.entity_type} {entity.description or ''}"
        search_results = await state.search.search_entities(
            query.strip(),
            limit=limit + 1,  # +1 because self might appear
            include_observations=False,
        )

        # Get existing relationships for this entity
        existing_rels = await state.graph.get_relationships(entity_name)
        connected_names: set[str] = set()
        for rel in existing_rels:
            connected_names.add(str(rel.get("source_name", "")))
            connected_names.add(str(rel.get("target_name", "")))
            # Also handle the flat format from get_relationships
            connected_names.add(str(rel.get("source", "")))
            connected_names.add(str(rel.get("target", "")))
        connected_names.discard("")
        connected_names.discard(entity_name)

        # Build suggestions
        suggestions: list[dict[str, Any]] = []
        for result in search_results:
            name = str(result.get("name", ""))
            if name == entity_name:
                continue  # skip self

            already_connected = name in connected_names
            suggestions.append(
                {
                    "name": name,
                    "entity_type": result.get("entity_type", ""),
                    "description": result.get("description", ""),
                    "already_connected": already_connected,
                    "score": result.get("score", 0),
                }
            )

            if len(suggestions) >= limit:
                break

        unconnected = [s for s in suggestions if not s["already_connected"]]
        connected = [s for s in suggestions if s["already_connected"]]

        return {
            "entity": entity_name,
            "suggestions": suggestions,
            "unconnected_count": len(unconnected),
            "already_connected_count": len(connected),
            "hint": (
                "Entities listed as already_connected=false are candidates "
                "for new relationships. Use add_relationships to connect them."
                if unconnected
                else "All similar entities are already connected."
            ),
        }

    except GraphMemError as exc:
        return _error_response(exc, tool_name="suggest_connections")
