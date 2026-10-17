"""Stage S8b table checker (gate: docs/gates/S8.md addendum). Parses LaTeX tables, maps each column to ledger ids (results/table_map.csv), classifies every data cell."""
import csv, re, sys
from pathlib import Path
from bridgedeck import paths

R = paths.REPO / "results"; PUB = Path("/mnt/phd_data/phd_master/05_publications")
FILES = {("measurement", "tab:bending"): "p02_measurement_revision_2026-10/manuscript/sections/04_results.tex", ("measurement", "tab:supp_s2"): "p02_measurement_revision_2026-10/manuscript/sections/04_results.tex",
         ("measurement", "tab:torsion"): "p02_measurement_revision_2026-10/manuscript/sections/04_results.tex", ("measurement", "tab:robustness"): "p02_measurement_revision_2026-10/manuscript/sections/04_results.tex"}
SENS = "p02_sensors_mdpi_revision_2026-10/paper2_sensors_synthesis.tex"
ledger = {r["id"]: float(r["value"]) for r in csv.DictReader(open(R / "ledger.csv"))}
cond_of = {int(re.search(r"_(\d+)rpm", r["condition"]).group(1)): r["condition"] for r in csv.DictReader(open(R / "s3_spectra_by_stream.csv"))}


def clean(c):
    c = re.sub(r"\\(textbf|texttt|textsuperscript|boldmath)\{([^{}]*)\}", r"\2", c)
    c = re.sub(r"\\(textbf|texttt|textsuperscript|boldmath)\{([^{}]*)\}", r"\2", c)
    c = c.replace("\\_", "_").replace("\\%", "%").replace("$\\times$", "").replace("{\\times}", "").replace("\\times", "").replace("$\\dagger$", "").replace("$\\ddagger$", "").replace("~", " ")
    return re.sub(r"\s+", " ", re.sub(r"\$|\\,", "", c)).strip()


def tables(text):
    out = {}
    for blk in re.finditer(r"\\begin\{table\}.*?\\end\{table\}", text, re.S):
        b = blk.group(0); lab = re.search(r"\\label\{(tab:[^}]*)\}", b)
        if not lab:
            continue
        for k, t in enumerate(re.finditer(r"\\begin\{(tabularx?)\}(.*?)\\end\{\1\}", b, re.S)):
            body = t.group(2)
            body = body[body.index("\\toprule") + 8:] if "\\toprule" in body else body
            body = body.split("\\bottomrule")[0]
            rows = []
            for r in re.split(r"\\\\(?:\[[^\]]*\])?", body):
                r = re.sub(r"\\(midrule|toprule|hline)", "", r).strip()
                if r:
                    rows.append([clean(c) for c in re.split(r"(?<!\\)&", r)])
            out[(lab.group(1), k)] = rows
    return out


def nums(cell):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", cell)], re.findall(r"-?\d+(?:\.\d+)?", cell)


def value(expr, rpm):
    kind, rest = expr.split(":", 1)
    fill = lambda t: t.format(rpm=rpm, cond=cond_of.get(rpm, "NA"))
    if kind == "id":
        return ledger.get(fill(rest), None), fill(rest)
    if kind == "ratio":
        a, b = rest.split("/")
        va, vb = ledger.get(fill(a)), ledger.get(fill(b))
        return (va / vb if va is not None and vb else None), fill(rest)
    return None, rest


tabs = {}
for ms in ("measurement", "sensors"):
    for (m, lab), f in {**FILES, **{("sensors", l): SENS for l in ("tab:tb4-posthoc-reference", "tab:rpm-sweep", "tab:tb3-cross-view", "tab:timebase")}}.items():
        if m == ms and (ms, f) not in tabs:
            tabs[(ms, f)] = tables((PUB / f).read_text())
