"""Stage S7: uncertainty budget for Q1 (heave @ f_h) and Q2 (pitch @ f_alpha). Gate: docs/gates/S7.md (components C1-C7, L1-L4)."""

import json
import numpy as np
import pandas as pd
from bridgedeck import compare as C, laser, paths, pose

R = paths.REPO / "results"
S3 = np.sqrt(3.0)
FH, FA = C.FH, C.FA
P = pd.read_csv(R / "s6_matched_pairs.csv")
P = P[(P.arm == "A") & (P.rpm < 320)]
floors = json.load(open(R / "s6_floors.json"))
fr = pd.read_parquet(paths.REPO / "outputs/s4_pose_channels_by_frame.parquet")
det = pd.read_parquet(paths.REPO / "outputs/s2_detect/wtt_main/detections_ALL21.parquet")
hdr = det[["condition", "camera", "frame_idx", "stamp_hdr_ns"]].drop_duplicates(["condition", "camera", "frame_idx"])
fr = fr.merge(hdr, on=["condition", "camera", "frame_idx"], how="left")
HALVES = (0.03, 0.05, 0.08, 0.15)
QS = {  # quantity: (line, camera estimators, primary camera estimator column, laser column, camera floor key)
    "Q1": (FH, ["P1_y_mm", "P2_y_mm", "P6_y_mm", "H1_y_mm"], "P1_y_mm", "las_heave_Afh"),
    "Q2": (FA, ["P5_roll_rad", "H2_roll_rad"], "P5_roll_rad", "las_pitch_Afa"),
}


def A(t, y, f, h=C.HALF):
    return pose.line_amplitude(np.asarray(t, float), np.asarray(y, float), f, h)[0]


def windows(t, y, f, n):
    e = np.linspace(t.min(), t.max() + 1e-9, n + 1)
    return np.array([A(t[(t >= a) & (t < b)], y[(t >= a) & (t < b)], f) for a, b in zip(e[:-1], e[1:])])


rows = []
for cond in sorted(P.condition.unique(), key=lambda c: int(c.split("_")[1].replace("rpm", ""))):
    rpm = int(cond.split("_")[1].replace("rpm", ""))
    g = fr[fr.condition == cond]
    pc = P[(P.condition == cond)].iloc[0]
    for q, (f, ests, prim, lascol) in QS.items():
        r = {"condition": cond, "rpm": rpm, "quantity": q}
        cams = sorted(g.camera.unique())
        per_cam = {c: g[g.camera == c].sort_values("t_s") for c in cams}
        base = np.array([A(d.t_s, d[prim], f) for d in per_cam.values()])
        a_cam = float(base.mean())
        r["cam_amp"] = a_cam
        # C1 scale
        r["C1"] = 0.025 / S3 if q == "Q1" else 0.0
        # C2 estimator spread (relative SD across estimators of the camera-mean amplitude)
        em = np.array([np.mean([A(d.t_s, d[e], f) for d in per_cam.values()]) for e in ests])
        r["C2"] = float(np.std(em, ddof=1) / em.mean())
        # C3 camera to camera (includes the physical marker-position difference for heave)
        r["C3"] = float(np.std(base, ddof=1) / np.sqrt(len(base)) / a_cam) if len(base) > 1 else np.nan
        # C4 timebase: header stamps, nominal index/60, uniform 60 Hz interpolation of record stamps
        alts = []
        for kind in ("hdr", "nom", "i60"):
            am = []
            for d in per_cam.values():
                if kind == "hdr":
                    t, y = d.stamp_hdr_ns.to_numpy() / 1e9, d[prim].to_numpy()
                elif kind == "nom":
                    t, y = d.frame_idx.to_numpy() / 60.0, d[prim].to_numpy()
                else:
                    m = np.isfinite(d[prim].to_numpy()); t, y = d.t_s.to_numpy()[m], d[prim].to_numpy()[m]
                    t = t - t[0]; tg = np.arange(t[0], t[-1], 1 / 60.0); y = np.interp(tg, t, y); t = tg
                am.append(A(t, y, f))
            alts.append(np.mean(am))
        r["C4"] = float(max(abs(np.array(alts) / a_cam - 1)) / S3)
        # C5 line search
        ah = np.array([np.mean([A(d.t_s, d[prim], f, h) for d in per_cam.values()]) for h in HALVES])
        r["C5"] = float((ah.max() - ah.min()) / 2 / ah.mean() / S3)
        # C6 stationarity: three consecutive windows
        wa = np.array([windows(d.t_s.to_numpy(), d[prim].to_numpy(), f, 3) for d in per_cam.values()]).mean(axis=0)
        r["C6"] = float(np.std(wa, ddof=1) / wa.mean() / S3)
        # C7 additive noise: mean per-camera zero-wind floor / amplitude
        fl = np.mean([floors["camera_e0"].get(f"cam_{c}_{prim}_{'Afh' if q=='Q1' else 'Afa'}", np.nan) for c in cams])
        r["C7"] = float(fl / a_cam)
        r["cam_floor"] = float(fl)
        r["u_C"] = float(np.sqrt(np.nansum([r[k] ** 2 for k in ("C1", "C2", "C3", "C4", "C5", "C6", "C7")])))
        rows.append(r)
