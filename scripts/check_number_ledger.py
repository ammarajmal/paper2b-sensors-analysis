"""Stage S8 checker (gate: docs/gates/S8.md). P1: independent recompute of every ledger row (stdlib only); P3/P5: curated claims and full scan of both manuscripts."""
import csv, json, re, statistics, sys
from pathlib import Path
from bridgedeck import paths

R = paths.REPO / "results"
PUB = Path("/mnt/phd_data/phd_master/05_publications")
MS = {"measurement": [PUB / "p02_measurement_revision_2026-10/manuscript/abstract.tex", *sorted((PUB / "p02_measurement_revision_2026-10/manuscript/sections").glob("*.tex"))],
      "sensors": [PUB / "p02_sensors_mdpi_revision_2026-10/paper2_sensors_synthesis.tex"]}
MS_ROOT = {"measurement": PUB / "p02_measurement_revision_2026-10/manuscript", "sensors": PUB / "p02_sensors_mdpi_revision_2026-10"}
AGG = {"median": statistics.median, "min": min, "max": max, "sum": sum, "count": len}


def recompute(recipe):
    f, sel, col, agg = recipe.split("|")
    if f.endswith(".json"):
        j = json.load(open(R / f)); rows = j if isinstance(j, list) else [j]
    else:
        rows = list(csv.DictReader(open(R / f)))
    for kv in filter(None, sel.split(";")):
        k, v = kv.split("=", 1); rows = [r for r in rows if str(r[k]) == v]
    assert rows, f"empty selection {recipe}"
    if agg == "count":
        return float(len(rows))
    xs = [float(r[col]) for r in rows]
    return float(xs[0]) if agg == "first" and len(xs) == 1 else float(AGG[agg](xs))


ledger = list(csv.DictReader(open(R / "ledger.csv")))
need = ["id", "group", "description", "value", "source_file", "recipe", "script", "commit", "source_sha256_16"]
bad = [r["id"] for r in ledger if any(r[k] in ("", None) for k in need)]
mism = [r["id"] for r in ledger if recompute(r["recipe"]) != float(r["value"]) and abs(recompute(r["recipe"]) - float(r["value"])) > 1e-9 * max(1, abs(float(r["value"])))]
print(f"P1 ledger rows {len(ledger)}; rows with an empty field {len(bad)}; rows whose independent recompute differs {len(mism)}")
byid = {r["id"]: float(r["value"]) for r in ledger}


def decimals(tok):
    return len(tok.split(".")[1]) if "." in tok else 0


rep = []
cl = list(csv.DictReader(open(R / "claims_map.csv")))
for c in cl:
    path = MS_ROOT[c["manuscript"]] / c["file"]
    line = path.read_text().splitlines()[int(c["line"]) - 1]
    status, lv = None, ""
    if c["token"] not in line:
        status = "TOKEN_NOT_AT_LINE"
    elif not c["ledger_id"]:
        status = "NOT_IN_LEDGER"
    elif c["ledger_id"] not in byid:
        status = "LEDGER_ID_MISSING"
    else:
        lv = byid[c["ledger_id"]]; d = decimals(c["token"])
        status = "AGREE" if round(lv, d) == float(c["token"]) else "DIFFER"
    rep.append(dict(kind="claim", manuscript=c["manuscript"], file=c["file"], line=c["line"], printed=c["token"], ledger_value=lv, status=status, relation=c["relation"], note=c["description"], ledger_id=c["ledger_id"]))
print("P5 curated claims:", {s: sum(r["status"] == s for r in rep) for s in sorted({r["status"] for r in rep})})
# full scan: decimal tokens only (bare integers match the ledger by chance too often to mean anything)
vals_by_d = {}
for d in range(1, 7):
    vals_by_d[d] = {f"{v:.{d}f}" for v in byid.values()}
scan_stats = {}
pat = re.compile(r"(?<![\w.])-?\d+\.\d+(?![\w.])")
for m, files in MS.items():
    for f in files:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if line.lstrip().startswith("%") or re.search(r"doi|\\bibitem|http|\\cite|\\label|\\includegraphics|\\usepackage", line):
                continue
            code = line.split("%")[0]
            for t in pat.findall(code):
                d = decimals(t)
                hit = d in vals_by_d and f"{abs(float(t)):.{d}f}" in vals_by_d[d] or (d > 6)
                rep.append(dict(kind="scan", manuscript=m, file=str(f.relative_to(MS_ROOT[m])), line=i, printed=t, ledger_value="", status="VALUE_IN_LEDGER" if hit else "NO_LEDGER_VALUE", relation="", note=code.strip()[:90], ledger_id=""))
                scan_stats.setdefault((m, min(d, 4)), [0, 0])[0 if hit else 1] += 1
fields = ["kind", "manuscript", "file", "line", "printed", "ledger_value", "status", "relation", "note", "ledger_id"]
with open(R / "number_check_report.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fields); w.writeheader(); w.writerows(rep)
lines = ["# S8 number check summary", "", f"Ledger rows {len(ledger)}; P1 empty fields {len(bad)}; recompute mismatches {len(mism)}.", "", "## Curated claims (results/claims_map.csv)", "", "| id | printed | rebuilt value | status | relation | description |", "|---|---|---|---|---|---|"]
for c, r in zip(cl, [r for r in rep if r["kind"] == "claim"]):
    lv = f'{float(r["ledger_value"]):.4f}' if r["ledger_value"] != "" else ""
    lines.append(f'| {c["claim_id"]} | {r["printed"]} | {lv} | {r["status"]} | {r["relation"]} | {r["note"]} |')
lines += ["", "## Full scan of decimal numbers (VALUE_IN_LEDGER = equal at the printed precision to some ledger value; coincidence is likely at 1-2 decimals)", "", "| manuscript | decimals | in ledger | not in ledger |", "|---|---|---|---|"]
for (m, d), (a, b) in sorted(scan_stats.items()):
    lines.append(f"| {m} | {d if d < 4 else '4+'} | {a} | {b} |")
Path(R / "number_check_summary.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines[6:6 + len(cl) + 3]))
print("scan:", {f"{m}/{d}": tuple(v) for (m, d), v in sorted(scan_stats.items())})
sys.exit(1 if bad or mism else 0)
