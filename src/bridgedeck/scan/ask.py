"""Ask a question against the catalogue (semantic search with the local embedding model, answered by a local chat model)."""

from __future__ import annotations

import json

import numpy as np

from . import llm, prompts


def search(con, question: str, embed_model: str, k: int = 8) -> list[dict]:
    qv = np.asarray(llm.embed(embed_model, [question])[0], dtype=np.float32)
    qv /= np.linalg.norm(qv) + 1e-9
    rows = con.execute("SELECT sha, vec FROM emb").fetchall()
    M = np.vstack([np.frombuffer(r[1], dtype=np.float32) for r in rows])
    M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    top = np.argsort(-(M @ qv))[:k]
    out = []
    for i in top:
        sha = rows[i][0]
        f = con.execute(
            "SELECT label, rel, path FROM files WHERE sha=? ORDER BY label, rel LIMIT 3", (sha,)
        ).fetchall()
        js = json.loads(
            con.execute(
                "SELECT js FROM summaries WHERE sha=? AND ver=?", (sha, prompts.VER)
            ).fetchone()[0]
        )
        out.append({"files": f, "js": js, "score": float(M[i] @ qv)})
    return out


def answer(con, question: str, chat_model: str, embed_model: str, k: int = 8) -> str:
    hits = search(con, question, embed_model, k)
    ctx = []
    for n, h in enumerate(hits, 1):
        d = h["js"]
        ctx.append(
            f"[{n}] {h['files'][0][0]}:{h['files'][0][1]} :: {d.get('purpose') or d.get('summary', '')} | method: {d.get('method', d.get('key_findings', ''))} | status: {d.get('status', '?')}"
        )
    txt = llm.generate_text(
        chat_model,
        prompts.ASK,
        "CATALOGUE ENTRIES:\n" + "\n".join(ctx)[:7000] + f"\n\nQUESTION: {question}",
    )
    paths_ = "\n".join(f"[{n}] {h['files'][0][2]}" for n, h in enumerate(hits, 1))
    return txt.strip() + "\n\nSOURCES:\n" + paths_
