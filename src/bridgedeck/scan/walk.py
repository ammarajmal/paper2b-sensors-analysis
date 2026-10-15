"""Stage 1 (no LLM): enumerate files, hash, extract deterministic facts, record git state. Read-only."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

from .. import paths

STD = set(sys.stdlib_module_names)
PATH_RE = re.compile(
    r"""['"](/(?:mnt|media|run|home|tmp)[^'"\s]{3,}|[A-Za-z0-9_./-]+\.(?:csv|npz|json|yaml|yml|png|pdf|bag|npy|parquet|txt|md|tex))['"]"""
)
OUT_CALLS = {
    "to_csv",
    "savez",
    "savez_compressed",
    "savefig",
    "dump",
    "to_parquet",
    "save",
    "write_text",
    "imwrite",
    "to_json",
}


def load_roots(cfg_path: Path | None = None) -> dict:
    cfg = yaml.safe_load((cfg_path or paths.REPO / "config/scan_roots.yaml").read_text())
    root = paths.load()["phd_root"]
    for r in cfg["roots"]:
        r["path"] = r["path"].replace("${phd_root}", root)
    return cfg


def category(ext: str, cfg: dict) -> str | None:
    if ext in cfg["code_ext"]:
        return "code"
    if ext in cfg["doc_ext"]:
        return "doc"
    if ext in cfg["config_ext"]:
        return "config"
    return None


def py_facts(src: str) -> dict:
    try:
        t = ast.parse(src)
    except SyntaxError:
        return {"doc": "", "funcs": [], "imports": [], "args": [], "outs": [], "consts": []}
    funcs, imps, args, outs, consts = [], set(), [], set(), []
    for n in ast.walk(t):
        if (
            isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and n.col_offset == 0
        ):
            funcs.append(n.name)
        elif isinstance(n, ast.Import):
            imps |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            imps.add(n.module.split(".")[0])
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name == "add_argument" and n.args and isinstance(n.args[0], ast.Constant):
                args.append(str(n.args[0].value))
            if name in OUT_CALLS:
                outs.add(name)
        elif isinstance(n, ast.Assign) and n.col_offset == 0:
            for tg in n.targets:
                if (
                    isinstance(tg, ast.Name)
                    and tg.id.isupper()
                    and isinstance(n.value, ast.Constant)
                ):
                    consts.append(f"{tg.id}={str(n.value.value)[:30]}")
    return {
        "doc": (ast.get_docstring(t) or "").strip().replace("\n", " ")[:300],
        "funcs": funcs[:30],
        "imports": sorted(i for i in imps if i not in STD)[:25],
        "args": args[:20],
        "outs": sorted(outs),
        "consts": consts[:15],
    }


def ipynb_text(raw: str) -> str:
    try:
        nb = json.loads(raw)
        return "\n\n".join(
            "".join(c.get("source", []))
            for c in nb.get("cells", [])
            if c.get("cell_type") in ("code", "markdown")
        )
    except Exception:
        return raw


def read_text(p: Path, limit: int) -> str:
    b = p.read_bytes()[:limit]
    t = b.decode("utf-8", errors="replace")
    return ipynb_text(t) if p.suffix == ".ipynb" else t


def looks_like_data(txt: str) -> bool:
    sample = txt[:4000]
    return bool(sample) and sum(c.isdigit() or c in ",.;-\t " for c in sample) / len(sample) > 0.85


def git_info(root: Path) -> dict:
    if not (root / ".git").exists():
        return {}

    def g(*a):
        try:
            return subprocess.run(
                ["git", "-C", str(root), *a], capture_output=True, text=True, timeout=30
            ).stdout.strip()
        except Exception:
            return ""

    return {
        "head": g("rev-parse", "--short", "HEAD"),
        "branch": g("rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_files": len(g("status", "--short").splitlines()),
        "commits": g("rev-list", "--count", "HEAD"),
        "last_commit": g("log", "-1", "--format=%ad %s", "--date=short")[:120],
    }


def walk_root(r: dict, cfg: dict):
    base = Path(r["path"])
    skip = set(r.get("skip_subdirs", [])) | set(cfg["exclude_dirs"])
    lim = cfg["limits"]
    for dp, dn, fs in os.walk(base):
        dn[:] = sorted(d for d in dn if d not in skip)
        if any(x in dp + "/" for x in cfg["exclude_path_contains"]):
            continue
        for f in sorted(fs):
            p = Path(dp) / f
            cat = category(p.suffix.lower(), cfg)
            if cat is None:
                continue
            try:
                st = p.stat()
            except OSError:
                continue
            cap = lim[f"max_{cat}_bytes"]
            if st.st_size > cap and cat != "code":
                yield {
                    "label": r["label"],
                    "path": str(p),
                    "rel": str(p.relative_to(base)),
                    "cat": cat,
                    "size": st.st_size,
                    "mtime": date.fromtimestamp(st.st_mtime).isoformat(),
                    "sha": "",
                    "skipped": "too_large",
                    "facts": {},
                }
                continue
            try:
                txt = read_text(p, min(cap, 2_000_000))
                sha = hashlib.sha256(p.read_bytes()).hexdigest()
            except OSError:
                continue
            skipped = ""
            if cat == "doc" and looks_like_data(txt):
                skipped = "data_like"
            if st.st_size < 120 and cat != "config":
                skipped = skipped or "tiny"
            facts = {
                "lines": txt.count("\n") + 1,
                "abs_paths": len(re.findall(r"['\"]/(?:mnt|media|run|home)/", txt)),
                "todo_marks": len(re.findall(r"\b(?:TODO|FIXME|XXX|HACK)\b", txt)),
                "legacy_words": len(
                    re.findall(
                        r"\b(?:deprecated|superseded|obsolete|stale|legacy|old)\b", txt, re.I
                    )
                ),
            }
            if p.suffix == ".py":
                facts.update(py_facts(txt))
            if cat == "code":
                facts["path_literals"] = sorted(set(m.group(1) for m in PATH_RE.finditer(txt)))[:15]
            if cat == "config" and p.suffix == ".json":
                try:
                    j = json.loads(txt)
                    facts["json_keys"] = list(j)[:15] if isinstance(j, dict) else f"list[{len(j)}]"
                except Exception:
                    pass
            yield {
                "label": r["label"],
                "path": str(p),
                "rel": str(p.relative_to(base)),
                "cat": cat,
                "size": st.st_size,
                "mtime": date.fromtimestamp(st.st_mtime).isoformat(),
                "sha": sha,
                "skipped": skipped,
                "facts": facts,
            }
