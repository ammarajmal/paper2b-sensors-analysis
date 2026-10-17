"""S9 Step 1 (docs/gates/S9.md): camera-internal outlier flags F1-F7. This script must not read any laser file."""
import numpy as np, pandas as pd, json
from pathlib import Path
from bridgedeck import paths, pose

R = paths.REPO / "results"; O = Path(paths.load()["outputs"]); FH, FA = 1.4318, 3.0982
det = pd.read_parquet(O / "s2_detect/wtt_main/detections_ALL21.parquet")
det5 = pd.read_parquet(next((O / "s2_detect/wtt_5sec").glob("*.parquet")))
fr = pd.read_parquet(O / "s4_pose_channels_by_frame.parquet")
B = pd.read_csv(R / "s7_budget_by_condition.csv"); B = B[B.session == "y2025"]   # camera columns are identical in both sessions
fl = json.load(open(R / "s6_floors.json"))["camera_e0"]
CAMS = ("cam1", "cam2", "cam3")
CONDS = sorted(det.condition.unique(), key=lambda c: int(c.split("_")[1].replace("rpm", "")))


def mz(x):
    x = np.asarray(x, float); m = np.nanmedian(x); mad = np.nanmedian(np.abs(x - m))
    return 0.6745 * (x - m) / mad if mad > 0 else np.zeros_like(x)


rows = []
for c in CONDS:
    for k in CAMS:
        g = det[(det.condition == c) & (det.camera == k)]
        if len(g) == 0: continue
        ok = g.detected & (g.decision_margin >= 30)
        rows.append(dict(condition=c, camera=k, n=len(g), valid_frac=float(ok.mean()), median_margin=float(g.decision_margin[ok].median())))
S = pd.DataFrame(rows); S["rpm"] = S.condition.str.extract(r"_(\d+)rpm").astype(int)
adm = S[~S.condition.str.startswith("e20")]
S["F1_completeness"] = S.valid_frac < 0.95
S["margin_z_all"] = np.nan; S.loc[adm.index, "margin_z_all"] = mz(adm.median_margin)
S["F2_margin"] = S.margin_z_all.abs() > 3.5
# sensitivity (not the gate rule): modified z within camera
S["margin_z_within_cam"] = np.nan
for k, g in adm.groupby("camera"): S.loc[g.index, "margin_z_within_cam"] = mz(g.median_margin)
# F6 common-mode line relative to the structural line (cam1, cam2 only)
f6 = []
for _, r in S.iterrows():
    d = fr[(fr.condition == r.condition) & (fr.camera == r.camera)].sort_values("t_s")
    a9 = pose.line_amplitude(d.t_s.to_numpy(), d.P1_y_mm.to_numpy(), 9.25, 0.15)[0]
    ah = pose.line_amplitude(d.t_s.to_numpy(), d.P1_y_mm.to_numpy(), FH, 0.08)[0]; aa = pose.line_amplitude(d.t_s.to_numpy(), d.P5_roll_rad.to_numpy(), FA, 0.08)[0]
    f6.append(dict(A9_mm=a9, A_fh_mm=ah, ratio_9_to_fh=a9 / ah if ah > 0 else np.nan))
S = pd.concat([S.reset_index(drop=True), pd.DataFrame(f6)], axis=1)
S["F6_common_mode"] = (S.camera.isin(["cam1", "cam2"])) & (S.ratio_9_to_fh > 0.5)
S.to_csv(R / "s9_stream_flags.csv", index=False, float_format="%.10g")

P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.session == "y2025") & (P.rpm < 320)].set_index("condition")   # camera columns only


def light(g, cam, line, kind, half=0.15, nwin=3):
    K, D = pose.intrinsics(cam); c = pose.corners_of(g); cu = pose.undistort(c, K, D); t = g.timestamp_s.to_numpy()
    if kind == "heave": cy = cu.mean(axis=1)[:, 1]; y = (cy - np.median(cy)) * (pose.TAG_MM / np.median(pose.side_len(cu)))
    else: ang = pose.edge_angle(cu); y = ang - np.median(ang)
    a, f = pose.line_amplitude(t, y, line, half)
    e = np.linspace(t.min(), t.max() + 1e-9, nwin + 1); w = []
    for lo, hi in zip(e[:-1], e[1:]):
        m = (t >= lo) & (t < hi); X = np.column_stack([np.cos(2 * np.pi * f * t[m]), np.sin(2 * np.pi * f * t[m]), np.ones(m.sum())]); cf = np.linalg.lstsq(X, y[m], rcond=None)[0]; w.append(np.hypot(cf[0], cf[1]))
    return a, float(np.std(w, ddof=1) / np.mean(w) / np.sqrt(nwin))


