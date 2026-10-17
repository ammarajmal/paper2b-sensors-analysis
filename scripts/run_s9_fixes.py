"""S9 Step 3 (docs/gates/S9.md): fix candidates X1-X5, all applied to all 19 conditions, judged first on camera-internal repeatability, then reported against BOTH lasers."""
import json
import numpy as np, pandas as pd
from pathlib import Path
from bridgedeck import compare as C, paths, pose

R = paths.REPO / "results"; O = Path(paths.load()["outputs"]); FH, FA, HALF = 1.4318, 3.0982, 0.08; SEED = 11
fr = pd.read_parquet(O / "s4_pose_channels_by_frame.parquet")
det = pd.read_parquet(O / "s2_detect/wtt_main/detections_ALL21.parquet")[["condition", "camera", "frame_idx", "decision_margin"]]
fr = fr.merge(det, on=["condition", "camera", "frame_idx"], how="left")
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.rpm < 320)]
B = pd.read_csv(R / "s7_budget_by_condition.csv")
floors = json.load(open(R / "s6_floors.json"))["camera_e0"]
Q = {"Q1": ("P1_y_mm", FH, "Afh", "las_heave_Afh"), "Q2": ("P5_roll_rad", FA, "Afa", "las_pitch_Afa")}
CAMS = ("cam1", "cam2", "cam3")


def design(t, f): return np.column_stack([np.cos(2 * np.pi * f * t), np.sin(2 * np.pi * f * t), np.ones_like(t)])


def lsq(t, y, f0):
    return pose.line_amplitude(t, y, f0, HALF)


def huber(t, y, f0):
    best = (np.inf, 0.0, f0)
    for f in np.linspace(f0 - HALF, f0 + HALF, 21):
        X = design(t, f); w = np.ones(len(y))
        for _ in range(10):
            sw = np.sqrt(w); beta = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]; r = y - X @ beta
            s = 1.4826 * np.median(np.abs(r - np.median(r))) + 1e-12; w = np.minimum(1.0, 1.345 * s / np.maximum(np.abs(r), 1e-12))
        u = np.abs(r) / s; loss = np.sum(np.where(u <= 1.345, 0.5 * u**2, 1.345 * u - 0.5 * 1.345**2))
        if loss < best[0]: best = (loss, float(np.hypot(beta[0], beta[1])), float(f))
    return best[1], best[2]


def hampel_keep(y, k=11, nsig=3.0):
    s = pd.Series(y); med = s.rolling(k, center=True, min_periods=1).median(); mad = (s - med).abs().rolling(k, center=True, min_periods=1).median()
    return ((s - med).abs() <= nsig * 1.4826 * mad + 1e-12).to_numpy()


def windows(t, y, f, n=3):
    e = np.linspace(t.min(), t.max() + 1e-9, n + 1); out = []
    for lo, hi in zip(e[:-1], e[1:]):
        m = (t >= lo) & (t < hi)
        if m.sum() < 20: out.append(np.nan); continue
        cf = np.linalg.lstsq(design(t[m], f), y[m], rcond=None)[0]; out.append(np.hypot(cf[0], cf[1]))
    return np.array(out)


rows = []
for cond in sorted(P.condition.unique(), key=lambda c: int(c.split("_")[1].replace("rpm", ""))):
    rpm = int(cond.split("_")[1].replace("rpm", ""))
    for q, (col, f0, suf, _) in Q.items():
        per = {v: {} for v in ("base", "X1", "X2", "X2r", "X3", "X5a")}; wspread = {}
        for cam in CAMS:
            d = fr[(fr.condition == cond) & (fr.camera == cam)].sort_values("t_s"); t, y, mg = d.t_s.to_numpy(), d[col].to_numpy(), d.decision_margin.to_numpy()
            if len(d) < 100: continue
            a0, fs = lsq(t, y, f0); per["base"][cam] = a0
            per["X1"][cam] = huber(t, y, f0)[0]
            keep = (mg >= np.nanpercentile(mg, 5)) & hampel_keep(y); per["X2"][cam] = lsq(t[keep], y[keep], f0)[0]
            res = y - design(t, fs) @ np.linalg.lstsq(design(t, fs), y, rcond=None)[0]; kr = hampel_keep(res) & (mg >= np.nanpercentile(mg, 5)); per["X2r"][cam] = lsq(t[kr], y[kr], f0)[0]
            w = windows(t, y, fs); per["X3"][cam] = float(np.nanmedian(w)); wspread[cam] = float(np.nanstd(w, ddof=1) / np.nanmean(w) / np.sqrt(3))
            per["X5a"][cam] = huber(t[keep], y[keep], f0)[0]
        r = dict(condition=cond, rpm=rpm, quantity=q)
        for v, dct in per.items():
            r[f"{v}_mean"] = float(np.mean(list(dct.values())))
            if "cam1" in dct and "cam2" in dct: r[f"{v}_ln_c1c2"] = float(np.log(dct["cam1"] / dct["cam2"]))
        # X4 inverse-variance fusion of the base and of the X5a per-camera amplitudes
        for v in ("base", "X5a"):
            dct = per[v]; wv = {k: 1.0 / ((floors[f"cam_{k}_{col}_{suf}"] / dct[k]) ** 2 + wspread[k] ** 2) for k in dct}; r[f"{'X4' if v == 'base' else 'X5b'}_mean"] = float(sum(wv[k] * dct[k] for k in dct) / sum(wv.values()))
        r["ref_S6_cam_mean"] = float(P[(P.condition == cond)].iloc[0][f"cam_mean_{col}_{suf}"])
        rows.append(r)
