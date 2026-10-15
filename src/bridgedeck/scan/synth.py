"""Stage 3: folder-level syntheses from the file summaries (map-reduce), then the catalogue files."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from . import llm, prompts


def _purpose(js: dict) -> str:
    return (js.get("purpose") or js.get("summary") or "").replace("\n", " ")[:230]


def _flags(facts_json: str) -> str:
    f = json.loads(facts_json or "{}")
    out = []
    if f.get("abs_paths"):
        out.append(f"{f['abs_paths']} absolute paths")
    if f.get("todo_marks"):
        out.append(f"{f['todo_marks']} TODO")
    if f.get("legacy_words", 0) >= 3:
        out.append("mentions legacy/old/superseded")
    return ", ".join(out)


def load_overrides(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def apply_overrides(rows: list[dict], overrides: list[dict]) -> None:
    import re as _re

    for r in rows:
        for o in overrides:
            if o["label"] in ("*", r["label"]) and _re.search(o["rel_regex"], r["rel"]):
                r["reuse"], r["reuse_why"] = o["verdict"], o["why"]
                break


def folder_summaries(con, cfg: dict, model: str, min_files: int = 3) -> int:
    roles = {r["label"]: r["role"] for r in cfg["roots"]}
    q = """SELECT f.label, f.rel, s.js FROM files f JOIN summaries s ON s.sha=f.sha AND s.ver=? WHERE f.skipped=''"""
    by = defaultdict(list)
    for label, rel, js in con.execute(q, (prompts.VER,)):
        parts = Path(rel).parts
        key = (label, str(Path(*parts[:-1])) if len(parts) > 1 else ".")
        by[key].append((Path(rel).name, json.loads(js)))
    done = {
        (a, b) for a, b in con.execute("SELECT label, rel FROM dirs WHERE ver=?", (prompts.VER,))
    }
    n = 0
    for (label, rel), items in sorted(by.items()):
        if len(items) < min_files or (label, rel) in done:
            continue
        lines = []
        for name, js in items[:60]:
            tags = ",".join(js.get("tags", [])[:3]) if isinstance(js.get("tags"), list) else ""
            lines.append(f"- {name}: {_purpose(js)} [{js.get('status', '?')}; {tags}]")
        user = prompts.DIR.format(
            rel=rel, label=label, role=roles.get(label, ""), items="\n".join(lines)[:7000]
        )
        js, _, _ = llm.chat_json(model, prompts.SYSTEM, user, num_predict=500)
        con.execute(
            "INSERT OR REPLACE INTO dirs VALUES(?,?,?,?,?)",
            (
                label,
                rel,
                prompts.VER,
                model,
                json.dumps(js or {"error": "unparsable"}, ensure_ascii=False),
            ),
        )
        con.commit()
        n += 1
    return n


def write_catalog(con, cfg: dict, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for path, label, rel, cat, size, mtime, sha, skipped, facts in con.execute(
        "SELECT path,label,rel,cat,size,mtime,sha,skipped,facts FROM files ORDER BY label, rel"
    ):
        s = (
            con.execute(
                "SELECT js, trust, model FROM summaries WHERE sha=? AND ver=?", (sha, prompts.VER)
            ).fetchone()
            if sha
            else None
        )
        js = json.loads(s[0]) if s else {}
        rows.append(
            {
                "label": label,
                "rel": rel,
                "cat": cat,
                "size": size,
                "mtime": mtime,
                "sha": sha[:10],
                "skipped": skipped,
                "purpose": _purpose(js),
                "status": js.get("status", ""),
                "tags": ",".join(js.get("tags", [])) if isinstance(js.get("tags"), list) else "",
                "relevance": js.get("paper_relevance", ""),
                "reuse": (js.get("reuse") or {}).get("verdict", "")
                if isinstance(js.get("reuse"), dict)
                else "",
                "reuse_why": (js.get("reuse") or {}).get("why", "")
                if isinstance(js.get("reuse"), dict)
                else "",
                "risks": "; ".join(js.get("risks", []))
                if isinstance(js.get("risks"), list)
                else "",
                "trust": s[1] if s else "",
                "model": s[2] if s else "",
                "path": path,
            }
        )
    apply_overrides(rows, load_overrides(out_dir.parent.parent / "config" / "reuse_overrides.csv"))
    with open(out_dir / "catalog.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    # duplicates: same sha under several paths
    dup = defaultdict(list)
    for r in rows:
        if r["sha"]:
            dup[r["sha"]].append(f"{r['label']}:{r['rel']}")
    # per-root markdown
    by = defaultdict(list)
    for r in rows:
        by[r["label"]].append(r)
    index = [
        "# Repository catalogue (machine-generated, local model)\n",
        "Every summary below is produced by a local language model from the file text and is UNVERIFIED unless the `trust` value is high "
        "(share of the model's evidence quotes found verbatim in the file; docs also check stated numbers). Open the file before relying on a summary.\n",
        "| tree | files | summarised | skipped | duplicate-of-another-tree |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, rs in by.items():
        summ = sum(1 for r in rs if r["purpose"])
        skip = sum(1 for r in rs if r["skipped"])
        dups = sum(1 for r in rs if r["sha"] and len(dup[r["sha"]]) > 1)
        index.append(f"| [{label}](CATALOG_{label}.md) | {len(rs)} | {summ} | {skip} | {dups} |")
        lines = [
            f"# {label}\n",
            "| file | purpose | status | tags | reuse | trust |",
            "|---|---|---|---|---|---:|",
        ]
        for r in rs:
            if not r["purpose"]:
                continue
            others = [d for d in dup[r["sha"]] if d != f"{r['label']}:{r['rel']}"]
            note = f" (same content also: {', '.join(others[:2])})" if others else ""
            lines.append(
                f"| `{r['rel']}` | {r['purpose'].replace('|', '/')}{note} | {r['status']} | {r['tags']} | {r['reuse']} | {r['trust']} |"
            )
        folders = con.execute(
            "SELECT rel, js FROM dirs WHERE label=? AND ver=? ORDER BY rel", (label, prompts.VER)
        ).fetchall()
        if folders:
            lines += ["\n## Folder summaries\n"]
            for rel, js in folders:
                d = json.loads(js)
                lines.append(
                    f"- **{rel}**: {d.get('what_it_does', '')} (role: {d.get('pipeline_role', '?')}; key: {', '.join(d.get('key_files', [])[:5]) if isinstance(d.get('key_files'), list) else ''})"
                )
        (out_dir / f"CATALOG_{label}.md").write_text("\n".join(lines) + "\n")
    (out_dir / "INDEX.md").write_text("\n".join(index) + "\n")
    return {"rows": len(rows), "roots": len(by)}


def nearest(con, sha: str, k: int = 5, embed_model: str | None = None) -> list[tuple[str, float]]:
    rows = con.execute("SELECT sha, vec FROM emb").fetchall()
    if not rows:
        return []
    shas = [r[0] for r in rows]
    M = np.vstack([np.frombuffer(r[1], dtype=np.float32) for r in rows])
    M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    i = shas.index(sha)
    sim = M @ M[i]
    order = np.argsort(-sim)[1 : k + 1]
    return [(shas[j], float(sim[j])) for j in order]
