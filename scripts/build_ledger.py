"""Stage S8: build results/ledger.csv. Every row is read from a results file by a recipe (file|selector|column|aggregate); nothing is typed in.
Recipe grammar (also evaluated independently by check_number_ledger.py): path|k1=v1;k2=v2|column|agg, agg in first, median, min, max, count, sum."""
import hashlib, json, subprocess
import numpy as np, pandas as pd
from bridgedeck import paths

R = paths.REPO / "results"
SCRIPT = {  # producing script per results file
    "reference_frequencies_free_vibration.json": "scripts/run_s5a.py", "s1_census_wtt_main.csv": "bridgedeck census", "gate_S2_full.json": "bridgedeck gate-s2",
    "s2c_summary.json": "scripts/run_s2c.py", "s3_spectra_by_stream.csv": "scripts/run_s3.py", "laser_y2025_by_condition.csv": "scripts/run_s5a.py",
    "laser_y2024_by_condition.csv": "scripts/run_s5a.py", "s6_metrics.csv": "scripts/run_s6.py", "s6_closeness.csv": "scripts/run_s6.py",
    "s6b_variant_metrics.csv": "scripts/run_s6b.py", "s6b_variant_closeness.csv": "scripts/run_s6b.py", "s7_budget_by_condition.csv": "scripts/run_s7.py", "paperset_check.csv": "scripts/run_paperset_check.py", "paperset_intervals.csv": "scripts/run_paperset_intervals.py", "s6_matched_pairs.csv": "scripts/run_s6.py",
}
commit = subprocess.check_output(["git", "-C", str(paths.REPO), "rev-parse", "--short", "HEAD"], text=True).strip()
rows, cache = [], {}


def sha(f):
    return hashlib.sha256((R / f).read_bytes()).hexdigest()[:16]


def load(f):
    if f not in cache:
        if f.endswith(".csv"):
            cache[f] = pd.read_csv(R / f)
        else:
            j = json.load(open(R / f)); cache[f] = pd.DataFrame(j) if isinstance(j, list) else j
    return cache[f]


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def sel_df(df, sel):
    """Selector grammar: terms joined by ';', each k=v, k!=v or k>v; '=' and '!=' compare numerically when both sides parse as numbers."""
    for kv in filter(None, sel.split(";")):
        if "!=" in kv:
            k, v = kv.split("!=", 1); op = "ne"
        elif ">" in kv:
            k, v = kv.split(">", 1); op = "gt"
        else:
            k, v = kv.split("=", 1); op = "eq"
        col = df[k]
        if op == "gt":
            df = df[col.astype(float) > float(v)]
        else:
            same = (col.astype(float) == float(v)) if _num(v) is not None and pd.api.types.is_numeric_dtype(col) else (col.astype(str) == v)
            df = df[same if op == "eq" else ~same]
    return df


def add(group, desc, f, sel, col, agg, unit="", pop=""):
    d = load(f)
    if isinstance(d, dict):
        val = d[col]
    else:
        sub = sel_df(d, sel)
        if len(sub) == 0 and agg == "count" and ">" in sel:  # a threshold count may be 0, but only if the selection without the threshold term is not empty
            assert len(sel_df(d, ";".join(t for t in sel.split(";") if ">" not in t or "!=" in t))) > 0, f"empty selection: {f} {sel}"
            val = 0.0
            return rows.append(dict(id=f"{group}.{f.rsplit('.',1)[0]}.{sel.replace('!=','-NOT-').replace('>','-GT-').replace('=','-').replace(';','.')}.{col}.{agg}", group=group, description=desc, value=val, unit=unit, population=pop or sel.replace(";", " "),
                                    source_file=f"results/{f}", recipe=f"{f}|{sel}|{col}|{agg}", script=SCRIPT.get(f, "scripts/open_issues_check.py"), commit=commit, source_sha256_16=sha(f)))
        assert len(sub) > 0, f"empty selection: {f} {sel}"
        x = sub[col] if agg != "count" else sub.iloc[:, 0]
        if agg == "first":
            assert len(x) == 1, (f, sel, col, len(x)); val = x.iloc[0]
        else:
            val = getattr(x, agg)() if agg != "count" else len(x)
    if isinstance(val, (bool, np.bool_)) or val is None or (isinstance(val, float) and not np.isfinite(val)):
        return
    sel_s = sel.replace(";", " ")
    rows.append(dict(id=f"{group}.{f.rsplit('.',1)[0]}.{sel_s.replace('!=','-NOT-').replace('>','-GT-').replace('=','-').replace(' ','.')}.{col}.{agg}".replace("..", "."), group=group, description=desc, value=float(val), unit=unit,
                     population=pop or sel_s, source_file=f"results/{f}", recipe=f"{f}|{sel}|{col}|{agg}", script=SCRIPT.get(f, "scripts/open_issues_check.py"), commit=commit, source_sha256_16=sha(f)))


