"""Tests for search-related Config fields: rrf_alpha, obs_boost."""

from __future__ import annotations

import os

import pytest

from graph_mem.utils.config import Config
from graph_mem.utils.errors import ConfigError


def test_config_rrf_alpha_default():
    c = Config()
    assert c.rrf_alpha == 0.5


def test_config_obs_boost_default():
    c = Config()
    assert c.obs_boost == 0.5


def test_config_rrf_alpha_invalid():
    os.environ["GRAPHMEM_RRF_ALPHA"] = "2.0"
    try:
        with pytest.raises(ConfigError):
            Config()
    finally:
        del os.environ["GRAPHMEM_RRF_ALPHA"]


def test_config_obs_boost_invalid():
    os.environ["GRAPHMEM_OBS_BOOST"] = "-1.0"
    try:
        with pytest.raises(ConfigError):
            Config()
    finally:
        del os.environ["GRAPHMEM_OBS_BOOST"]
