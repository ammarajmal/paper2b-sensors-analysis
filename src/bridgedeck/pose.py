"""Stage S4: camera displacement / rotation channels by several estimators (gate: docs/gates/S4.md).

Corner order from the detector: lb, rb, rt, lt. Units: pixels, millimetres, radians. y is the image-down axis.
"""

from __future__ import annotations

import json

import cv2
import numpy as np
import pandas as pd

from . import paths

TAG_MM = 20.0  # tag side; ledger section J (2025 campaign); owner to confirm


def intrinsics(cam: str) -> tuple[np.ndarray, np.ndarray]:
    d = json.loads((paths.REPO / "config/intrinsics_bag.json").read_text())[cam]
    return np.array(d["K"], float), np.array(d["D"], float)


def corners_of(df: pd.DataFrame) -> np.ndarray:
    return np.stack(
        [df[[f"corner{k}_x", f"corner{k}_y"]].to_numpy() for k in range(4)], axis=1
    )  # (n, 4, 2)


def undistort(c: np.ndarray, K: np.ndarray, D: np.ndarray) -> np.ndarray:
    u = cv2.undistortPoints(c.reshape(-1, 1, 2).astype(np.float64), K, D, P=K)
    return u.reshape(-1, 4, 2)


def side_len(c: np.ndarray) -> np.ndarray:
    e = np.linalg.norm(c - np.roll(c, -1, axis=1), axis=2)
    return e.mean(axis=1)


def edge_angle(c: np.ndarray) -> np.ndarray:
    v = (c[:, 1] - c[:, 0]) + (c[:, 2] - c[:, 3])  # mean of the two 'horizontal' edges
    return np.unwrap(np.arctan2(v[:, 1], v[:, 0]))


def obj_points(order: str, s: float = TAG_MM) -> np.ndarray:
    h = s / 2
    pts = np.array(
        [[-h, -h, 0], [h, -h, 0], [h, h, 0], [-h, h, 0]], float
    )  # lb, rb, rt, lt with tag y up
    return (
        pts if order == "a" else pts[::-1][[3, 2, 1, 0]] * np.array([1, -1, 1])
    )  # y-flipped (handedness) variant


def choose_order(c0: np.ndarray, K, D) -> str:
    best = None
    for order in ("a", "b"):
        ok, rv, tv = cv2.solvePnP(obj_points(order), c0, K, D, flags=cv2.SOLVEPNP_IPPE)
        pr, _ = cv2.projectPoints(obj_points(order), rv, tv, K, D)
        e = float(np.linalg.norm(pr.reshape(4, 2) - c0, axis=1).mean())
        if ok and tv[2, 0] > 0 and (best is None or e < best[1]):
            best = (order, e)
    return best[0]


def pnp_stream(c: np.ndarray, K, D, order: str):
    """Per frame: IPPE best pose, reprojection-error ratio of the two solutions, iterative refinement."""
    n = len(c)
    out = {
        k: np.full(n, np.nan)
        for k in (
            "x",
            "y",
            "z",
            "rx",
            "ry",
            "rz",
            "amb_ratio",
            "x_it",
            "y_it",
            "z_it",
            "rx_it",
            "ry_it",
            "rz_it",
        )
    }
    op = obj_points(order)
    for i in range(n):
        ci = c[i].reshape(4, 1, 2)
        n_sol, rvs, tvs, errs = cv2.solvePnPGeneric(op, ci, K, D, flags=cv2.SOLVEPNP_IPPE)
        if n_sol == 0:
            continue
        errs = np.asarray(errs, float).ravel()
        j = int(np.argmin(errs))
        out["x"][i], out["y"][i], out["z"][i] = tvs[j].ravel()
        out["rx"][i], out["ry"][i], out["rz"][i] = rvs[j].ravel()
        out["amb_ratio"][i] = (errs[1 - j] / errs[j]) if n_sol > 1 and errs[j] > 0 else np.inf
        ok, rv, tv = cv2.solvePnP(
            op, ci, K, D, rvs[j], tvs[j], useExtrinsicGuess=True, flags=cv2.SOLVEPNP_ITERATIVE
        )
        if ok:
            out["x_it"][i], out["y_it"][i], out["z_it"][i] = tv.ravel()
            out["rx_it"][i], out["ry_it"][i], out["rz_it"][i] = rv.ravel()
    return out


