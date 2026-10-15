"""Static inventory of reference code (read-only). Per file: size, docstring, functions, third-party imports,
CLI args, path-like string literals, output calls, UPPER_CASE numeric constants. No code is executed."""
import ast, csv, re, sys, os, hashlib
from pathlib import Path

STD = set(sys.stdlib_module_names)
PATH_RE = re.compile(r"""['"](/(?:mnt|media|run|home|tmp)[^'"\s]{3,}|[A-Za-z0-9_./-]+\.(?:csv|npz|json|yaml|yml|png|pdf|bag|npy|parquet|txt|md))['"]""")
OUT_CALLS = ("to_csv", "savez", "savez_compressed", "savefig", "dump", "to_parquet", "save", "write_text", "imwrite")

def analyse_py(src: str):
    try: t = ast.parse(src)
    except SyntaxError as e: return dict(doc="(syntax error)", funcs="", imports="", args="", consts="", outs="")
    doc = (ast.get_docstring(t) or "").strip().replace("\n", " ")[:260]
    funcs, imps, args, consts, outs = [], set(), [], [], set()
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.col_offset == 0: funcs.append(n.name)
        elif isinstance(n, ast.Import): imps |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0: imps.add(n.module.split(".")[0])
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name == "add_argument" and n.args and isinstance(n.args[0], ast.Constant): args.append(str(n.args[0].value))
            if name in OUT_CALLS: outs.add(name)
        elif isinstance(n, ast.Assign) and n.col_offset == 0:
            for tg in n.targets:
                if isinstance(tg, ast.Name) and tg.id.isupper() and isinstance(n.value, (ast.Constant, ast.Tuple, ast.List)):
                    try: consts.append(f"{tg.id}={ast.unparse(n.value)[:40]}")
                    except Exception: pass
    return dict(doc=doc, funcs=" ".join(funcs[:25]), imports=" ".join(sorted(i for i in imps if i not in STD)),
                args=" ".join(args[:20]), consts="; ".join(consts[:12]), outs=" ".join(sorted(outs)))

def analyse_other(src: str, ext: str):
    if ext == ".m":
        m = re.search(r"^\s*%\s*(.+)$", src, re.M); funcs = re.findall(r"^\s*function\s+.*?(\w+)\s*\(", src, re.M)
        return dict(doc=(m.group(1) if m else "")[:260], funcs=" ".join(funcs[:15]), imports="", args="", consts="", outs="")
    m = re.search(r"^#(?!!)\s*(.+)$", src, re.M)
    return dict(doc=(m.group(1) if m else "")[:260], funcs="", imports="", args="", consts="", outs="")

def main(tree, out_csv, label):
    rows = []
    for dp, dn, fs in os.walk(tree):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", ".venv", "venv", "venv310", "node_modules", "build", "devel", "install", ".ruff_cache")]
        for f in sorted(fs):
            ext = Path(f).suffix
            if ext not in (".py", ".m", ".sh"): continue
            p = Path(dp) / f
            try: src = p.read_text(errors="replace")
            except OSError: continue
            a = analyse_py(src) if ext == ".py" else analyse_other(src, ext)
            paths = sorted(set(m.group(1) for m in PATH_RE.finditer(src)))[:10]
            rows.append(dict(tree=label, rel=str(p.relative_to(tree)), loc=src.count("\n") + 1, sha=hashlib.sha256(src.encode(errors="replace")).hexdigest()[:10],
                             mtime=__import__("datetime").date.fromtimestamp(p.stat().st_mtime).isoformat(), **a, path_literals=" | ".join(paths)))
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(label, len(rows), "files", sum(r["loc"] for r in rows), "lines")

if __name__ == "__main__":
    main(Path(sys.argv[1]), sys.argv[2], sys.argv[3])
