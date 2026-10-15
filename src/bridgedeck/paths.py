"""Resolve config/paths.yaml (with ${key} substitution) and guard inputs against writes."""

from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def load(config: str | os.PathLike | None = None) -> dict:
    raw = yaml.safe_load(Path(config or REPO / "config/paths.yaml").read_text())
    root = raw["phd_root"]

    def sub(v):
        if isinstance(v, dict):
            return {k: sub(x) for k, x in v.items()}
        return v.replace("${phd_root}", root) if isinstance(v, str) else v

    cfg = sub(raw)
    if os.environ.get("BVP_OUT"):
        cfg["outputs"] = os.environ["BVP_OUT"]
    return cfg


def out_dir(*parts: str) -> Path:
    p = Path(load()["outputs"], *parts)
    p.mkdir(parents=True, exist_ok=True)
    return p


def assert_not_input(path: os.PathLike) -> None:
    """Refuse to write inside any configured input tree."""
    target = Path(path).resolve()
    cfg = load()
    roots = [cfg["phd_root"], *cfg["bags"].values(), *cfg["laser"].values()]
    for r in roots:
        if re.match(re.escape(str(Path(r).resolve())), str(target)):
            raise PermissionError(f"refusing to write into input tree: {target}")