amap = list(csv.DictReader(open(R / "table_map.csv")))
exp = list(csv.DictReader(open(R / "table_expected_rows.csv")))
report, s1 = [], []
for e in exp:
    f = FILES.get((e["manuscript"], e["label"]), SENS)
    rows = tabs[(e["manuscript"], f)][(e["label"], int(e["tab_idx"]))]
    key = int(e["rpm_col"])
    if e["key_kind"] == "rpm":  # data rows: the key column starts with an integer
        data = [r for r in rows if len(r) > key and r[key].split() and re.fullmatch(r"\d+", r[key].split()[0])]
    else:  # rows keyed by their first-cell label: every row after the header row with a non-empty label
        data = [r for r in rows[1:] if r[0]]
    ok = len(data) == int(e["expected_rows"])
    s1.append((e["manuscript"], e["label"], e["tab_idx"], len(data), e["expected_rows"], ok))
    for r in data:
        rk = int(r[key].split()[0]) if e["key_kind"] == "rpm" else None
        for mp in [m for m in amap if m["manuscript"] == e["manuscript"] and m["label"] == e["label"] and int(m["tab_idx"]) == int(e["tab_idx"])]:
            if mp["key_kind"] == "label" and mp["row_label"] != r[0]:
                continue
            ci = int(mp["col_idx"])
            if ci >= len(r):
                continue
            vals, toks = nums(r[ci]); p = int(mp["part"])
            if p >= len(vals):
                report.append(dict(**{k: mp[k] for k in ("manuscript", "label")}, row=r[0] if rk is None else rk, col=ci, part=p, printed="", rebuilt="", status="CELL_NOT_NUMERIC", rel_diff="", id_or_reason=mp["expr"], note=mp["note"]))
                continue
            tok = toks[p]; d = len(tok.split(".")[1]) if "." in tok else 0
            v, ident = value(mp["expr"], rk)
            if mp["expr"].startswith("unmapped"):
                st, rb, rd = "UNMAPPED", "", ""
            elif v is None:
                st, rb, rd = "NOT_IN_LEDGER", "", ""  # e.g. 320 RPM streams the pipeline rejected
            else:
                st = "AGREE" if round(v, d) == float(tok) else ("CLOSE" if abs(v - float(tok)) <= 3 * 10 ** -d else "DIFFER"); rb = v; rd = (v - float(tok)) / float(tok) if float(tok) else ""
            report.append(dict(manuscript=mp["manuscript"], label=mp["label"], row=r[0] if rk is None else rk, col=ci, part=p, printed=tok, rebuilt=rb, status=st, rel_diff=rd, id_or_reason=ident, note=mp["note"]))
tmpl_ok = all(any(r["status"] in ("AGREE", "CLOSE", "DIFFER") for r in report if (r["label"], r["col"], r["part"]) == (m["label"], int(m["col_idx"]), int(m["part"]))) or m["expr"].startswith("unmapped") for m in amap)
miss = [m for m in amap if not tmpl_ok]
with open(R / "table_check_report.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, list(report[0])); w.writeheader(); w.writerows(report)
lines = ["# S8b table check summary", "", "| manuscript | table | expected rows | found | OK |", "|---|---|---|---|---|"] + [f"| {a} | {b}#{c} | {e} | {d} | {'yes' if ok else 'NO'} |" for a, b, c, d, e, ok in s1]
lines += ["", "## Cells by table and column (AGREE = equal at printed precision / CLOSE = within 3 units of the last printed digit / DIFFER / UNMAPPED / NOT_IN_LEDGER); median |relative difference| of DIFFER cells", "", "| table | col.part | AGREE | CLOSE | DIFFER | UNMAPPED | NOT_IN_LEDGER | median abs rel diff of DIFFER |", "|---|---|---|---|---|---|---|---|"]
import statistics
keys = sorted({(r["label"], r["col"], r["part"]) for r in report})
for k in keys:
    g = [r for r in report if (r["label"], r["col"], r["part"]) == k]; dd = [abs(float(r["rel_diff"])) for r in g if r["status"] == "DIFFER" and r["rel_diff"] != ""]
    cnt = " | ".join(str(sum(r["status"] == st for r in g)) for st in ("AGREE", "CLOSE", "DIFFER", "UNMAPPED", "NOT_IN_LEDGER"))
    lines.append(f"| {k[0]} | {k[1]}.{k[2]} | {cnt} | {statistics.median(dd):.3f} |" if dd else f"| {k[0]} | {k[1]}.{k[2]} | {cnt} | |")
Path(R / "table_check_summary.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines[:4 + len(s1)])); print("\n".join(lines[4 + len(s1):]))
print("S1 all tables expected rows:", all(x[-1] for x in s1), "| S2 map templates that resolve to no ledger value:", len(miss))
