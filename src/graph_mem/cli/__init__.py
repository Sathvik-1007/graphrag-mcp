"""CLI entry points for graph-mem."""

from __future__ import annotations

from graph_mem.cli.install import install_skill, uninstall_skill
from graph_mem.cli.main import cli, main

__all__ = ["cli", "install_skill", "main", "uninstall_skill"]
