"""S2c: candidate detection-admissibility rules (docs/gates/S2c.md). Rules fixed before the analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

KEYS = ["condition", "camera"]


def add_speed(df: pd.DataFrame) -> pd.DataFrame:
    """Per-frame centroid speed (px/frame), from the nearest detected neighbours on each side (defined across misses)."""
    out = []
    for _, g in df.sort_values("frame_idx").groupby(KEYS):
        g = g.copy()
        det = g[g.detected]
        i, x, y = (
            det.frame_idx.to_numpy(float),
            det.centroid_x.to_numpy(),
            det.centroid_y.to_numpy(),
        )
        f = g.frame_idx.to_numpy(float)
        vx = np.interp(f, (i[1:] + i[:-1]) / 2, np.diff(x) / np.diff(i))
        vy = np.interp(f, (i[1:] + i[:-1]) / 2, np.diff(y) / np.diff(i))
        g["speed"] = np.hypot(vx, vy)
        side = np.hypot(det.corner0_x - det.corner1_x, det.corner0_y - det.corner1_y).median()
        g["side_px"] = side
        out.append(g)
    return pd.concat(out)


def stream_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (c, cam), g in df.groupby(KEYS):
        n, k = len(g), int(g.detected.sum())
        p = k / n
        z = 1.6449
        wl = (p + z * z / (2 * n) - z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (
            1 + z * z / n
        )
        rows.append(
            dict(
                condition=c,
                camera=cam,
                n=n,
                detected=k,
                completeness=p,
                wilson_lb=wl,
                max_speed=g.speed.max(),
                speed_det_max=g.loc[g.detected, "speed"].max(),
                side_px=g.side_px.iloc[0],
                miss=n - k,
            )
        )
    return pd.DataFrame(rows)


def ledger_class(row) -> str:
    if row.condition == "e20_320rpm":
        return "diagnostic" if row.camera == "cam3" else "rejected"
    return "admissible"


def r1_threshold(side_px: float) -> float:
    return side_px / 10.0


def r2_threshold(st: pd.DataFrame) -> float:
    clean = st[st.miss == 0].speed_det_max.max()
    first_fail = st[st.miss > 0].max_speed.min()
    return float((clean + first_fail) / 2)


def cluster_boot_logistic(fr: pd.DataFrame, p: float, n_boot=2000, seed=11):
    conds = fr.condition.unique()
    rng = np.random.default_rng(seed)

    def thr(d):
        m = LogisticRegression(C=1e6, max_iter=2000).fit(
            d.speed.to_numpy()[:, None], (~d.detected).astype(int)
        )
        b, a = m.coef_[0][0], m.intercept_[0]
        return (np.log(p / (1 - p)) - a) / b if b > 0 else np.nan

    est = thr(fr)
    bs = []
    for _ in range(n_boot):
        pick = rng.choice(conds, len(conds))
        d = pd.concat([fr[fr.condition == c] for c in pick])
        if (~d.detected).sum() < 5:
            continue
        bs.append(thr(d))
    bs = np.array([b for b in bs if np.isfinite(b)])
    return est, (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), len(bs)) if len(
        bs
    ) else (np.nan, np.nan, 0)


def hampel_flags(df: pd.DataFrame, k: float = 3.0) -> pd.Series:
    flag = pd.Series(False, index=df.index)
    for _, g in df[df.detected].groupby(KEYS):
        med = g.decision_margin.median()
        mad = 1.4826 * (g.decision_margin - med).abs().median()
        flag.loc[g.index[g.decision_margin < med - k * mad]] = True
    return flag
