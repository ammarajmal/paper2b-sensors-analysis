"""S11 (docs/gates/S11.md): raw spectra of 60, 80, 110, 140 RPM, camera vs laser 2025."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
from bridgedeck import laser, paths, pose, spectral as S
R = paths.REPO / "results"; O = Path(paths.load()["outputs"]); FH, FA = 1.4318, 3.0982
fr = pd.read_parquet(O / "s4_pose_channels_by_frame.parquet")
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.session == "y2025")].set_index("rpm")
sess = laser.SESSIONS["y2025"]; b = laser.bias(sess); (R / "figures").mkdir(exist_ok=True)
def lineamp(t, y, f): return pose.line_amplitude(np.asarray(t, float), np.asarray(y, float), f, 0.08)[0]
def fft(y, fs=laser.FS):
    y = y - y.mean(); w = np.hanning(len(y)); n = 8 * len(y); sp = np.abs(np.fft.rfft(y * w, n)) * 2 / w.sum(); f = np.fft.rfftfreq(n, 1 / fs); return f, sp
rows = []
import os
for rpm in [int(x) for x in os.environ.get("S11_RPMS", "60,80,110,140").split(",")]:
    cond = [c for c in fr.condition.unique() if c.endswith(f"_{rpm}rpm")][0]
    v = laser.load_volts(sess, laser.disk_name(sess, P.loc[rpm, "file"])); ch = laser.channels(v, b, sess); tl = np.arange(len(v)) / laser.FS
    fig, ax = plt.subplots(2, 2, figsize=(13, 8))
    for j, (q, camcol, lasy, unit, f0) in enumerate((("heave", "P1_y_mm", ch["heave_mm"], "mm", FH), ("pitch", "P5_roll_rad", ch["pitch_rad"], "rad", FA))):
        a = ax[0, j]; fl, sl = fft(lasy); m = (fl >= 0.5) & (fl <= 10); a.plot(fl[m], sl[m], "k", lw=1.4, label="laser 2025")
        r = dict(rpm=rpm, quantity=q, laser_rms=float(np.std(lasy)), laser_line=lineamp(tl, lasy, f0), laser_peak_hz=float(fl[m][np.argmax(sl[m])]), laser_peak_amp=float(sl[m].max()))
        for cam, col in (("cam1", "C0"), ("cam2", "C1"), ("cam3", "C2")):
            d = fr[(fr.condition == cond) & (fr.camera == cam)].sort_values("t_s"); t, y = d.t_s.to_numpy(), d[camcol].to_numpy()
            tt, yy = S.prep(t, y); f = np.arange(0.5, 10, 0.01); p = S.ls_scipy(tt, yy, f)
            # amplitude spectrum from least squares at each f (same estimator as the line amplitude)
            am = np.array([np.hypot(*np.linalg.lstsq(np.column_stack([np.cos(2*np.pi*x*t), np.sin(2*np.pi*x*t), np.ones_like(t)]), y - y.mean(), rcond=None)[0][:2]) for x in f])
            a.plot(f, am, color=col, lw=1, alpha=.85, label=cam); r[f"{cam}_rms"] = float(np.std(y)); r[f"{cam}_line"] = lineamp(t, y, f0); r[f"{cam}_peak_hz"] = float(f[np.argmax(am)]); r[f"{cam}_peak_amp"] = float(am.max())
        for x in (FH, FA): a.axvline(x, color="r", ls=":", lw=1)
        a.set(yscale="log", xlabel="Hz", ylabel=f"amplitude ({unit})", title=f"{rpm} RPM {q}"); a.legend(fontsize=7); a.grid(alpha=.3)
        b2 = ax[1, j]; d1 = fr[(fr.condition == cond) & (fr.camera == "cam1")].sort_values("t_s"); k = d1.t_s < 8
        b2.plot(d1.t_s[k], d1[camcol][k] - d1[camcol].mean(), "C0", lw=.8, label="cam1"); k2 = tl < 8; b2.plot(tl[k2], lasy[k2] - lasy.mean(), "k", lw=.5, alpha=.7, label="laser"); b2.set(xlabel="s", title=f"{rpm} RPM {q}, first 8 s"); b2.legend(fontsize=7)
        rows.append(r)
    fig.tight_layout(); fig.savefig(R / "figures" / f"s11_spectra_{rpm}.png", dpi=90); plt.close(fig)
T = pd.DataFrame(rows); T["cam_mean_line"] = T[[f"cam{i}_line" for i in (1, 2, 3)]].mean(axis=1); T["line_ratio_cam_over_laser"] = T.cam_mean_line / T.laser_line
T["laser_line_var_share"] = (T.laser_line / np.sqrt(2)) ** 2 / T.laser_rms ** 2; T["cam1_line_var_share"] = (T.cam1_line / np.sqrt(2)) ** 2 / T.cam1_rms ** 2
T.to_csv(R / ("s11_spectra.csv" if not os.environ.get("S11_RPMS") else "s11b_spectra.csv"), index=False, float_format="%.6g")
pd.set_option("display.width", 250); print(T[["rpm", "quantity", "laser_peak_hz", "laser_peak_amp", "laser_line", "cam1_peak_hz", "cam1_peak_amp", "cam3_peak_hz", "cam3_peak_amp", "cam_mean_line", "line_ratio_cam_over_laser", "laser_line_var_share", "cam1_line_var_share"]].round(4).to_string(index=False))