# reference frequencies
for s in ("y2025", "y2024"):
    for m in ("bending", "torsion"):
        for c, u in (("f_fit_hz", "Hz"), ("f_fit_lo", "Hz"), ("f_fit_hi", "Hz"), ("f_fft_hz", "Hz"), ("zeta", "-")):
            add("REF", f"free-decay {m} {c} (damped-sinusoid fit)", "reference_frequencies_free_vibration.json", f"session={s};mode={m}", c, "first", u)
# timing census
for cam in ("cam1", "cam2", "cam3"):
    add("TIM", f"median header frame rate {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "rate_hdr_hz", "median", "Hz")
    add("TIM", f"median of per-bag mean frame rate {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "rate_mean_hz", "median", "Hz")
    add("TIM", f"minimum per-bag mean frame rate {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "rate_mean_hz", "min", "Hz")
    add("TIM", f"maximum per-bag mean frame rate {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "rate_mean_hz", "max", "Hz")
    add("TIM", f"median record-to-header latency {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "lat_mean_ms", "median", "ms")
    add("TIM", f"bags {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "bag", "count", "bags")
    add("TIM", f"consecutive duplicate frames summed over bags {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "dup_consecutive_payload", "sum", "frames")
    add("TIM", f"largest frame interval {cam}", "s1_census_wtt_main.csv", f"cam=sony_{cam}", "dt_max_ms", "max", "ms")
# detection gate
for k in ("frames_new", "detected_flag_equal_pct", "both_detected", "corner_diff_median", "corner_diff_p99", "corner_diff_max"):
    add("DET", f"S2 versus frozen detections: {k}", "gate_S2_full.json", "", k, "first")
add("DET", "S2c R2_all", "s2c_summary.json", "", "R2_all", "first")
# spectra
s3 = load("s3_spectra_by_stream.csv")
for _, r in s3.iterrows():
    add("SPEC", "refined dominant line of the stream", "s3_spectra_by_stream.csv", f"condition={r.condition};camera={r.camera}", "f_refined", "first", "Hz")
# laser per-condition statistics
for s in ("2025", "2024"):
    f = f"laser_y{s}_by_condition.csv"
    for rpm in load(f).rpm.unique():
        for c, u in (("bending_avg_mm_rms", "mm"), ("torsion_proxy_mm_rms", "mm"), ("heave_mm_rms", "mm"), ("pitch_rad_rms", "rad"), ("wind_measured_ms", "m/s")):
            add("LAS", f"laser {s} {c}", f, f"rpm={rpm}", c, "first", u)
# S6 headline and full metrics
for _, r in load("s6_metrics.csv")[["session", "arm", "quantity", "variant", "rule", "scope"]].iterrows():
    sel = ";".join(f"{k}={r[k]}" for k in ("session", "arm", "quantity", "variant", "rule", "scope"))
    for c in ("n", "pearson_log", "spearman", "median_ratio", "median_ratio_lo", "median_ratio_hi", "E_log10", "deming_slope_log"):
        add("S6", f"camera versus laser {c}", "s6_metrics.csv", sel, c, "first")
for _, r in load("s6_closeness.csv")[["arm", "quantity", "variant", "rule"]].iterrows():
    sel = ";".join(f"{k}={r[k]}" for k in ("arm", "quantity", "variant", "rule"))
    for c in ("n", "E_2025", "E_2024", "dE", "dE_lo", "dE_hi", "P_2025_closer"):
        add("S6", f"2025 versus 2024 closeness {c}", "s6_closeness.csv", sel, c, "first")
# S6b exploratory
for _, r in load("s6b_variant_metrics.csv")[["combo", "session", "quantity", "rule"]].drop_duplicates().iterrows():
    sel = ";".join(f"{k}={r[k]}" for k in ("combo", "session", "quantity", "rule"))
    for c in ("median_ratio", "E_log10"):
        add("EXPL_S6b", f"exploratory variant {c}", "s6b_variant_metrics.csv", sel, c, "first")
for _, r in load("s6b_variant_closeness.csv")[["combo", "quantity", "rule"]].iterrows():
    sel = ";".join(f"{k}={r[k]}" for k in ("combo", "quantity", "rule"))
    for c in ("E_2025", "E_2024", "dE", "P_2025_closer"):
        add("EXPL_S6b", f"exploratory variant closeness {c}", "s6b_variant_closeness.csv", sel, c, "first")
# S7 aggregates
for q in ("Q1", "Q2"):
    for s in ("y2025", "y2024"):
        for ra in ("True", "False"):
            base = f"quantity={q};session={s};rule_a={ra}"
            add("S7", "conditions in the set", "s7_budget_by_condition.csv", base, "rpm", "count", "conditions")
            for c in ("u_C", "u_L", "u_R", "C6", "L1", "L2"):
                add("S7", f"median {c}", "s7_budget_by_condition.csv", base, c, "median")
            add("S7", "conditions covered at k=2", "s7_budget_by_condition.csv", base + ";covered_k2=True", "rpm", "count", "conditions")
# S8a exploratory reproduction on the manuscripts' own 16-condition set
for _, r in load("paperset_check.csv")[["scope", "quantity"]].iterrows():
    for c in ("n", "pearson_lin", "spearman", "mean_ratio", "rmse_mm", "mae_mm", "slope_through_origin", "slope_ols"):
        add("EXPL_PAPERSET", f"rebuilt pipeline on manuscript set, {c}", "paperset_check.csv", f"scope={r.scope};quantity={r.quantity}", c, "first")
# S8b: per-RPM rows for the table checks, stream spectra details, timebase shifts, intervals
for rpm in sorted(load("s6_matched_pairs.csv").query("arm == 'A' and rpm < 320").rpm.astype(int).unique()):
    for c, u in (("cam_legacy_bend_rms", "mm"), ("cam_legacy_tors_rms", "mm"), ("cam_legacy_bend_peak", "mm"), ("cam_legacy_tors_peak", "mm"), ("cam_dom_hz", "Hz")):
        add("S8TAB", f"camera {c} at {rpm} RPM", "s6_matched_pairs.csv", f"arm=A;session=y2024;rpm={rpm}", c, "first", u)
    for c in ("bending_avg_mm_peak", "torsion_proxy_mm_peak", "bending_dom_hz", "torsion_dom_hz"):
        for s_ in ("2025", "2024"):
            if (load(f"laser_y{s_}_by_condition.csv").rpm.astype(int) == rpm).any():
                add("S8TAB", f"laser {s_} {c} at {rpm} RPM", f"laser_y{s_}_by_condition.csv", f"rpm={rpm}", c, "first")
for _, r in s3.iterrows():
    for c in ("f_E0", "T", "RI"):
        add("SPEC", f"stream {c}", "s3_spectra_by_stream.csv", f"condition={r.condition};camera={r.camera}", c, "first")
for c in ("d_E1_RI", "d_hdr_RI", "d_i60_RI", "d_nom_RI"):
    base = "condition!=e20_320rpm"
    add("TBASE", f"max shift in Rayleigh intervals, admitted streams, {c}", "s3_spectra_by_stream.csv", base, c, "max")
    add("TBASE", f"median shift, admitted streams, {c}", "s3_spectra_by_stream.csv", base, c, "median")
    add("TBASE", f"streams with shift > 0.1, {c}", "s3_spectra_by_stream.csv", base + f";{c}>0.1", c, "count", "streams")
add("TBASE", "admitted streams", "s3_spectra_by_stream.csv", "condition!=e20_320rpm", "RI", "count", "streams")
for _, r in load("paperset_intervals.csv")[["quantity", "stat"]].iterrows():
    for c in ("estimate", "ci_lo", "ci_hi"):
        add("EXPL_PAPERSET", f"paperset16 {c}", "paperset_intervals.csv", f"scope=paperset16;quantity={r.quantity};stat={r.stat}", c, "first")
out = pd.DataFrame(rows)
assert out.id.is_unique, out.id[out.id.duplicated()].head()
assert out.notna().all().all()
out.to_csv(R / "ledger.csv", index=False, float_format="%.12g")
print(len(out), "rows;", out.group.value_counts().to_dict(), "commit", commit)
