"""Deterministic index of RESULT folders (no LLM): what files exist, CSV headers, which scripts name them."""

from __future__ import annotations

import csv
import json
import os
from collections import Counter
from datetime import date
from pathlib import Path

DATA_EXT = {
    ".csv",
    ".json",
    ".npz",
    ".npy",
    ".parquet",
    ".png",
    ".pdf",
    ".txt",
    ".md",
    ".h5",
    ".mat",
    ".xlsx",
    ".tsv",
}


def csv_header(p: Path) -> tuple[str, int]:
    try:
        with open(p, newline="", errors="replace") as fh:
            head = next(csv.reader(fh), [])
            n = sum(1 for _ in fh)
        return ",".join(head)[:240], n
    except Exception:
        return "", 0


def index_results(
    result_roots: list[tuple[str, Path]], producers: dict[str, list[str]]
) -> list[dict]:
    out = []
    for label, base in result_roots:
        for dp, dn, fs in os.walk(base):
            dn[:] = [d for d in dn if d not in (".git", "__pycache__", "worktrees")]
            files = [Path(dp) / f for f in fs if Path(f).suffix.lower() in DATA_EXT]
            if len(files) < 3:
                continue
            ext = Counter(f.suffix.lower() for f in files)
            sizes = sum(f.stat().st_size for f in files)
            mt = sorted(date.fromtimestamp(f.stat().st_mtime).isoformat() for f in files)
            csvs = [f for f in files if f.suffix == ".csv"][:3]
            headers = [f"{c.name}: {h} ({n} rows)" for c in csvs for h, n in [csv_header(c)]]
            jkeys = []
            for jf in [f for f in files if f.suffix == ".json"][:2]:
                try:
                    j = json.loads(jf.read_text(errors="replace")[:300000])
                    jkeys.append(f"{jf.name}: {list(j)[:10] if isinstance(j, dict) else 'list'}")
                except Exception:
                    pass
            prod = sorted({s for f in files for s in producers.get(f.name, [])})[:6]
            out.append(
                {
                    "tree": label,
                    "dir": str(Path(dp).relative_to(base)),
                    "files": len(files),
                    "mb": round(sizes / 1e6, 1),
                    "ext": " ".join(f"{k}:{v}" for k, v in ext.most_common(5)),
                    "oldest": mt[0],
                    "newest": mt[-1],
                    "csv_headers": " || ".join(headers)[:700],
                    "json_keys": " || ".join(jkeys)[:400],
                    "scripts_naming_these_files": "; ".join(prod),
                }
            )
    return out
