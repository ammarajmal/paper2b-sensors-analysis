"""Per-camera RMS for Paper 2B, computed from the frame-level S4 Parquet only.

Run from the repo root:  .venv/bin/python analysis/paper2b/per_camera_rms/run_per_camera_rms.py
Writes only into analysis/paper2b/per_camera_rms/. The pooled RMS table is never read.
Stage order: FULL results (all admitted streams, total mean-removed RMS) are computed and written
before SENSITIVITY results (detrend, exclusions, bootstrap, leave-one-condition-out).
"""

import csv
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

T0 = time.time()
REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
AUDIT = REPO / "analysis/paper2b/per_camera_rms_audit"
PARQUET = REPO / "outputs/s4_pose_channels_by_frame.parquet"
INTR = REPO / "config/intrinsics_bag.json"
S4CSV = REPO / "results/s4_pose_by_stream.csv"  # reproducibility check only, never a value source
LASER = {
    "y2025": REPO / "results/laser_y2025_by_condition.csv",
    "y2024": REPO / "results/laser_y2024_by_condition.csv",
}
CAMS = ["cam1", "cam2", "cam3"]
QTY = {"H1_y_mm": "mm", "H2_roll_rad": "rad"}
SCALE_REL = 0.025  # +/-2.5% tag-size scale uncertainty: mm quantities only
LEVER_MM = 125.0  # approximate cam1/cam2 marker offset from rotation axis (design review)
BOUNDARY = {"e4_60rpm", "e6_80rpm"}
FLOOR_GATE = 5.0
SEED, NBOOT = 0, 10000
SIGNAL_DEF = {
    "H1_y_mm": "vertical (image-y) displacement of rectified tag-corner centroid, mm in tag plane, minus stream median (pose.py:175-190)",
    "H2_roll_rad": "unwrapped in-plane edge angle of rectified corners, rad, minus stream median (pose.py:40-42,189)",
}
AGG = {
    "total": "np.nanstd ddof=0 about stream mean; full band to camera Nyquist (~30 Hz); no detrend",
    "detrended": "np.nanstd ddof=0 of residual after least-squares linear fit vs t_s; SENSITIVITY quantity",
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rel(p):
    return str(Path(p).relative_to(REPO))


def rms0(y):
    return float(np.nanstd(y))


def rms_detr(t, y):
    m = np.isfinite(t) & np.isfinite(y)
    c = np.polyfit(t[m], y[m], 1)
    return float(np.std(y[m] - np.polyval(c, t[m])))


def rpm_of(cond):
    return int(cond.split("_")[1].replace("rpm", ""))


# ---------- provenance ----------
src_hash = sha(PARQUET)
registry = {
    ln.split()[1]: ln.split()[0]
    for ln in (AUDIT / "PER_CAMERA_RMS_SOURCE_HASHES.sha256").read_text().splitlines()
    if ln.strip()
}
registry_ok = registry.get("outputs/s4_pose_channels_by_frame.parquet") == src_hash
assert registry_ok, "parquet hash differs from approved registry"
intr_hash = sha(INTR)
intr = json.loads(INTR.read_text())
head = subprocess.run(
    ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
).stdout.strip()

d = pd.read_parquet(
    PARQUET, columns=["condition", "camera", "frame_idx", "t_s", "H1_y_mm", "H2_roll_rad"]
)
d = d.sort_values(["condition", "camera", "frame_idx"], kind="stable")
conds = sorted(d.condition.unique(), key=rpm_of)
streams = d.groupby(["condition", "camera"]).ngroups
assert streams == 61 and len(conds) == 21

# ---------- FULL stage: per-stream values ----------
rows, rec = [], {}
for (cond, cam), g in d.groupby(["condition", "camera"], sort=False):
    t = g.t_s.to_numpy()
    rec[(cond, cam)] = dict(
        n_total=len(g), dur=float(t.max() - t.min()), fs=(len(g) - 1) / float(t.max() - t.min())
    )
    diag = cond.startswith("e20")
    adm = (
        "diagnostic_only"
        if diag
        else ("admitted_noise_floor_reference" if cond.startswith("e0_") else "admitted")
    )
    flags = []
    if cond in BOUNDARY:
        flags.append("regime_boundary_60_80_sensitivity")
    if diag:
        flags.append("320rpm_cam3_diagnostic_only_IPPE_ambiguity_not_used_for_H1_H2")
    for q, unit in QTY.items():
        y = g[q].to_numpy()
        for agg, val in (("total", rms0(y)), ("detrended", rms_detr(t, y))):
            rows.append(
                dict(
                    condition=cond,
                    rpm=rpm_of(cond),
                    camera=cam,
                    quantity=f"{q}_rms_total_meanremoved"
                    if agg == "total"
                    else f"{q}_rms_linear_detrended",
                    rms_value=val,
                    unit=unit,
                    n_total=len(g),
                    n_valid=int(np.isfinite(y).sum()),
                    signal_column=q,
                    signal_definition=SIGNAL_DEF[q],
                    aggregation_method=AGG[agg],
                    admissibility=adm,
                    calibration_source=f"config/intrinsics_bag.json[{cam}] K+D from e0_0rpm_run1.bag camera_info; tag side 20.0 mm (pose.py:16)",
                    calibration_sha256=intr_hash,
                    source_file=rel(PARQUET),
                    source_sha256=src_hash,
                    scale_rel_unc=SCALE_REL if unit == "mm" else np.nan,
                    rms_scale_lo=val * (1 - SCALE_REL) if unit == "mm" else np.nan,
                    rms_scale_hi=val * (1 + SCALE_REL) if unit == "mm" else np.nan,
                    flags=";".join(flags),
                )
            )
V = pd.DataFrame(rows)

# noise floors (e0_0rpm, per camera) and ratios for every condition
ratio_rows = []
for agg in ("total_meanremoved", "linear_detrended"):
    for q, unit in QTY.items():
        name = f"{q}_rms_{agg}"
        for _, r in V[V.quantity == name].iterrows():
            fl = V[
                (V.quantity == name) & (V.condition == "e0_0rpm") & (V.camera == r.camera)
            ].rms_value.iloc[0]
            f = r["flags"].split(";") if r["flags"] else []
            ratio = r.rms_value / fl
            if r.condition != "e0_0rpm" and ratio < FLOOR_GATE:
                f.append(f"below_{FLOOR_GATE:g}x_camera_floor")
            ratio_rows.append(
                {
                    **r.to_dict(),
                    "quantity": f"{name}_noise_floor_ratio",
                    "rms_value": ratio,
                    "unit": "ratio",
                    "aggregation_method": f"{r.aggregation_method} | divided by same-camera e0_0rpm value ({fl:.6g} {unit}); scale cancels",
                    "scale_rel_unc": np.nan,
                    "rms_scale_lo": np.nan,
                    "rms_scale_hi": np.nan,
                    "flags": ";".join(f),
                }
            )
V = pd.concat([V, pd.DataFrame(ratio_rows)], ignore_index=True)
cols = [
    "condition",
    "rpm",
    "camera",
    "quantity",
    "rms_value",
    "unit",
    "n_total",
    "n_valid",
    "signal_column",
    "signal_definition",
    "aggregation_method",
    "admissibility",
    "calibration_source",
    "calibration_sha256",
    "source_file",
    "source_sha256",
    "scale_rel_unc",
    "rms_scale_lo",
    "rms_scale_hi",
    "flags",
]
V = V[cols]
V.to_csv(OUT / "PER_CAMERA_RMS_VALUES.csv", index=False, float_format="%.10g")

# reproducibility vs existing s4 table (check only)
s4 = pd.read_csv(S4CSV)
chk = []
for q in QTY:
    a = V[V.quantity == f"{q}_rms_total_meanremoved"].merge(
        s4[["condition", "camera", f"{q}_rms"]], on=["condition", "camera"]
    )
    chk.append(((a.rms_value - a[f"{q}_rms"]).abs().max(), len(a)))
max_diff = max(c[0] for c in chk)
assert all(c[1] == 61 for c in chk) and max_diff < 1e-12

W = V[V.quantity.str.endswith("rms_total_meanremoved")].pivot_table(
    index=["condition", "rpm"], columns=["camera", "signal_column"], values="rms_value"
)
W = W.reset_index().sort_values("rpm")


def val(cond, cam, q, kind="total_meanremoved"):
    return V[
        (V.condition == cond) & (V.camera == cam) & (V.quantity == f"{q}_rms_{kind}")
    ].rms_value.iloc[0]


# laser
L = {}
for s, p in LASER.items():
    las = pd.read_csv(p)
    las["condition"] = None
    las = las[las.rpm.isin([rpm_of(c) for c in conds[1:]])].copy()
    las["condition"] = las.rpm.map({rpm_of(c): c for c in conds})
    L[s] = las.set_index("condition")
adm_conds = [c for c in conds if c != "e0_0rpm"]  # e1..e19 admitted + e20 diagnostic handled below
primary = [c for c in conds if not c.startswith("e0_") and not c.startswith("e20")]  # 19 conditions

# ---------- comparison rows ----------
CR = []


def crow(
    stage,
    comp,
    cond,
    quantity,
    unit,
    a_label,
    a,
    b_label,
    b,
    flags="",
    notes="",
    scale_a=False,
    scale_b=False,
):
    ratio = a / b if b not in (0, None) and np.isfinite(b) else np.nan
    lo = hi = np.nan
    if scale_a and scale_b:
        lo, hi = (
            ratio * (1 - SCALE_REL) / (1 + SCALE_REL),
            ratio * (1 + SCALE_REL) / (1 - SCALE_REL),
        )
    elif scale_a:
        lo, hi = ratio * (1 - SCALE_REL), ratio * (1 + SCALE_REL)
    CR.append(
        dict(
            row_type="condition",
            stage=stage,
            comparison=comp,
            condition=cond,
            rpm=rpm_of(cond),
            quantity=quantity,
            unit=unit,
            a_label=a_label,
            a_value=a,
            b_label=b_label,
            b_value=b,
            ratio_a_over_b=ratio,
            ratio_scale_lo=lo,
            ratio_scale_hi=hi,
            flags=flags,
            notes=notes,
        )
    )


def cflags(c, extra=""):
    f = []
    if c in BOUNDARY:
        f.append("regime_boundary_60_80_sensitivity")
    if c.startswith("e20"):
        f.append("diagnostic_only_320rpm")
    if extra:
        f.append(extra)
    return ";".join(f)


LASER_NOTE = (
    "camera: 30.5 s record, ~30 Hz Nyquist, camera dataset campaign; laser: {dur:g} s, 360 Hz (180 Hz band), laser session {s}; "
    "separate non-simultaneous recordings; laser ddof=1 vs camera ddof=0 (<0.03%); laser scale/calibration uncertainty not propagated"
)
for c in conds[1:]:
    # cam1 vs cam2 same marker (ID-0-1)
    for q, unit in QTY.items():
        crow(
            "full",
            "cam1_vs_cam2_same_marker",
            c,
            f"{q}_rms_total_meanremoved",
            unit,
            "cam1",
            val(c, "cam1", q) if not c.startswith("e20") else np.nan,
            "cam2",
            val(c, "cam2", q) if not c.startswith("e20") else np.nan,
            cflags(c),
            "same physical marker ID-0-1, separate K/D and sensors; ratio of mm values bounded by independent +/-2.5% (conservative; common tag-size term would cancel)",
            unit == "mm",
            unit == "mm",
        )
    if not c.startswith("e20"):
        for cam in ("cam1", "cam2"):
            crow(
                "full",
                f"{cam}_lever_arm_term",
                c,
                "H1_y_over_lever125mm_x_H2roll",
                "ratio",
                f"{cam} H1_y_mm rms",
                val(c, cam, "H1_y_mm"),
                f"{LEVER_MM:g} mm x {cam} H2_roll_rad rms",
                LEVER_MM * val(c, cam, "H2_roll_rad"),
                cflags(c),
                "descriptive only: H1_y at offset marker includes lever-arm x roll; NOT laser heave; no phase/sign info in RMS ratio",
                True,
                True,
            )
    # cam3 observation path vs cam1/cam2
    for other in ("cam1", "cam2"):
        if c.startswith("e20"):
            continue
        for q, unit in QTY.items():
            crow(
                "full",
                f"cam3_vs_{other}_observation_path",
                c,
                f"{q}_rms_total_meanremoved",
                unit,
                "cam3",
                val(c, "cam3", q),
                other,
                val(c, other, q),
                cflags(c),
                "cam3 views different physical marker (ID-0-2, near axis, ~6 mm), own K/D, 60.00 Hz vs 59.94 Hz; paths kept separate",
                unit == "mm",
                unit == "mm",
            )
    # camera vs laser heave
    for s in ("y2025", "y2024"):
        if c not in L[s].index:
            continue
        lh = L[s].loc[c, "heave_mm_rms"]
        dur = L[s].loc[c, "duration_s"]
        for cam in CAMS:
            if c.startswith("e20") and cam != "cam3":
                continue
            prim = cam == "cam3"
            comp = f"{cam}_H1_y_vs_laser_heave_{s}" + ("_PRIMARY" if prim and s == "y2025" else "")
            note = LASER_NOTE.format(dur=dur, s=s) + (
                ""
                if prim
                else "; cam1/cam2 H1_y is offset-marker vertical displacement incl. lever-arm x roll, NOT heave"
            )
            crow(
                "full",
                comp,
                c,
                "H1_y_mm_rms_total_meanremoved_vs_laser_heave_mm_rms",
                "mm",
                cam,
                val(c, cam, "H1_y_mm"),
                f"laser_{s}",
                lh,
                cflags(c),
                note,
                True,
                False,
            )

C = pd.DataFrame(CR)


# ---------- condition-level statistics ----------
def spearman(x, y):
    from scipy.stats import spearmanr

    return float(spearmanr(x, y).statistic)


def stats(a, b):
    la, lb = np.log10(a), np.log10(b)
    return dict(
        geomean_ratio=float(10 ** np.mean(la - lb)),
        spearman=spearman(a, b),
        pearson_log=float(np.corrcoef(la, lb)[0, 1]),
    )


rng = np.random.default_rng(SEED)
S = []


def summarize(stage, comp, df, label):
    """df: condition-level rows with a_value,b_value. Condition is the unit for every statistic."""
    df = df[np.isfinite(df.a_value) & np.isfinite(df.b_value) & (df.a_value > 0) & (df.b_value > 0)]
    n = len(df)
    if n < 5:
        return
    a, b = df.a_value.to_numpy(), df.b_value.to_numpy()
    st = stats(a, b)
    for k, v in st.items():
        S.append(
            dict(
                row_type="summary",
                stage=stage,
                comparison=comp,
                stat=k,
                stat_value=v,
                n_conditions=n,
                notes=label,
            )
        )
    if stage == "sensitivity":
        bs = {k: [] for k in st}
        for _ in range(NBOOT):
            i = rng.integers(0, n, n)
            if len(set(i)) < 3:
                continue
            s2 = stats(a[i], b[i])
            for k in bs:
                bs[k].append(s2[k])
        for k in bs:
            x = np.array(bs[k])
            x = x[np.isfinite(x)]
            S.append(
                dict(
                    row_type="summary",
                    stage=stage,
                    comparison=comp,
                    stat=f"{k}_bootstrap_over_conditions",
                    stat_value=float(np.median(x)),
                    ci_lo=float(np.percentile(x, 2.5)),
                    ci_hi=float(np.percentile(x, 97.5)),
                    n_conditions=n,
                    notes=f"{label}; {NBOOT} resamples of conditions, seed {SEED}, percentile 95%",
                )
            )
        loco = []
        for j in range(n):
            m = np.arange(n) != j
            loco.append(dict(cond=df.condition.iloc[j], **stats(a[m], b[m])))
        lo = pd.DataFrame(loco)
        for k in st:
            S.append(
                dict(
                    row_type="summary",
                    stage=stage,
                    comparison=comp,
                    stat=f"{k}_leave_one_condition_out_range",
                    stat_value=float(lo[k].median()),
                    ci_lo=float(lo[k].min()),
                    ci_hi=float(lo[k].max()),
                    n_conditions=n - 1,
                    notes=f"{label}; min at held-out {lo.loc[lo[k].idxmin(), 'cond']}, max at held-out {lo.loc[lo[k].idxmax(), 'cond']}",
                )
            )


groups = C[C.row_type == "condition"].groupby("comparison")


def sel(comp, conds_):
    g = C[(C.comparison == comp) & C.condition.isin(conds_)]
    return g.groupby("condition").first().reset_index() if False else g


# FULL: admitted conditions e1..e19 (60/80 included, flagged)
for comp in C.comparison.unique():
    if "lever_arm" in comp:
        continue
    for qn in C[C.comparison == comp].quantity.unique():
        g = C[(C.comparison == comp) & (C.quantity == qn) & C.condition.isin(primary)]
        summarize("full", f"{comp}|{qn}", g, "admitted e1-e19, 60/80 RPM included")
# SENSITIVITY rows (after full)
excl = [c for c in primary if c not in BOUNDARY]
gated_cache = {}
for comp in C.comparison.unique():
    if "lever_arm" in comp:
        continue
    for qn in C[C.comparison == comp].quantity.unique():
        base = C[(C.comparison == comp) & (C.quantity == qn)]
        summarize(
            "sensitivity",
            f"{comp}|{qn}",
            base[base.condition.isin(primary)],
            "admitted e1-e19 incl 60/80 (bootstrap + LOCO)",
        )
        summarize(
            "sensitivity",
            f"{comp}|{qn}|excl_60_80",
            base[base.condition.isin(excl)],
            "excluding 60 and 80 RPM",
        )
        if comp.startswith("cam3") and "laser" in comp:
            summarize(
                "sensitivity",
                f"{comp}|{qn}|incl_e20_diagnostic",
                base[base.condition.isin(primary + ["e20_320rpm"])],
                "incl. diagnostic-only 320 RPM (not admitted)",
            )
# camera-floor-gated and detrended variants of cam3-vs-laser
for s in ("y2025", "y2024"):
    for cam in CAMS:
        ok = [
            c
            for c in primary
            if val(c, cam, "H1_y_mm") / val("e0_0rpm", cam, "H1_y_mm") >= FLOOR_GATE
        ]
        g = C[
            (C.comparison.str.startswith(f"{cam}_H1_y_vs_laser_heave_{s}")) & C.condition.isin(ok)
        ]
        summarize(
            "sensitivity",
            f"{cam}_H1_y_vs_laser_heave_{s}|camera_floor_gated_{FLOOR_GATE:g}x",
            g,
            f"camera >= {FLOOR_GATE:g}x own e0 floor ({len(ok)} conditions); laser floor not available, S6 both-sided gate not reproduced",
        )
        det = pd.DataFrame(
            [
                dict(
                    condition=c,
                    a_value=val(c, cam, "H1_y_mm", "linear_detrended"),
                    b_value=L[s].loc[c, "heave_mm_rms"],
                )
                for c in primary
            ]
        )
        summarize(
            "sensitivity",
            f"{cam}_H1_y_detrended_vs_laser_heave_{s}|linear_detrended",
            det,
            "camera linear-detrended RMS",
        )

Sdf = pd.DataFrame(S)
# detrended sensitivity condition rows (appended after full rows)
det_rows = []
for cond in conds[1:]:
    if cond.startswith("e20"):
        continue
    for s in ("y2025", "y2024"):
        crow(
            "sensitivity",
            f"cam3_H1_y_detrended_vs_laser_heave_{s}",
            cond,
            "H1_y_mm_rms_linear_detrended_vs_laser_heave_mm_rms",
            "mm",
            "cam3",
            val(cond, "cam3", "H1_y_mm", "linear_detrended"),
            f"laser_{s}",
            L[s].loc[cond, "heave_mm_rms"],
            cflags(cond),
            "sensitivity quantity; laser not detrended",
            True,
            False,
        )
C = pd.DataFrame(CR)
out = pd.concat([C, Sdf], ignore_index=True)
order = {"full": 0, "sensitivity": 1}
out["_o"] = out.stage.map(order)
out = out.sort_values("_o", kind="stable").drop(columns="_o")
cc = [
    "row_type",
    "stage",
    "comparison",
    "condition",
    "rpm",
    "quantity",
    "unit",
    "a_label",
    "a_value",
    "b_label",
    "b_value",
    "ratio_a_over_b",
    "ratio_scale_lo",
    "ratio_scale_hi",
    "stat",
    "stat_value",
    "ci_lo",
    "ci_hi",
    "n_conditions",
    "flags",
    "notes",
]
out[cc].to_csv(OUT / "PER_CAMERA_RMS_COMPARISON.csv", index=False, float_format="%.8g")

# ---------- ledger ----------
_rows = list(csv.reader(open(AUDIT / "PER_CAMERA_RMS_DEFINITION_LEDGER.csv", newline="")))
_fixed = []
for _r in _rows[
    1:
]:  # approved ledger has an unquoted comma in the H2_roll_rad source field; merge extras into source
    if len(_r) > 5:
        _r = _r[:2] + [",".join(_r[2 : len(_r) - 2])] + _r[-2:]
    _fixed.append(_r)
led = pd.DataFrame(_fixed, columns=_rows[0])
new = [
    (
        "rms_total_meanremoved",
        AGG["total"] + "; per stream, per camera, for H1_y_mm (mm) and H2_roll_rad (rad)",
        "analysis/paper2b/per_camera_rms/run_per_camera_rms.py",
        f"max |diff| vs results/s4_pose_by_stream.csv over 61 streams x 2 channels = {max_diff:.2e}",
        "verified",
    ),
    (
        "rms_linear_detrended",
        AGG["detrended"],
        "run_per_camera_rms.py",
        "sensitivity only; never substituted for total RMS",
        "defined",
    ),
    (
        "noise_floor",
        "Per-camera total (or detrended) RMS of the e0_0rpm stream, same channel; not noise-corrected",
        "run_per_camera_rms.py",
        "e0_0rpm has cam1,cam2,cam3 streams",
        "defined",
    ),
    (
        "noise_floor_ratio",
        f"RMS / same-camera e0_0rpm RMS; flag below_{FLOOR_GATE:g}x_camera_floor when ratio < {FLOOR_GATE:g}",
        "run_per_camera_rms.py; threshold from S6 rule (a)",
        "camera side only; laser floor not available here",
        "defined",
    ),
    (
        "regime_boundary_flag",
        "e4_60rpm and e6_80rpm flagged regime_boundary_60_80_sensitivity; retained in full results, excluded only in named sensitivity rows",
        "PER_CAMERA_RMS_GO_NO_GO.md cond. 5",
        "n/a",
        "defined",
    ),
    (
        "admissibility",
        "admitted (e0-e19 x cam1-3 = 60 streams); diagnostic_only (e20_320rpm cam3); e20 cam1/cam2 rejected, no values",
        "PER_CAMERA_RMS_GO_NO_GO.md cond. 3",
        "61 streams in parquet",
        "verified",
    ),
    (
        "scale_uncertainty",
        f"+/-{SCALE_REL * 100:g}% relative on mm quantities only (columns rms_scale_lo/hi, ratio_scale_lo/hi); not applied to rad; cancels in same-stream noise-floor ratios",
        "pose.py:16; OPEN_ISSUES_2026-10-17.md",
        "provisional pending ruler confirmation",
        "provisional",
    ),
    (
        "cam1_cam2_H1_y",
        "Offset-marker vertical displacement incl. lever-arm (~125 mm) x roll; NOT laser heave",
        "PER_CAMERA_RMS_GO_NO_GO.md cond. 4",
        "lever-arm descriptive ratio in COMPARISON.csv",
        "defined",
    ),
    (
        "laser_heave_rms",
        "heave_mm_rms (centre head, ddof=1, 360 Hz, full band to 180 Hz, no detrend) from results/laser_y{2025,2024}_by_condition.csv; sessions kept separate",
        "src/bridgedeck/laser.py:110-115",
        "files hashed in SOURCE_HASHES; not in the approved registry",
        "defined",
    ),
    (
        "condition_level_unit",
        "Correlations, bootstrap (resample conditions) and leave-one-condition-out use one value per condition; streams/frames are never resampled",
        "this script",
        f"seed {SEED}, {NBOOT} resamples",
        "defined",
    ),
]
led = pd.concat([led, pd.DataFrame(new, columns=led.columns)], ignore_index=True)
led.to_csv(OUT / "PER_CAMERA_RMS_DEFINITION_LEDGER.csv", index=False)

# ---------- hashes ----------
hl = []
for p in [
    PARQUET,
    INTR,
    S4CSV,
    LASER["y2025"],
    LASER["y2024"],
    AUDIT / "PER_CAMERA_RMS_DEFINITION_LEDGER.csv",
    AUDIT / "PER_CAMERA_RMS_GO_NO_GO.md",
    AUDIT / "PER_CAMERA_RMS_DESIGN_REVIEW.md",
    AUDIT / "PER_CAMERA_RMS_INPUT_REGISTRY.tsv",
    Path(__file__).resolve(),
]:
    hl.append(f"{sha(p)}  {rel(p)}")
(OUT / "PER_CAMERA_RMS_SOURCE_HASHES.sha256").write_text("\n".join(hl) + "\n")

# ---------- plots ----------
PAL = {"cam1": "#0072B2", "cam2": "#D55E00", "cam3": "#009E73"}
plt.rcParams.update(
    {
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "font.size": 9,
    }
)


def vline(ax):
    for r in (60, 80):
        ax.axvline(r, color="gray", ls=":", lw=1)


for q, unit in QTY.items():
    fig, ax = plt.subplots(figsize=(7, 4))
    for cam in CAMS:
        g = V[(V.quantity == f"{q}_rms_total_meanremoved") & (V.camera == cam)].sort_values("rpm")
        a = g[g.condition != "e20_320rpm"] if cam == "cam3" else g
        ax.plot(a.rpm, a.rms_value, "-o", ms=4, lw=1.5, color=PAL[cam], label=cam)
        if cam == "cam3":
            e = g[g.condition == "e20_320rpm"]
            ax.plot(
                e.rpm, e.rms_value, "x", color=PAL[cam], ms=9, label="cam3 e20 (diagnostic-only)"
            )
        ax.axhline(val("e0_0rpm", cam, q), color=PAL[cam], ls="--", lw=0.8)
    vline(ax)
    ax.set_yscale("symlog", linthresh=g.rms_value.min()) if False else ax.set_yscale("log")
    ax.set_xlabel("rpm (0 rpm = noise floor, dashed)")
    ax.set_ylabel(f"total mean-removed RMS ({unit})")
    ax.set_title(f"{q}: per-camera total RMS (ddof=0); dotted = 60/80 RPM")
    ax.legend(frameon=False)
    ax.set_xscale("symlog", linthresh=20)
    fig.tight_layout()
    fig.savefig(OUT / f"plots/rms_by_rpm_{q}.png", dpi=150)
    plt.close(fig)
fig, ax = plt.subplots(figsize=(7, 4))
for cam in CAMS:
    g = V[
        (V.quantity == "H1_y_mm_rms_total_meanremoved_noise_floor_ratio")
        & (V.camera == cam)
        & (V.rpm > 0)
    ].sort_values("rpm")
    ax.plot(g.rpm, g.rms_value, "-o", ms=4, color=PAL[cam], label=cam)
ax.axhline(FLOOR_GATE, color="k", lw=0.8, ls="--")
vline(ax)
ax.set_yscale("log")
ax.set_xlabel("rpm")
ax.set_ylabel("RMS / own e0_0rpm RMS")
ax.set_title(f"H1_y noise-floor ratio (dashed = {FLOOR_GATE:g}x)")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "plots/noise_floor_ratio_H1_y.png", dpi=150)
plt.close(fig)
fig, ax = plt.subplots(figsize=(7, 4))
for s, mk in (("y2025", "o"), ("y2024", "s")):
    g = C[
        (C.comparison.str.startswith(f"cam3_H1_y_vs_laser_heave_{s}"))
        & C.condition.isin(primary + ["e20_320rpm"])
    ]
    ax.scatter(
        g.b_value,
        g.a_value,
        marker=mk,
        color=PAL["cam3"],
        facecolor="none" if s == "y2024" else PAL["cam3"],
        label=f"cam3 vs laser {s}",
    )
    for _, r in g[g.condition.isin(BOUNDARY)].iterrows():
        ax.annotate(str(int(r.rpm)), (r.b_value, r.a_value), fontsize=7)
