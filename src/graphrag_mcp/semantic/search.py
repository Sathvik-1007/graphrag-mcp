"""Hybrid search combining vector similarity, FTS5 full-text, and RRF fusion.

Search strategy:
1. Vector similarity via StorageBackend.vector_search (cosine distance)
2. FTS5 full-text search via StorageBackend.fts_search_*
3. Reciprocal Rank Fusion to combine rankings

RRF_score(item) = sum(1 / (k + rank_in_method))  where k=60

The search layer is **storage-agnostic**: it delegates all persistence
and query operations to a :class:`StorageBackend`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

from graphrag_mcp.models.entity import Entity
from graphrag_mcp.models.observation import Observation
from graphrag_mcp.utils.errors import EmbeddingError
from graphrag_mcp.utils.logging import get_logger

if TYPE_CHECKING:
    from graphrag_mcp.semantic.embeddings import EmbeddingEngine
    from graphrag_mcp.storage.base import StorageBackend


class _RelationshipEntry(TypedDict):
    """Shape of relationship entries nested inside search results."""

    relationship_type: str
    direction: str
    connected_entity: str
    weight: float


class SearchResult(TypedDict, total=False):
    """Return type for entity/observation search results.

    Required keys come from ``Entity.to_dict()`` plus ``relevance_score``.
    Optional keys (``observations``, ``relationships``) are present depending
    on the search method and options.
    """

    # Required keys (from Entity.to_dict)
    id: str
    name: str
    entity_type: str
    description: str
    properties: dict[str, object]
    created_at: float
    updated_at: float
    relevance_score: float
    # Optional keys
    observations: list[dict[str, object]]
    relationships: list[_RelationshipEntry]


log = get_logger("semantic.search")

RRF_K = 60  # Standard RRF constant


class HybridSearch:
    """Combined vector + full-text search with RRF fusion.

    Usage::
        search = HybridSearch(storage, embedding_engine)
        results = await search.search_entities("detective in Berlin", limit=10)
    """

    def __init__(self, storage: StorageBackend, embeddings: EmbeddingEngine) -> None:
        self._storage = storage
        self._embeddings = embeddings

    # ── Shared retrieval primitives ──────────────────────────────────

    async def _vector_search(
        self,
        query: str,
        table: str,
        limit: int,
    ) -> dict[str, float]:
        """Run vector similarity search and return ``{id: rrf_score}``."""
        results: dict[str, float] = {}
        if not self._embeddings.available:
            return results

        try:
            vectors = await self._embeddings.embed([query])
            query_vec = vectors[0]
            if query_vec is None:
                raise ValueError("Embedding returned None for query")

            from graphrag_mcp.semantic.embeddings import _embedding_to_bytes

            query_blob = _embedding_to_bytes(query_vec)

            rows = await self._storage.vector_search(table, query_blob, limit * 3)
            for rank, (item_id, _distance) in enumerate(rows):
                results[item_id] = 1.0 / (RRF_K + rank + 1)
        except (ValueError, EmbeddingError) as exc:
            log.warning(
                "Vector search on %s unavailable: %s — results will rely on FTS5 only", table, exc
            )

        return results

    async def _fts_entity_search(self, query: str, limit: int) -> dict[str, float]:
        """Run FTS5 search on entities and return ``{id: rrf_score}``."""
        results: dict[str, float] = {}
        rows = await self._storage.fts_search_entities(query, limit * 3)
        for rank, (entity_id, _rank_score) in enumerate(rows):
            results[entity_id] = 1.0 / (RRF_K + rank + 1)
        return results

    async def _fts_observation_search(self, query: str, limit: int) -> dict[str, float]:
        """Run FTS5 search on observations and return ``{id: rrf_score}``."""
        results: dict[str, float] = {}
        rows = await self._storage.fts_search_observations(query, limit * 3)
        for rank, (obs_id, _rank_score) in enumerate(rows):
            results[obs_id] = 1.0 / (RRF_K + rank + 1)
        return results

    @staticmethod
    def _rrf_fuse(
        vec_results: dict[str, float],
        fts_results: dict[str, float],
    ) -> list[tuple[str, float]]:
        """Combine vector and FTS results using Reciprocal Rank Fusion.

        Returns ``[(id, score), ...]`` sorted by descending fused score.
        """
        all_ids = set(vec_results) | set(fts_results)
        if not all_ids:
            return []

        scored = [
            (item_id, vec_results.get(item_id, 0.0) + fts_results.get(item_id, 0.0))
            for item_id in all_ids
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    # ── Public search methods ────────────────────────────────────────

    async def search_entities(
        self,
        query: str,
        *,
        limit: int = 10,
        entity_types: list[str] | None = None,
        include_observations: bool = False,
    ) -> list[SearchResult]:
        """Search entities using hybrid vector + FTS5 + RRF.

        Returns entities ranked by fused relevance score, with optional
        observations and direct relationships attached.
        """
        vec_results = await self._vector_search(query, "entity_embeddings", limit)
        fts_results = await self._fts_entity_search(query, limit)
        scored = self._rrf_fuse(vec_results, fts_results)
        if not scored:
            return []

        # ── Batch-fetch entities in one query ────────────────────────
        candidate_ids = [eid for eid, _ in scored[: limit * 3]]
        if not candidate_ids:
            return []

        rows = await self._storage.fetch_entity_rows(candidate_ids)

        # Apply type filter if needed
        if entity_types:
            type_set = set(entity_types)
            rows = [r for r in rows if str(r.get("entity_type", "")) in type_set]

        # Build lookup for O(1) access by id
        row_by_id: dict[str, Any] = {str(r["id"]): r for r in rows}

        # ── Assemble results in score order ──────────────────────────
        results: list[SearchResult] = []
        for entity_id, score in scored:
            if entity_id not in row_by_id:
                continue

            entity = Entity.from_row(row_by_id[entity_id])
            entry = SearchResult(
                **entity.to_dict(),  # type: ignore[typeddict-item]
                relevance_score=round(score, 6),
            )

            # Optionally attach observations
            if include_observations:
                obs_rows = await self._storage.get_observations_for_entity(entity_id)
                entry["observations"] = [Observation.from_row(r).to_dict() for r in obs_rows]

            # Attach direct relationships (always useful context)
            rel_rows = await self._storage.get_relationships_for_entity(entity_id)
            entry["relationships"] = [
                _RelationshipEntry(
                    relationship_type=str(r["relationship_type"]),
                    direction="outgoing" if str(r.get("source_id")) == entity_id else "incoming",
                    connected_entity=(
                        str(r.get("target_name", ""))
                        if str(r.get("source_id")) == entity_id
                        else str(r.get("source_name", ""))
                    ),
                    weight=float(r["weight"]),
                )
                for r in rel_rows[:20]  # Limit to 20 relationships per entity
            ]

            results.append(entry)
            if len(results) >= limit:
                break

        return results

    async def search_observations(
        self,
        query: str,
        *,
        limit: int = 10,
        entity_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search observations using hybrid vector + FTS5 + RRF.

        Optionally scoped to a single entity.
        """
        vec_results = await self._vector_search(query, "observation_embeddings", limit)
        fts_results = await self._fts_observation_search(query, limit)
        scored = self._rrf_fuse(vec_results, fts_results)
        if not scored:
            return []

        # ── Batch-fetch observations ─────────────────────────────────
        candidate_ids = [oid for oid, _ in scored[: limit * 3]]
        if not candidate_ids:
            return []

        # Use raw fetch for observation batch lookup
        obs_rows = await self._storage.fetch_all(
            f"SELECT * FROM observations WHERE id IN ({','.join('?' for _ in candidate_ids)})",
            tuple(candidate_ids),
        )
        obs_by_id: dict[str, Any] = {str(r["id"]): r for r in obs_rows}

        # ── Batch-fetch parent entity names ──────────────────────────
        parent_ids = {str(r["entity_id"]) for r in obs_rows}
        ent_lookup = await self._storage.resolve_entity_names(parent_ids)
        # Also need entity_type — fetch full rows
        ent_type_lookup: dict[str, str] = {}
        if parent_ids:
            ent_rows = await self._storage.fetch_entity_rows(list(parent_ids))
            ent_type_lookup = {str(r["id"]): str(r.get("entity_type", "")) for r in ent_rows}

        # ── Assemble results in score order ──────────────────────────
        results: list[dict[str, Any]] = []
        for obs_id, score in scored:
            row = obs_by_id.get(obs_id)
            if not row:
                continue
            if entity_id and str(row["entity_id"]) != entity_id:
                continue

            obs = Observation.from_row(row)
            entry: dict[str, Any] = {**obs.to_dict(), "relevance_score": round(score, 6)}

            parent_eid = str(row["entity_id"])
            if parent_eid in ent_lookup:
                entry["entity_name"] = ent_lookup[parent_eid]
            if parent_eid in ent_type_lookup:
                entry["entity_type"] = ent_type_lookup[parent_eid]

            results.append(entry)
            if len(results) >= limit:
                break

        return results