D = pd.DataFrame(rows); D.to_csv(R / "s9_fix_amplitudes.csv", index=False, float_format="%.10g")
print("baseline reproduces the S6 camera amplitude: max rel diff", float(np.max(np.abs(D.base_mean / D.ref_S6_cam_mean - 1))))
VAR = ["base", "X1", "X2", "X2r", "X3", "X4", "X5a", "X5b"]; out = []
for q, (col, f0, suf, lascol) in Q.items():
    for v in VAR:
        r = {"quantity": q, "variant": v}; d = D[D.quantity == q].sort_values("rpm")
        if f"{v}_ln_c1c2" in d: r["median_abs_ln_c1c2"] = float(np.abs(d[f"{v}_ln_c1c2"]).median()); r["max_abs_ln_c1c2"] = float(np.abs(d[f"{v}_ln_c1c2"]).max())
        r["median_shift_vs_base"] = float(np.median(d[f"{v}_mean"] / d.base_mean - 1)); r["max_abs_shift_vs_base"] = float(np.max(np.abs(d[f"{v}_mean"] / d.base_mean - 1)))
        for s in ("y2025", "y2024"):
            las = P[P.session == s].sort_values("rpm"); lv = las[lascol].to_numpy(); cv = d[f"{v}_mean"].to_numpy(); ra = B[(B.quantity == q) & (B.session == s)].sort_values("rpm").rule_a.to_numpy()
            for sn, m in (("all19", np.ones(len(cv), bool)), ("rule_a", ra)):
                mm = C.metrics_once(cv[m], lv[m]); r[f"{s}_{sn}_E"] = mm["E_log10"]; r[f"{s}_{sn}_median_ratio"] = mm["median_ratio"]
        for sn in ("all19", "rule_a"):
            m = np.ones(len(d), bool) if sn == "all19" else (B[(B.quantity == q) & (B.session == "y2025")].sort_values("rpm").rule_a.to_numpy() & B[(B.quantity == q) & (B.session == "y2024")].sort_values("rpm").rule_a.to_numpy())
            cv = d[f"{v}_mean"].to_numpy()[m]; l25 = P[P.session == "y2025"].sort_values("rpm")[lascol].to_numpy()[m]; l24 = P[P.session == "y2024"].sort_values("rpm")[lascol].to_numpy()[m]
            e25, e24 = np.log10(cv / l25) ** 2, np.log10(cv / l24) ** 2; obs = np.sqrt(e24.mean()) - np.sqrt(e25.mean()); rng = np.random.default_rng(SEED); cnt = 0
            for _ in range(5000):
                sw = rng.random(len(cv)) < 0.5; a = np.where(sw, e24, e25); b_ = np.where(sw, e25, e24); cnt += (np.sqrt(b_.mean()) - np.sqrt(a.mean())) >= obs
            r[f"dE_2024_minus_2025_{sn}"] = float(obs); r[f"perm_p_2025_closer_{sn}"] = float((cnt + 1) / 5001)
        out.append(r)
T = pd.DataFrame(out); T.to_csv(R / "s9_fix_summary.csv", index=False, float_format="%.8g")
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40)
print(T[["quantity", "variant", "median_abs_ln_c1c2", "max_abs_ln_c1c2", "median_shift_vs_base", "max_abs_shift_vs_base"]].round(4).to_string(index=False))
print(T[["quantity", "variant", "y2025_all19_E", "y2024_all19_E", "y2025_all19_median_ratio", "y2024_all19_median_ratio", "dE_2024_minus_2025_all19", "perm_p_2025_closer_all19"]].round(3).to_string(index=False))
print(T[["quantity", "variant", "y2025_rule_a_E", "y2024_rule_a_E", "dE_2024_minus_2025_rule_a", "perm_p_2025_closer_rule_a"]].round(3).to_string(index=False))
