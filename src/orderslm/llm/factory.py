"""Build the client stack for a config id: CachedClient → ThrottledClient → HttpChatClient."""

import os
from functools import partial
from pathlib import Path

import httpx

from orderslm.domain.clock import Clock, system_clock

from .cache import CACHE_DIR, CACHE_MODES, CachedClient, CacheMode
from .client import HttpChatClient
from .config import get_model
from .env import api_key
from .throttle import Throttle, ThrottledClient
from .types import ChatClient

_throttles: dict[str, Throttle] = {}  # one per model, shared by every client in the process


def cache_mode_from_env() -> CacheMode:
    mode = os.environ.get("LLM_CACHE", "record").strip() or "record"
    if mode not in CACHE_MODES:
        raise ValueError(f"LLM_CACHE must be one of {CACHE_MODES}, got {mode!r}")
    return mode  # type: ignore[return-value]


def make_client(
    config_id: str,
    *,
    cache_mode: CacheMode | None = None,
    clock: Clock | None = None,
    http: httpx.Client | None = None,
    cache_dir: Path = CACHE_DIR,
) -> ChatClient:
    config = get_model(config_id)
    http_client = HttpChatClient(
        config, partial(api_key, config.key_env), clock=clock or system_clock(), http=http
    )
    throttle = _throttles.setdefault(config.id, Throttle(config.rpm))
    return CachedClient(
        ThrottledClient(http_client, throttle),
        config,
        cache_mode or cache_mode_from_env(),
        cache_dir,
    )
