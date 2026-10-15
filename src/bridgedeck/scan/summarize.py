"""Stage 2: summarise each UNIQUE file once with a local model, then verify the model's quotes against the file."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np

from . import llm, prompts, walk


def _norm(s: str) -> str:
    s = re.sub(r"[`*_#>|\\]", "", s)  # markdown the model tends to drop when quoting
    return re.sub(r"\s+", " ", s).strip().lower()


def _grams(text: str, n: int = 3) -> set[tuple[str, ...]]:
    w = re.findall(r"[a-z0-9.%+-]+", _norm(text))
    return {tuple(w[i : i + n]) for i in range(len(w) - n + 1)}


def trust_score(js: dict, text: str, cat: str) -> float:
    """Evidence check: for each quote the model gives, the share of its 3-word sequences that occur in the file,
    averaged over quotes (1.0 = all quotes verbatim or nearly; ~0 = invented). Tolerates small edits."""
    ev = [q for q in js.get("evidence", []) if isinstance(q, str) and len(q.split()) >= 3]
    if not ev:
        return 0.0
    body = _grams(text)
    cov = []
    for q in ev:
        g = _grams(q)
        cov.append(len(g & body) / len(g) if g else 0.0)
    return round(sum(cov) / len(cov), 3)


def numbers_ok(js: dict, text: str) -> float | None:
    """Share of the numbers listed by the model whose value string occurs in the document (None if none listed)."""
    nums = js.get("numbers")
    if not isinstance(nums, list):
        return None
    vals = [
        re.sub(r"[\s,]", "", str(n.get("value", "")).lower()) for n in nums if isinstance(n, dict)
    ]
    vals = [v for v in vals if len(v) >= 2]
    if not vals:
        return None
    body = re.sub(r"[\s,]", "", text.lower())
    return round(sum(v in body for v in vals) / len(vals), 3)


def build_content(path: Path, cat: str, cfg: dict) -> str:
    lim = cfg["limits"]
    txt = walk.read_text(path, 2_000_000)
    head = lim["doc_head_chars"] if cat == "doc" else lim["head_chars"]
    if len(txt) <= head + lim["tail_chars"]:
        return txt
    out = (
        txt[:head] + "\n...[truncated]...\n" + (txt[-lim["tail_chars"] :] if cat == "code" else "")
    )
    if cat == "doc":
        heads = [ln for ln in txt.splitlines() if ln.startswith("#")][:40]
        out += "\nHEADINGS: " + " | ".join(heads)
    return out


def full_text(path: Path) -> str:
    return walk.read_text(path, 2_000_000)


def run(
    con,
    cfg: dict,
    model: str,
    limit: int | None = None,
    only: str | None = None,
    verbose: bool = True,
) -> dict:
    roles = {r["label"]: r["role"] for r in cfg["roots"]}
    rows = con.execute(
        "SELECT sha, MIN(path), MIN(label), MIN(rel), MIN(cat), MIN(facts) FROM files WHERE skipped='' AND sha!='' AND cat IN ('code','doc') GROUP BY sha ORDER BY MIN(label), MIN(rel)"
    ).fetchall()
    done = {r[0] for r in con.execute("SELECT sha FROM summaries WHERE ver=?", (prompts.VER,))}
    todo = [r for r in rows if r[0] not in done and (only is None or re.search(only, r[1]))]
    if limit:
        todo = todo[:limit]
    stats = {"todo": len(todo), "done": 0, "failed": 0}
    t_start = time.time()
    for i, (sha, path, label, rel, cat, facts) in enumerate(todo, 1):
        p = Path(path)
        content = build_content(p, cat, cfg)
        f = json.loads(facts)
        short = {k: v for k, v in f.items() if v and k != "doc"}
        if f.get("doc"):
            short["docstring"] = f["doc"]
        tmpl = prompts.CODE if cat == "code" else prompts.DOC
        user = tmpl.format(
            rel=rel,
            label=label,
            role=roles.get(label, ""),
            facts=json.dumps(short)[:1500],
            content=content,
            tags=prompts.TAGS,
        )
        js, raw, secs = llm.chat_json(model, prompts.SYSTEM, user)
        if js is None:  # one retry with a longer output budget (the reply was probably cut off)
            js, raw, secs2 = llm.chat_json(model, prompts.SYSTEM, user, num_predict=1800)
            secs += secs2
        if js is None:
            stats["failed"] += 1
            js = {"error": "unparsable", "raw": raw[:300]}
            trust = 0.0
        else:
            full = full_text(p)
            trust = trust_score(js, full, cat)
            if cat == "doc":
                js["_numbers_verified"] = numbers_ok(js, full)
        con.execute(
            "INSERT OR REPLACE INTO summaries VALUES(?,?,?,?,?,?,?)",
            (sha, prompts.VER, model, cat, json.dumps(js, ensure_ascii=False), trust, secs),
        )
        con.commit()
        stats["done"] += 1
        if verbose and (i % 10 == 0 or i == len(todo)):
            el = time.time() - t_start
            print(
                f"[{i}/{len(todo)}] {el / 60:.1f} min elapsed, ~{el / i * (len(todo) - i) / 60:.0f} min left | last trust {trust:.2f} | {rel[:70]}",
                flush=True,
            )
    return stats


def embed_all(con, model: str, batch: int = 16) -> int:
    rows = con.execute(
        "SELECT s.sha, s.js, MIN(f.rel) FROM summaries s JOIN files f ON f.sha=s.sha WHERE s.ver=? AND s.sha NOT IN (SELECT sha FROM emb) GROUP BY s.sha",
        (prompts.VER,),
    ).fetchall()
    n = 0
    for i in range(0, len(rows), batch):
        chunk = rows[i : i + batch]
        texts = []
        for sha, js, rel in chunk:
            d = json.loads(js)
            texts.append(
                f"{rel}\n{d.get('purpose') or d.get('summary', '')}\n{' '.join(d.get('method', []) if isinstance(d.get('method'), list) else [])}\n{' '.join(d.get('tags', []) if isinstance(d.get('tags'), list) else [])}"
            )
        vecs = llm.embed(model, texts)
        for (sha, _, _), v in zip(chunk, vecs):
            con.execute(
                "INSERT OR REPLACE INTO emb VALUES(?,?,?)",
                (sha, model, np.asarray(v, dtype=np.float32).tobytes()),
            )
            n += 1
        con.commit()
    return n
