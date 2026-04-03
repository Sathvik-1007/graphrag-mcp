"""Shared test fixtures for graph-mem."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest


@pytest.fixture
def tmp_db_path(tmp_path: Path) -> Path:
    """Provide a temporary database path."""
    return tmp_path / "test_graph.db"


@pytest.fixture
def tmp_graphmem_dir(tmp_path: Path) -> Path:
    """Provide a temporary .graphmem directory."""
    d = tmp_path / ".graphmem"
    d.mkdir()
    return d