def stream_channels(g: pd.DataFrame, cam: str) -> pd.DataFrame:
    """All estimators for one stream (rows = admitted frames, time-ordered)."""
    K, D = intrinsics(cam)
    c = corners_of(g)
    cu = undistort(c, K, D)
    s_med = np.median(side_len(cu))
    mm_px = TAG_MM / s_med
    cen_u = cu.mean(axis=1)
    cen_det = g[["centroid_x", "centroid_y"]].to_numpy()
    out = pd.DataFrame({"frame_idx": g.frame_idx.to_numpy(), "t_s": g.timestamp_s.to_numpy()})
    out["P0_x_px"], out["P0_y_px"] = (
        cen_det[:, 0] - np.median(cen_det[:, 0]),
        cen_det[:, 1] - np.median(cen_det[:, 1]),
    )
    out["P1_x_mm"], out["P1_y_mm"] = (
        (cen_u[:, 0] - np.median(cen_u[:, 0])) * mm_px,
        (cen_u[:, 1] - np.median(cen_u[:, 1])) * mm_px,
    )
    sc = TAG_MM / side_len(cu)
    out["P2_x_mm"], out["P2_y_mm"] = (
        (cen_u[:, 0] - np.median(cen_u[:, 0])) * sc,
        (cen_u[:, 1] - np.median(cen_u[:, 1])) * sc,
    )
    order = choose_order(c[0], K, D)
    p = pnp_stream(c, K, D, order)
    for k in ("x", "y", "z"):
        out[f"P3_{k}_mm"] = p[k] - np.nanmedian(p[k])
        out[f"P4_{k}_mm"] = p[f"{k}_it"] - np.nanmedian(p[f"{k}_it"])
    for k in ("rx", "ry", "rz"):
        out[f"P3_{k}_rad"] = p[k] - np.nanmedian(p[k])
        out[f"P4_{k}_rad"] = p[f"{k}_it"] - np.nanmedian(p[f"{k}_it"])
    out["P3_amb_ratio"] = p["amb_ratio"]
    ang = edge_angle(cu)
    out["P5_roll_rad"] = ang - np.median(ang)
    cm = c.mean(axis=1)
    cmu = undistort(c, K, D).mean(axis=1)
    out["P6_x_mm"], out["P6_y_mm"] = (
        (cmu[:, 0] - np.median(cmu[:, 0])) * mm_px,
        (cmu[:, 1] - np.median(cmu[:, 1])) * mm_px,
    )
    out.attrs.update(
        order=order,
        mm_per_px=mm_px,
        side_px=float(s_med),
        z_med_mm=float(np.nanmedian(p["z"])),
        cm_unused=float(cm.mean()),
    )
    return out


def line_amplitude(
    t: np.ndarray, y: np.ndarray, f0: float, half: float = 0.05
) -> tuple[float, float]:
    """Sinusoid amplitude at the best frequency within +/- half of f0 (least squares on irregular stamps)."""
    m = np.isfinite(y)
    t, y = t[m], y[m] - np.nanmean(y[m])
    best = (0.0, f0)
    for f in np.linspace(f0 - half, f0 + half, 21):
        X = np.column_stack([np.cos(2 * np.pi * f * t), np.sin(2 * np.pi * f * t)])
        cf, *_ = np.linalg.lstsq(X, y, rcond=None)
        a = float(np.hypot(*cf))
        if a > best[0]:
            best = (a, float(f))
    return best
