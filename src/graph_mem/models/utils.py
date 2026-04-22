"""Shared utilities for data model modules."""

from __future__ import annotations


def safe_float(val: object, default: float = 0.0) -> float:
    """Safely coerce a DB row value to *float*.

    SQLite row dicts use ``dict[str, object]``, so ``.get()`` returns
    ``object``.  This helper handles ``None`` and non-numeric types
    gracefully — always returns a float, never raises.
    """
    if val is None:
        return default
    try:
        return float(val)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default
