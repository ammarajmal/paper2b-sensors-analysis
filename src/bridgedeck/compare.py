"""Stage S6: camera versus laser comparison (gate: docs/gates/S6.md). Descriptive; rules fixed in the gate."""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import laser, pose

FH, FA, HALF = 1.4318, 3.0982, 0.08
TAG_SCALE_SENS = 0.025
RNG_SEED = 11
N_BOOT = 2000


def amp(t, y, f0):
    return pose.line_amplitude(np.asarray(t, float), np.asarray(y, float), f0, HALF)[0]


# ---------------- camera ----------------
CAM_Q1 = ["P1_y_mm", "P2_y_mm", "P6_y_mm", "H1_y_mm"]
CAM_Q2 = ["P5_roll_rad", "H2_roll_rad"]


def camera_table(frames: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cond, gc in frames.groupby("condition"):
        r = {"condition": cond, "rpm": int(cond.split("_")[1].replace("rpm", ""))}
        per = {}
        for cam, g in gc.groupby("camera"):
            t = g.t_s.to_numpy()
            for c in CAM_Q1:
                per.setdefault(("Q1", c), []).append(amp(t, g[c], FH))
                r[f"cam_{cam}_{c}_Afh"] = per[("Q1", c)][-1]
            for c in CAM_Q2:
                per.setdefault(("Q2", c), []).append(amp(t, g[c], FA))
                r[f"cam_{cam}_{c}_Afa"] = per[("Q2", c)][-1]
        for c in CAM_Q1:
            r[f"cam_mean_{c}_Afh"] = float(np.mean(per[("Q1", c)]))
        for c in CAM_Q2:
            r[f"cam_mean_{c}_Afa"] = float(np.mean(per[("Q2", c)]))
        r["n_cams"] = gc.camera.nunique()
        # legacy series: pair cam1, cam2 to the cam3 stamps (nearest, within 0.75 of the median interval, no interpolation)
        if {"cam1", "cam2", "cam3"} <= set(gc.camera.unique()):
            g3 = gc[gc.camera == "cam3"].sort_values("t_s")
            t3, y3 = g3.t_s.to_numpy(), g3.P1_y_mm.to_numpy()
            dt = np.median(np.diff(t3))
            ys = {}
            for cam in ("cam1", "cam2"):
                g = gc[gc.camera == cam].sort_values("t_s")
                tt, yy = g.t_s.to_numpy(), g.P1_y_mm.to_numpy()
                i = np.clip(np.searchsorted(tt, t3), 1, len(tt) - 1)
                j = np.where(np.abs(tt[i - 1] - t3) <= np.abs(tt[i] - t3), i - 1, i)
                ys[cam] = np.where(np.abs(tt[j] - t3) <= 0.75 * dt, yy[j], np.nan)
            ok = np.isfinite(ys["cam1"]) & np.isfinite(ys["cam2"])
            y12 = (ys["cam1"] + ys["cam2"]) / 2
            bend = ((y12 + y3) / 2)[ok]
            tors = (y3 - y12)[ok]
            r["cam_legacy_bend_Afh"], r["cam_legacy_tors_Afa"] = (
                amp(t3[ok], bend, FH),
                amp(t3[ok], tors, FA),
            )
            r["cam_legacy_bend_rms"], r["cam_legacy_tors_rms"] = (
                float(np.std(bend)),
                float(np.std(tors)),
            )
            r["legacy_pair_share"] = float(ok.mean())
        rows.append(r)
    return pd.DataFrame(rows).sort_values("rpm").reset_index(drop=True)


# ---------------- laser ----------------
def laser_table(name: str) -> tuple[pd.DataFrame, dict]:
    s = laser.SESSIONS[name]
    b = laser.bias(s)
    base = laser.run_session(name)
    rows = []
    for _, r0 in base.iterrows():
        v = laser.load_volts(s, laser.disk_name(s, r0["file"]))
        ch = laser.channels(v, b, s)
        t = np.arange(len(v)) / laser.FS
        rows.append(
            {
                "session": name,
                "rpm": r0["rpm"],
                "file": r0["file"],
                "wind_ms": r0["wind_measured_ms"],
                "las_heave_Afh": amp(t, ch["heave_mm"], FH),
                "las_pitch_Afa": amp(t, ch["pitch_rad"], FA),
                "las_bend_Afh": amp(t, ch["bending_avg_mm"], FH),
                "las_tors_Afa": amp(t, ch["torsion_proxy_mm"], FA),
                "las_bend_rms": r0["bending_avg_mm_rms"],
                "las_tors_rms": r0["torsion_proxy_mm_rms"],
                "las_bend_dom_hz": r0["bending_dom_hz"],
                "las_tors_dom_hz": r0["torsion_dom_hz"],
            }
        )
    vb = laser.load_volts(s, s.bias_file)
    chb = laser.channels(vb, vb.mean(axis=0)[:2], s)
    tb = np.arange(len(vb)) / laser.FS
    floor = {
        "las_heave_Afh": amp(tb, chb["heave_mm"], FH),
        "las_pitch_Afa": amp(tb, chb["pitch_rad"], FA),
        "las_bend_Afh": amp(tb, chb["bending_avg_mm"], FH),
        "las_tors_Afa": amp(tb, chb["torsion_proxy_mm"], FA),
    }
    return pd.DataFrame(rows), floor


# ---------------- metrics ----------------
def deming_slope(x, y):
    sxx, syy, sxy = np.var(x, ddof=1), np.var(y, ddof=1), np.cov(x, y)[0, 1]
    return (
        float((syy - sxx + np.sqrt((syy - sxx) ** 2 + 4 * sxy**2)) / (2 * sxy))
        if sxy != 0
        else np.nan
    )


def metrics_once(cam, las):
    lc, ll = np.log10(cam), np.log10(las)
    lr = lc - ll
    ratio = cam / las
    return {
        "n": len(cam),
        "pearson_lin": float(np.corrcoef(cam, las)[0, 1]) if len(cam) > 2 else np.nan,
        "pearson_log": float(np.corrcoef(lc, ll)[0, 1]) if len(cam) > 2 else np.nan,
        "spearman": float(pd.Series(cam).rank().corr(pd.Series(las).rank()))
        if len(cam) > 2
        else np.nan,
        "median_ratio": float(np.median(ratio)),
        "E_log10": float(np.sqrt(np.mean(lr**2))),
        "gsd_ratio": float(10 ** np.std(lr, ddof=1)) if len(cam) > 2 else np.nan,
        "iqr_ratio": float(np.subtract(*np.percentile(ratio, [75, 25]))),
        "deming_slope_log": deming_slope(ll, lc) if len(cam) > 2 else np.nan,
        "ba_bias_log10": float(np.mean(lr)),
        "ba_loa_log10": float(1.96 * np.std(lr, ddof=1)) if len(cam) > 2 else np.nan,
    }


def metrics_boot(cam, las, seed=RNG_SEED, n_boot=N_BOOT):
    cam, las = np.asarray(cam, float), np.asarray(las, float)
    m = metrics_once(cam, las)
    if len(cam) < 4:
        return m
    rng = np.random.default_rng(seed)
    bs = {k: [] for k in ("median_ratio", "E_log10", "pearson_log", "spearman", "deming_slope_log")}
    for _ in range(n_boot):
        i = rng.integers(0, len(cam), len(cam))
        if len(set(i)) < 3:
            continue
        mm = metrics_once(cam[i], las[i])
        for k in bs:
            bs[k].append(mm[k])
    for k, v in bs.items():
        v = np.array([x for x in v if np.isfinite(x)])
        m[f"{k}_lo"], m[f"{k}_hi"] = (
            (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))
            if len(v) > 50
            else (np.nan, np.nan)
        )
    return m


def paired_dE(cam, l25, l24, seed=RNG_SEED, n_boot=N_BOOT):
    """dE = E_2024 - E_2025 on the SAME conditions; probability that 2025 is closer."""
    cam, l25, l24 = (np.asarray(a, float) for a in (cam, l25, l24))
    def E(c, z):
        return np.sqrt(np.mean(np.log10(c / z) ** 2))
    d0 = E(cam, l24) - E(cam, l25)
    rng = np.random.default_rng(seed)
    d = []
    for _ in range(n_boot):
        i = rng.integers(0, len(cam), len(cam))
        d.append(E(cam[i], l24[i]) - E(cam[i], l25[i]))
    d = np.array(d)
    return {
        "dE": float(d0),
        "dE_lo": float(np.percentile(d, 2.5)),
        "dE_hi": float(np.percentile(d, 97.5)),
        "P_2025_closer": float((d > 0).mean()),
        "n": len(cam),
    }
