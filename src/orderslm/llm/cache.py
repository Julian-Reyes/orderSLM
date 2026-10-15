"""Record/replay cache (ported from AgentDesk server/src/llm/cache.ts).

Key: sha256 of stable JSON of the request plus every config field that changes what the provider
is asked. Modes: off (always call), record (replay hits, call and save misses), replay (hits only;
a miss is an error, so a replay run is guaranteed $0), refresh (always call, overwrite).
Writes are atomic. A replayed response keeps its original latency and cost and is marked cached.
"""

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Literal

from orderslm.paths import ROOT

from .config import ModelConfig
from .types import ChatClient, ChatRequest, ChatResponse

CacheMode = Literal["off", "record", "replay", "refresh"]
CACHE_MODES: tuple[CacheMode, ...] = ("off", "record", "replay", "refresh")
CACHE_DIR = ROOT / ".llm-cache"


class CacheMiss(LookupError):
    pass


def cache_key_material(config: ModelConfig, request: ChatRequest) -> dict[str, Any]:
    return {
        "config": config.model_dump(
            include={"id", "api", "base_url", "model", "structured_output", "max_tokens_param", "extra_body"}
        ),
        "request": request.model_dump(mode="json"),
    }


def cache_key(config: ModelConfig, request: ChatRequest) -> str:
    stable = json.dumps(cache_key_material(config, request), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(stable.encode()).hexdigest()


class CachedClient:
    def __init__(self, inner: ChatClient, config: ModelConfig, mode: CacheMode, cache_dir: Path = CACHE_DIR):
        if mode not in CACHE_MODES:
            raise ValueError(f"cache mode must be one of {CACHE_MODES}, got {mode!r}")
        self._inner = inner
        self._config = config
        self._mode = mode
        self._dir = cache_dir / config.id.replace("/", "__")

    @property
    def config_id(self) -> str:
        return self._config.id

    def path_for(self, request: ChatRequest) -> Path:
        return self._dir / f"{cache_key(self._config, request)}.json"

    def complete(self, request: ChatRequest) -> ChatResponse:
        if self._mode == "off":
            return self._inner.complete(request)
        path = self.path_for(request)
        if self._mode in ("record", "replay") and path.exists():
            saved = json.loads(path.read_text())
            return ChatResponse.model_validate(saved["response"]).model_copy(update={"cached": True})
        if self._mode == "replay":
            raise CacheMiss(f"{self._config.id}: no cached response at {path.name} (mode=replay)")
        response = self._inner.complete(request)
        record = {
            "key_material": cache_key_material(self._config, request),
            "response": response.model_dump(mode="json"),
        }
        _atomic_write(path, json.dumps(record, indent=1, sort_keys=True))
        return response


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
