"""Gate checks. Criteria are fixed in docs/gates/*.md before the run."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from . import paths

SETMAP = {"wtt_main": "wtt", "wtt_5sec": "wtt_5sec", "static": "static"}
TOL = {"rate_hz": 1e-3, "lat_ms": 0.05}


def gate_s1(sets=("wtt_main", "wtt_5sec")) -> pd.DataFrame:
    """Compare S1 census with the earlier independent extraction (timing_per_camera.csv)."""
    ref = pd.read_csv(paths.load()["frozen"]["prior_timing_extraction"])
    ref = ref.rename(columns={"set": "set_ref"})
    ref["set_ref"] = ref["set_ref"].str.lower()
    ref["bag"] = ref["bag"].map(lambda p: Path(p).stem)
    ref["cam"] = "sony_cam" + ref["cam"].astype(str)
    rows = []
    for s in sets:
        new = pd.read_csv(Path(paths.load()["outputs"]) / "s1_census" / s / "census_summary.csv")
        new["set_ref"] = SETMAP[s]
        m = new.merge(ref, on=["set_ref", "bag", "cam"], how="left", suffixes=("", "_ref"))
        m["ok_n"] = m["n"] == m["n_img"]
        m["ok_rate"] = (m["rate_mean_hz"] - m["rate_hdr_hz_ref"]).abs() < TOL["rate_hz"]
        m["ok_dup"] = m["dup_consecutive_payload"] == m["dup_payload"]
        m["ok_lat"] = (m["lat_mean_ms"] - m["lat_mean_ms_ref"]).abs() < TOL["lat_ms"]
        m["ok"] = m[["ok_n", "ok_rate", "ok_dup", "ok_lat"]].all(axis=1)
        rows.append(
            m[
                [
                    "set",
                    "bag",
                    "cam",
                    "n",
                    "n_img",
                    "rate_mean_hz",
                    "rate_hdr_hz_ref",
                    "dup_consecutive_payload",
                    "dup_payload",
                    "lat_mean_ms",
                    "lat_mean_ms_ref",
                    "ok_n",
                    "ok_rate",
                    "ok_dup",
                    "ok_lat",
                    "ok",
                ]
            ]
        )
    out = pd.concat(rows, ignore_index=True)
    return out


def gate_s2(parquet: Path) -> tuple[dict, pd.DataFrame]:
    """Compare S2 detections with the frozen detections (criteria in docs/gates/S2.md)."""
    new = pd.read_parquet(parquet)
    fz = pd.read_csv(paths.load()["frozen"]["per_frame_detections"])
    m = new.merge(fz, on=["condition", "camera", "frame_idx"], how="left", suffixes=("", "_fz"))
    out = {"frames_new": len(new), "frames_without_frozen_row": int(m["detected_fz"].isna().sum())}
    m = m[m["detected_fz"].notna()]
    out["detected_flag_equal_pct"] = float(
        (m["detected"] == m["detected_fz"].astype(bool)).mean() * 100
    )
    out["timestamp_diff_max_s"] = float((m["timestamp_s"] - m["timestamp_s_fz"]).abs().max())
    both = m[m["detected"] & m["detected_fz"].astype(bool)].copy()
    # corners are compared as sets (order of the four corners can differ between bindings)
    d = np.full(len(both), np.nan)
    for j, (_, r) in enumerate(both.iterrows()):
        a = np.array([[r[f"corner{k}_x"], r[f"corner{k}_y"]] for k in range(4)])
        b = np.array([[r[f"corner{k}_x_fz"], r[f"corner{k}_y_fz"]] for k in range(4)])
        d[j] = max(np.linalg.norm(a - x, axis=1).min() for x in b)
    both["corner_diff_px"] = d
    both["centre_diff_px"] = np.hypot(
        both["centroid_x"] - both["centroid_x_fz"], both["centroid_y"] - both["centroid_y_fz"]
    )
    out.update(
        both_detected=len(both),
        corner_diff_median=float(np.median(d)),
        corner_diff_p99=float(np.percentile(d, 99)),
        corner_diff_p999=float(np.percentile(d, 99.9)),
        corner_diff_max=float(d.max()),
        centre_diff_median=float(both["centre_diff_px"].median()),
        margin_diff_median=float(
            (both["decision_margin"] - both["decision_margin_fz"]).abs().median()
        ),
    )
    out["pass_a_detected_ge_99.9pct"] = out["detected_flag_equal_pct"] >= 99.9
    out["pass_b_loose_median_le_0.02_p99_le_0.1"] = (
        out["corner_diff_median"] <= 0.02 and out["corner_diff_p99"] <= 0.1
    )
    out["info_b_tight_median_le_1e-3_p999_le_0.01"] = (
        out["corner_diff_median"] <= 1e-3 and out["corner_diff_p999"] <= 0.01
    )
    flips = m[m["detected"] != m["detected_fz"].astype(bool)][
        ["condition", "camera", "frame_idx", "detected", "detected_fz", "raw_num_detections"]
    ]
    return out, flips
