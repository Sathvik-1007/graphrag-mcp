"""Storage layer for graphrag-mcp — backend registry and factory.

Usage::

    from graphrag_mcp.storage import create_backend

    backend = create_backend("sqlite", db_path=Path(".graphrag/graph.db"))
    await backend.initialize()

To register a custom backend::

    from graphrag_mcp.storage import register_backend

    register_backend("neo4j", Neo4jBackend)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graphrag_mcp.storage.base import StorageBackend
from graphrag_mcp.storage.sqlite_backend import SQLiteBackend
from graphrag_mcp.utils.errors import ConfigError

# ── Backend registry ─────────────────────────────────────────────────────

_REGISTRY: dict[str, type[StorageBackend]] = {
    "sqlite": SQLiteBackend,
}


def register_backend(name: str, cls: type[StorageBackend]) -> None:
    """Register a storage backend class under *name*.

    Third-party backends (Neo4j, Memgraph, PostgreSQL) call this at
    import time or via a plugin entry point so they become available
    to :func:`create_backend`.

    Raises:
        ValueError: If a backend with *name* is already registered.
    """
    if name in _REGISTRY:
        raise ValueError(f"Storage backend {name!r} is already registered.")
    _REGISTRY[name] = cls


def available_backends() -> list[str]:
    """Return the names of all registered storage backends."""
    return sorted(_REGISTRY)


def create_backend(backend_type: str = "sqlite", **kwargs: Any) -> StorageBackend:
    """Instantiate a storage backend by name.

    Args:
        backend_type: Registered backend name (default ``"sqlite"``).
        **kwargs: Backend-specific constructor arguments.
            - For ``"sqlite"``: ``db_path`` (``Path``) is required.

    Returns:
        An **uninitialised** :class:`StorageBackend` — call
        ``await backend.initialize()`` before use.

    Raises:
        ConfigError: If *backend_type* is not registered.
        TypeError: If required constructor arguments are missing.
    """
    cls = _REGISTRY.get(backend_type)
    if cls is None:
        available = ", ".join(available_backends())
        raise ConfigError(
            f"Unknown storage backend {backend_type!r}. Available backends: {available}"
        )

    # Backend-specific argument mapping
    if backend_type == "sqlite":
        db_path = kwargs.get("db_path")
        if db_path is None:
            raise TypeError("SQLite backend requires 'db_path' argument.")
        if not isinstance(db_path, Path):
            db_path = Path(db_path)
        return SQLiteBackend(db_path)

    # Generic fallback — pass all kwargs to the constructor
    return cls(**kwargs)


__all__ = [
    "SQLiteBackend",
    "StorageBackend",
    "available_backends",
    "create_backend",
    "register_backend",
]
