"""Typed application keys for the aiohttp UI server.

Using ``web.AppKey`` instead of bare strings eliminates
``NotAppKeyWarning`` and provides type safety for ``app[key]`` access.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from aiohttp import web

if TYPE_CHECKING:
    import asyncio
    from pathlib import Path

    from graph_mem.graph.engine import GraphEngine
    from graph_mem.semantic import HybridSearch
    from graph_mem.storage.base import StorageBackend

storage_key: web.AppKey[StorageBackend] = web.AppKey("storage")
search_key: web.AppKey[HybridSearch] = web.AppKey("search")
graph_key: web.AppKey[GraphEngine] = web.AppKey("graph")
db_path_key: web.AppKey[str] = web.AppKey("db_path")
switch_lock_key: web.AppKey[asyncio.Lock] = web.AppKey("switch_lock")
frontend_dir_key: web.AppKey[Path | None] = web.AppKey("frontend_dir")