cam = pd.DataFrame(rows)

# ---- laser ----
lrows = []
for s in ("y2025", "y2024"):
    sess = laser.SESSIONS[s]
    b = laser.bias(sess)
    nwin = 4 if s == "y2025" else 3
    for _, pr in P[P.session == s].iterrows():
        v = laser.load_volts(sess, laser.disk_name(sess, pr["file"]))
        ch = laser.channels(v, b, sess)
        t = np.arange(len(v)) / laser.FS
        for q, (f, _, _, lascol) in QS.items():
            y = ch["heave_mm"] if q == "Q1" else ch["pitch_rad"]
            a = A(t, y, f)
            r = {"session": s, "condition": pr.condition, "rpm": pr.rpm, "quantity": q, "las_amp": a}
            r["L1"] = 0.15 / S3 if q == "Q2" else 0.0
            w = windows(t, y, f, nwin)
            r["L2"] = float(np.std(w, ddof=1) / w.mean() / np.sqrt(nwin))
            fl = floors["laser"][s][lascol]
            r["L3"] = float(fl / a)
            ah = np.array([A(t, y, f, h) for h in HALVES])
            r["L4"] = float((ah.max() - ah.min()) / 2 / ah.mean() / S3)
            r["u_L"] = float(np.sqrt(sum(r[k] ** 2 for k in ("L1", "L2", "L3", "L4"))))
            r["las_amp_s6"] = pr[lascol]
            lrows.append(r)
las = pd.DataFrame(lrows)
B = las.merge(cam, on=["condition", "rpm", "quantity"])
B["u_R"] = np.sqrt(B.u_C**2 + B.u_L**2)
B["ln_ratio"] = np.log(B.cam_amp / B.las_amp)
# rule a membership: both instruments >= 5x their own floor
B["las_floor"] = B.L3 * B.las_amp  # L3 is floor / amplitude
B["rule_a"] = (B.cam_amp >= 5 * B.cam_floor) & (B.las_amp >= 5 * B.las_floor)
B["covered_k2"] = B.ln_ratio.abs() <= 2 * B.u_R
B.to_csv(R / "s7_budget_by_condition.csv", index=False)
pd.set_option("display.width", 220)
comp = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "L1", "L2", "L3", "L4"]
print("integrity: rows", len(B), "| NaN u_R:", int(B.u_R.isna().sum()), "| rule-a rows with NaN:", int(B[B.rule_a].u_R.isna().sum()))
print("laser amplitude reproduces S6 (max rel diff):", float(np.nanmax(np.abs(B.las_amp / B.las_amp_s6 - 1))))
for q in ("Q1", "Q2"):
    for s in ("y2025", "y2024"):
        d = B[(B.quantity == q) & (B.session == s)]
        for lab, dd in (("rule a", d[d.rule_a]), ("all 19", d)):
            print(f"{q} {s} {lab:6s} n={len(dd):2d} median u_C {dd.u_C.median():.3f} u_L {dd.u_L.median():.3f} u_R {dd.u_R.median():.3f} | RMS ln ratio {np.sqrt(np.mean(dd.ln_ratio**2)):.3f} vs RMS u_R {np.sqrt(np.mean(dd.u_R**2)):.3f} | covered k=2: {dd.covered_k2.sum()}/{len(dd)}")
print("\nmedian relative component (rule a):")
print(B[B.rule_a].groupby(["quantity", "session"])[comp].median().round(3).to_string())
# session effect indicator
for q in ("Q1", "Q2"):
    w = B[B.quantity == q].pivot(index="rpm", columns="session", values="las_amp").dropna()
    ra = B[(B.quantity == q) & B.rule_a].groupby("rpm").rule_a.sum()
    ok = w.index[w.index.isin(ra.index[ra == 2])]
    d = np.log(w.loc[ok, "y2025"] / w.loc[ok, "y2024"])
    print(f"session-effect indicator {q}: SD of ln(laser2025/laser2024) = {d.std(ddof=1):.3f}, mean {d.mean():.3f} over {len(ok)} rule-a RPM")