rc = []
for c in CONDS:
    if c.startswith("e20") or c not in P.index: continue   # e0 (static) and e20 (rejected) are not among the 19 compared conditions
    rpm = int(c.split("_")[1].replace("rpm", "")); r = dict(condition=c, rpm=rpm)
    for q, col, suf, line, kind in (("Q1", "cam_mean_P1_y_mm_Afh", "P1_y_mm_Afh", FH, "heave"), ("Q2", "cam_mean_P5_roll_rad_Afa", "P5_roll_rad_Afa", FA, "pitch")):
        a1, a2 = P.loc[c, f"cam_cam1_{suf.replace('_Afh', '_Afh').replace('_Afa', '_Afa')}"], P.loc[c, f"cam_cam2_{suf}"]
        r[f"{q}_ln_cam1_cam2"] = float(np.log(a1 / a2)); amp = float(P.loc[c, col]); r[f"{q}_cam_amp"] = amp
        r[f"{q}_floor_ratio"] = amp / float(np.mean([fl[f"cam_{k}_{suf}"] for k in CAMS]))
        b = B[(B.condition == c) & (B.quantity == q)].iloc[0]; r[f"{q}_C6"] = float(b.C6)
        a5, w5 = [], []
        for k in CAMS:
            g = det5[(det5.condition == c) & (det5.camera == k) & det5.detected & (det5.decision_margin >= 30)].sort_values("frame_idx")
            if len(g) < 100: continue
            a, ws = light(g, k, line, kind); a5.append(a); w5.append(ws)
        r[f"{q}_amp_5s"] = float(np.mean(a5)) if a5 else np.nan; r[f"{q}_u_5s"] = float(np.mean(w5)) if w5 else np.nan
        r[f"{q}_ln_5s_over_main"] = float(np.log(np.mean(a5) / amp)) if a5 and amp > 0 else np.nan
        r[f"{q}_u_C"] = float(b.u_C)
    rc.append(r)
C = pd.DataFrame(rc)
for q in ("Q1", "Q2"):
    C[f"{q}_F3_z"] = mz(C[f"{q}_ln_cam1_cam2"]); C[f"{q}_F3"] = C[f"{q}_F3_z"].abs() > 3.5
    C[f"{q}_F4_z"] = mz(C[f"{q}_C6"]); C[f"{q}_F4"] = C[f"{q}_F4_z"].abs() > 3.5
    C[f"{q}_F5"] = C[f"{q}_ln_5s_over_main"].abs() > 2 * np.sqrt(C[f"{q}_u_C"] ** 2 + C[f"{q}_u_5s"] ** 2)
    C[f"{q}_F7"] = C[f"{q}_floor_ratio"] < 5
for f, col in (("F1", "F1_completeness"), ("F2", "F2_margin"), ("F6", "F6_common_mode")):
    C[f] = [bool(S[(S.condition == c) & ~S.condition.str.startswith("e20")][col].any()) for c in C.condition]
C.to_csv(R / "s9_condition_flags.csv", index=False, float_format="%.10g")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print("streams", len(S), "| admitted", len(adm), "| conditions", len(C))
print("F1", int(S.F1_completeness.sum()), "F2", int(S.F2_margin.sum()), "F6", int(S.F6_common_mode.sum()), "| F2 within-camera sensitivity:", int((S.margin_z_within_cam.abs() > 3.5).sum()))
for q in ("Q1", "Q2"):
    print(q, "F3", C.rpm[C[f"{q}_F3"]].tolist(), "F4", C.rpm[C[f"{q}_F4"]].tolist(), "F5", C.rpm[C[f"{q}_F5"]].tolist(), "F7", C.rpm[C[f"{q}_F7"]].tolist())
print("F1 conds", C.rpm[C.F1].tolist(), "| F2 conds", C.rpm[C.F2].tolist(), "| F6 conds", C.rpm[C.F6].tolist())
print("missing values:", int(C[[c for c in C if c.endswith(('_z', '_ln_5s_over_main'))]].isna().sum().sum()))
