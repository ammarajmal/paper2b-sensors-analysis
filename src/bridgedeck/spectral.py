"""Stage S3: per-camera spectra on native timestamps (gate: docs/gates/S3.md)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from astropy.timeseries import LombScargle
from scipy.optimize import minimize_scalar
from scipy.signal import lombscargle

BAND = (0.5, 10.0)


def prep(t: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    t = np.asarray(t, float) - t[0]
    y = np.asarray(y, float)
    y = y - np.median(y)
    return t, y - np.polyval(np.polyfit(t, y, 1), t)


def grid(T: float) -> tuple[np.ndarray, float]:
    ri = 1.0 / T
    return np.arange(BAND[0], BAND[1] + ri / 20, ri / 10), ri


def ls_scipy(t, y, f):
    return lombscargle(t, y, 2 * np.pi * f, precenter=True, normalize=True)


def peak(t, y, f, power_fn=ls_scipy):
    p = power_fn(t, y, f)
    k = int(np.argmax(p))
    return float(f[k]), p


def top_peaks(f, p, n=3, min_sep=0.1):
    order, out = np.argsort(-p), []
    for k in order:
        if all(abs(f[k] - o) > min_sep for o, _ in out):
            out.append((float(f[k]), float(p[k])))
        if len(out) == n:
            break
    return out


def fit_sinusoid_freq(t, y, f0, ri):
    """Least-squares refinement of the frequency within +/- ri of f0."""

    def sse(fr):
        X = np.column_stack(
            [np.cos(2 * np.pi * fr * t), np.sin(2 * np.pi * fr * t), np.ones_like(t)]
        )
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(np.sum((y - X @ c) ** 2))

    r = minimize_scalar(sse, bounds=(f0 - ri, f0 + ri), method="bounded", options={"xatol": 1e-7})
    return float(r.x)


def boot_interval(t, y, f_hat, ri, n_boot=200, seed=5):
    X = np.column_stack(
        [np.cos(2 * np.pi * f_hat * t), np.sin(2 * np.pi * f_hat * t), np.ones_like(t)]
    )
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    fit, res = X @ c, y - X @ c
    rng = np.random.default_rng(seed)
    dt = np.median(np.diff(t))
    bl = max(int(1.0 / dt), 1)
    nb = max(len(y) // bl, 1)
    out = []
    for _ in range(n_boot):
        idx = rng.integers(0, nb, nb)
        r = np.concatenate([res[i * bl : (i + 1) * bl] for i in idx])
        yb = fit[: len(r)] + r
        out.append(fit_sinusoid_freq(t[: len(r)], yb, f_hat, ri))
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def baluev_fap(t, y, f, power_at_peak):
    ls = LombScargle(t, y, fit_mean=True, center_data=True)
    return float(
        ls.false_alarm_probability(
            power_at_peak, method="baluev", minimum_frequency=f[0], maximum_frequency=f[-1]
        )
    )


def stream_series(det: pd.DataFrame, cond: str, cam: str, stamp: str = "timestamp_s"):
    g = det[
        (det.condition == cond) & (det.camera == cam) & det.detected & (det.decision_margin >= 30)
    ].sort_values("frame_idx")
    t = g[stamp].to_numpy() if stamp != "stamp_hdr_ns" else g[stamp].to_numpy() / 1e9
    return g.frame_idx.to_numpy(), t, g.centroid_y.to_numpy()


def interp60(t, y, fs=60.0):
    g = np.arange(t[0], t[-1], 1.0 / fs)
    return g, np.interp(g, t, y)