lim = [1e-3, 10]
ax.plot(lim, lim, "k:", lw=0.8)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("laser heave RMS (mm)")
ax.set_ylabel("cam3 H1_y total RMS (mm)")
ax.set_title("cam3 vs laser heave, per condition (60/80 labelled; not simultaneous)")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "plots/cam3_vs_laser_heave.png", dpi=150)
plt.close(fig)
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, q in zip(axs, QTY):
    for comp, col, lab in (
        ("cam1_vs_cam2_same_marker", "k", "cam1/cam2"),
        ("cam3_vs_cam1_observation_path", PAL["cam1"], "cam3/cam1"),
        ("cam3_vs_cam2_observation_path", PAL["cam2"], "cam3/cam2"),
    ):
        g = (
            C[(C.comparison == comp) & (C.quantity == f"{q}_rms_total_meanremoved") & (C.rpm > 0)]
            .dropna(subset=["ratio_a_over_b"])
            .sort_values("rpm")
        )
        ax.plot(g.rpm, g.ratio_a_over_b, "-o", ms=3, color=col, label=lab)
    ax.axhline(1, color="gray", lw=0.8)
    vline(ax)
    ax.set_yscale("log")
    ax.set_xlabel("rpm")
    ax.set_title(f"{q} RMS ratio")
    ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "plots/camera_path_ratios.png", dpi=150)
plt.close(fig)

# ---------- runtime ----------
rt = f"""per-camera RMS run
git HEAD: {head}
python: {sys.version.split()[0]}  numpy {np.__version__}  pandas {pd.__version__}
wall time s: {time.time() - T0:.1f}
source parquet sha256: {src_hash} (matches approved registry: {registry_ok})
streams in parquet: {streams}; conditions: {len(conds)}
max |diff| vs results/s4_pose_by_stream.csv total RMS (check only): {max_diff:.3e}
bootstrap: {NBOOT} resamples of conditions, seed {SEED}
"""
(OUT / "PER_CAMERA_RMS_RUNTIME.txt").write_text(rt)
print(rt)
