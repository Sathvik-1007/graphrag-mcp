"""Tests for graph_mem.ui.server module.

Covers _resolve_frontend_dir, create_app, and _error_middleware.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import web

from graph_mem.ui import server


# ---------------------------------------------------------------------------
# Minimal mocks
# ---------------------------------------------------------------------------


class StubStorage:
    """Bare-minimum storage mock."""

    async def list_entities(self, **kw):
        return []

    async def count_entities(self):
        return 0

    async def count_relationships(self):
        return 0

    async def count_observations(self):
        return 0

    async def entity_type_distribution(self):
        return {}

    async def relationship_type_distribution(self):
        return {}

    async def most_connected_entities(self, limit=10):
        return []

    async def recent_entities(self, limit=10):
        return []

    async def fetch_relationships_between(self, ids):
        return []


class StubSearch:
    """Bare-minimum search mock."""

    async def search_entities(self, *a, **kw):
        return []


# ---------------------------------------------------------------------------
# _resolve_frontend_dir
# ---------------------------------------------------------------------------


class TestResolveFrontendDir:
    """Tests for _resolve_frontend_dir."""

    def setup_method(self):
        # Reset cached value before each test
        server._FRONTEND_DIR = None

    def teardown_method(self):
        server._FRONTEND_DIR = None

    def test_returns_none_when_no_frontend(self):
        """Should return None when frontend dir missing."""
        with patch("importlib.resources.files") as mock_files:
            mock_files.return_value.__truediv__ = lambda self, x: Path("/nonexistent/frontend")
            result = server._resolve_frontend_dir()
            assert result is None

    def test_returns_path_when_frontend_exists(self, tmp_path):
        """Should return path when frontend/index.html exists."""
        frontend = tmp_path / "frontend"
        frontend.mkdir()
        (frontend / "index.html").write_text("<html></html>")

        with patch("importlib.resources.files") as mock_files:
            mock_files.return_value = tmp_path
            result = server._resolve_frontend_dir()
            assert result == frontend
            assert result.is_dir()

    def test_caches_result(self, tmp_path):
        """Second call returns cached value without re-resolving."""
        frontend = tmp_path / "frontend"
        frontend.mkdir()
        (frontend / "index.html").write_text("<html></html>")

        with patch("importlib.resources.files") as mock_files:
            mock_files.return_value = tmp_path
            first = server._resolve_frontend_dir()
            second = server._resolve_frontend_dir()
            assert first is second
            # Only called once due to cache
            mock_files.assert_called_once()


# ---------------------------------------------------------------------------
# create_app
# ---------------------------------------------------------------------------


class TestCreateApp:
    """Tests for create_app factory."""

    @pytest.fixture(autouse=True)
    def _reset_frontend(self):
        server._FRONTEND_DIR = None
        yield
        server._FRONTEND_DIR = None

    async def test_returns_web_application(self):
        """create_app returns aiohttp Application."""
        storage = StubStorage()
        search = StubSearch()
        app = await server.create_app(storage, search)
        assert isinstance(app, web.Application)

    async def test_app_has_storage_and_search(self):
        """App dict contains storage and search."""
        storage = StubStorage()
        search = StubSearch()
        app = await server.create_app(storage, search)
        assert app["storage"] is storage
        assert app["search"] is search

    async def test_app_has_graph_when_provided(self):
        """App dict contains graph when passed."""
        storage = StubStorage()
        search = StubSearch()
        fake_graph = object()
        app = await server.create_app(storage, search, graph=fake_graph)
        assert app["graph"] is fake_graph

    async def test_app_has_no_graph_key_when_none(self):
        """App dict has no graph key when not passed."""
        storage = StubStorage()
        search = StubSearch()
        app = await server.create_app(storage, search)
        assert "graph" not in app

    async def test_app_has_db_path(self):
        """App stores db_path when provided."""
        storage = StubStorage()
        search = StubSearch()
        app = await server.create_app(storage, search, db_path="/tmp/test.db")
        assert app["db_path"] == "/tmp/test.db"

    async def test_app_has_switch_lock(self):
        """App creates switch_lock for graph switching."""
        import asyncio

        storage = StubStorage()
        search = StubSearch()
        app = await server.create_app(storage, search)
        assert isinstance(app["switch_lock"], asyncio.Lock)

    async def test_app_has_routes(self):
        """App has API routes registered."""
        storage = StubStorage()
        search = StubSearch()
        app = await server.create_app(storage, search)
        # Check some known routes exist
        route_paths = [
            r.resource.canonical if hasattr(r, "resource") and r.resource else ""
            for r in app.router.routes()
        ]
        assert "/api/graph" in route_paths
        assert "/api/stats" in route_paths


# ---------------------------------------------------------------------------
# _error_middleware
# ---------------------------------------------------------------------------


class TestErrorMiddleware:
    """Tests for _error_middleware."""

    async def test_passes_through_normal_response(self):
        """Normal handler response passes through untouched."""
        expected = web.json_response({"ok": True})

        async def handler(request):
            return expected

        app = web.Application()
        request = _make_fake_request(app)
        result = await server._error_middleware(request, handler)
        assert result is expected

    async def test_reraises_http_exceptions(self):
        """HTTPException (like 404) re-raised for aiohttp."""

        async def handler(request):
            raise web.HTTPNotFound()

        app = web.Application()
        request = _make_fake_request(app)
        with pytest.raises(web.HTTPNotFound):
            await server._error_middleware(request, handler)

    async def test_catches_unhandled_and_returns_500(self):
        """Unhandled exception returns 500 JSON."""

        async def handler(request):
            raise RuntimeError("boom")

        app = web.Application()
        request = _make_fake_request(app)
        result = await server._error_middleware(request, handler)
        assert result.status == 500
        import json

        body = json.loads(result.body)
        assert body["error"] == "Internal server error"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_fake_request(app):
    """Create a minimal fake request for middleware testing."""
    from unittest.mock import MagicMock

    request = MagicMock(spec=web.Request)
    request.app = app
    request.method = "GET"
    request.path = "/test"
    return request
