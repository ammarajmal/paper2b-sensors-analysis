"""S7b Part 1 (docs/gates/S7b.md): Monte Carlo propagation through the in-plane estimators, camera and laser. N = 200 draws, seed 11."""
import json, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np, pandas as pd
from bridgedeck import laser, paths, pose

R = paths.REPO / "results"; O = Path(paths.load()["outputs"]); FH, FA, HALF = 1.4318, 3.0982, 0.08; N = 200; SEED = 11
det = pd.read_parquet(O / "s2_detect/wtt_main/detections_ALL21.parquet")
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.rpm < 320)]
CONDS = sorted(P.condition.unique(), key=lambda c: int(c.split("_")[1].replace("rpm", "")))
cen = pd.read_csv(R / "s1_census_wtt_main.csv")
SIGT = {k: float(g.lat_sd_ms.median()) / 1000 for k, g in cen.assign(cam=cen.cam.str.replace("sony_", "")).groupby("cam")}
VARIANTS = {"corner": (1, 0, 0), "time": (0, 1, 0), "scale": (0, 0, 1), "all": (1, 1, 1)}


def corner_sigma(cam):
    g = det[(det.condition == "e0_0rpm") & (det.camera == cam) & det.detected & (det.decision_margin >= 30)].sort_values("frame_idx")
    c = pose.corners_of(g).reshape(len(g), 8)
    return float(np.std(np.diff(c, axis=0), axis=0).mean() / np.sqrt(2))


def cam_stream(args):
    cond, cam, sig_c = args
    rng = np.random.default_rng(abs(hash((SEED, cond, cam))) % 2**32); K, D = pose.intrinsics(cam)
    g = det[(det.condition == cond) & (det.camera == cam) & det.detected & (det.decision_margin >= 30)].sort_values("frame_idx")
    c0 = pose.corners_of(g); t0 = g.timestamp_s.to_numpy(); out = {}
    for vn, (fc, ft, fs) in VARIANTS.items():
        q1, q2 = [], []
        for _ in range(N):
            c = c0 + fc * rng.normal(0, sig_c, c0.shape); t = t0 + ft * rng.normal(0, SIGT[cam], t0.shape)
            cu = pose.undistort(c, K, D); cy = cu.mean(axis=1)[:, 1]; s = 1.0 + fs * rng.uniform(-0.025, 0.025)
            y1 = (cy - np.median(cy)) * (pose.TAG_MM * s / np.median(pose.side_len(cu)))
            ang = pose.edge_angle(cu); y2 = ang - np.median(ang)
            q1.append(pose.line_amplitude(t, y1, FH, HALF)[0]); q2.append(pose.line_amplitude(t, y2, FA, HALF)[0])
        out[vn] = (np.array(q1), np.array(q2))
    return cond, cam, out


def laser_session(args):
    s_name, cond, rpm, file = args
    s = laser.SESSIONS[s_name]; rng = np.random.default_rng(abs(hash((SEED, s_name, rpm))) % 2**32)
    vb = laser.load_volts(s, s.bias_file)[:, :2]; b = vb.mean(axis=0); sig = vb.std(axis=0, ddof=1)
    v = laser.load_volts(s, laser.disk_name(s, file)); t = np.arange(len(v)) / laser.FS; out = {}
    for vn, (fn, fd) in {"noise": (1, 0), "spacing": (0, 1), "all": (1, 1)}.items():
        q1, q2 = [], []
        for _ in range(N):
            vv = v.copy(); vv[:, :2] = vv[:, :2] + fn * rng.normal(0, 1, (len(v), 2)) * sig
            ch = laser.channels(vv, b, s); dfac = 1.0 + fd * rng.uniform(-0.15, 0.15)
            q1.append(pose.line_amplitude(t, ch["heave_mm"], FH, HALF)[0]); q2.append(pose.line_amplitude(t, ch["pitch_rad"] / dfac, FA, HALF)[0])
        out[vn] = (np.array(q1), np.array(q2))
    return s_name, cond, rpm, out


if __name__ == "__main__":
    sig = {k: corner_sigma(k) for k in ("cam1", "cam2", "cam3")}; print("corner sigma px", sig, "| stamp sigma s", SIGT, flush=True)
    rows = []
    with ProcessPoolExecutor(8) as ex:
        cres = list(ex.map(cam_stream, [(c, k, sig[k]) for c in CONDS for k in ("cam1", "cam2", "cam3")]))
        lj = [(s, r.condition, int(r.rpm), r.file) for s in ("y2025", "y2024") for _, r in P[P.session == s].iterrows()]
        lres = list(ex.map(laser_session, lj))
    for cond in CONDS:
        rpm = int(cond.split("_")[1].replace("rpm", ""))
        for vn in VARIANTS:
            for qi, q in enumerate(("Q1", "Q2")):
                m = np.mean([o[vn][qi] for c, k, o in cres if c == cond], axis=0)  # camera mean over cameras, per draw
                rows.append(dict(source="camera", session="", condition=cond, rpm=rpm, quantity=q, variant=vn, mc_mean=float(m.mean()), mc_sd=float(m.std(ddof=1)), mc_rel_sd=float(m.std(ddof=1) / m.mean())))
    for s, cond, rpm, o in lres:
        for vn in ("noise", "spacing", "all"):
            for qi, q in enumerate(("Q1", "Q2")):
                a = o[vn][qi]; rows.append(dict(source="laser", session=s, condition=cond, rpm=rpm, quantity=q, variant=vn, mc_mean=float(a.mean()), mc_sd=float(a.std(ddof=1)), mc_rel_sd=float(a.std(ddof=1) / a.mean())))
    pd.DataFrame(rows).to_csv(R / "s7b_mc.csv", index=False, float_format="%.10g"); print("rows", len(rows))
