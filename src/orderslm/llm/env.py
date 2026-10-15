"""Read API keys from the environment, falling back to the gitignored .env. Keys are never logged."""

import os
from pathlib import Path

from orderslm.paths import ROOT


def read_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[name.strip()] = value
    return values


def api_key(name: str, dotenv: Path = ROOT / ".env") -> str:
    value = os.environ.get(name, "").strip() or read_dotenv(dotenv).get(name, "").strip()
    if not value:
        raise KeyError(f"{name} is not set (environment or .env)")
    return value
