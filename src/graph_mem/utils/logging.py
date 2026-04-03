"""Structured logging setup for graph-mem.

Uses the standard library logging module with a consistent format.
Log level is controlled by GRAPHMEM_LOG_LEVEL (default: WARNING).
"""

from __future__ import annotations

import logging
import os
import sys

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "WARNING") -> None:
    """Configure the root graph_mem logger.

    Safe to call multiple times.  Reconfigures when the requested level
    differs from the current one; otherwise is a no-op.
    """
    root = logging.getLogger("graph_mem")
    target_level = getattr(logging, level.upper(), logging.WARNING)

    if root.level == target_level and root.handlers:
        return  # Already configured at this level

    root.setLevel(target_level)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
        root.addHandler(handler)

    # Suppress noisy third-party loggers
    for name in (
        "sentence_transformers",
        "transformers",
        "torch",
        "onnxruntime",
        "httpx",
        "httpcore",
        "huggingface_hub",
        "filelock",
        "urllib3",
    ):
        logging.getLogger(name).setLevel(logging.ERROR)

    # Suppress the HuggingFace token warning via environment variable
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"graph_mem.{name}")
