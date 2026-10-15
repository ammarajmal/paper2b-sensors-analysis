"""Minimal Ollama client (local only). Uses the standard library, no extra dependency."""

from __future__ import annotations

import json
import os
import re
import urllib.request

HOST = os.environ.get("OLLAMA_HOST_URL", "http://127.0.0.1:11434")


def _post(route: str, body: dict, timeout: int = 600) -> dict:
    req = urllib.request.Request(
        HOST + route, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def available_models() -> list[str]:
    return [
        m["name"]
        for m in json.load(urllib.request.urlopen(HOST + "/api/tags", timeout=10))["models"]
    ]


def chat_json(
    model: str, system: str, user: str, num_ctx: int = 8192, num_predict: int = 900
) -> tuple[dict | None, str, float]:
    """Return (parsed JSON or None, raw text, seconds). Temperature 0, thinking off, JSON mode."""
    body = {
        "model": model,
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": "30m",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "options": {"temperature": 0, "num_ctx": num_ctx, "num_predict": num_predict, "seed": 7},
    }
    r = _post("/api/chat", body)
    raw = r["message"]["content"]
    secs = r.get("total_duration", 0) / 1e9
    try:
        return json.loads(raw), raw, secs
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                return json.loads(m.group(0)), raw, secs
            except json.JSONDecodeError:
                pass
    return None, raw, secs


def embed(model: str, texts: list[str]) -> list[list[float]]:
    return _post("/api/embed", {"model": model, "input": texts, "keep_alive": "30m"})["embeddings"]


def generate_text(
    model: str, system: str, user: str, num_ctx: int = 8192, num_predict: int = 700
) -> str:
    body = {
        "model": model,
        "stream": False,
        "think": False,
        "keep_alive": "30m",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "options": {"temperature": 0, "num_ctx": num_ctx, "num_predict": num_predict, "seed": 7},
    }
    return _post("/api/chat", body)["message"]["content"]
