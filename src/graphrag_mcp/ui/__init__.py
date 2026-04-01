"""Web UI for interactive graph exploration.

Provides a read-only REST API backed by the existing storage and search
engines, plus a built-in React SPA for visualising the knowledge graph.

Optional dependency — install with ``pip install graphrag-mcp[ui]``.
"""

from __future__ import annotations

__all__ = ["create_app", "start_server"]


def __getattr__(name: str) -> object:
    """Lazy imports to avoid pulling in aiohttp at package-scan time."""
    if name == "create_app":
        from graphrag_mcp.ui.server import create_app

        return create_app
    if name == "start_server":
        from graphrag_mcp.ui.server import start_server

        return start_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
