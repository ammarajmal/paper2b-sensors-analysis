"""Gate checks. Criteria are fixed in docs/gates/*.md before the run."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import paths

SETMAP = {"wtt_main": "wtt", "wtt_5sec": "wtt_5sec", "static": "static"}
TOL = {"rate_hz": 1e-3, "lat_ms": 0.05}


def gate_s1(sets=("wtt_main", "wtt_5sec")) -> pd.DataFrame:
    """Compare S1 census with the earlier independent extraction (timing_per_camera.csv)."""
    ref = pd.read_csv(paths.load()["frozen"]["prior_timing_extraction"])
    ref["set"] = ref["set"].str.lower()
    ref["bag"] = ref["bag"].map(lambda p: Path(p).stem)
    ref["cam"] = "sony_cam" + ref["cam"].astype(str)
    rows = []
    for s in sets:
        new = pd.read_csv(Path(paths.load()["outputs"]) / "s1_census" / s / "census_summary.csv")
        new["set_ref"] = SETMAP[s]
        m = new.merge(ref, left_on=["set_ref", "bag", "cam"], right_on=["set", "bag", "cam"],
                      how="left", suffixes=("", "_ref"))
        m["ok_n"] = m["n"] == m["n_img"]
        m["ok_rate"] = (m["rate_mean_hz"] - m["rate_hdr_hz_ref"]).abs() < TOL["rate_hz"]
        m["ok_dup"] = m["dup_consecutive_payload"] == m["dup_payload"]
        m["ok_lat"] = (m["lat_mean_ms"] - m["lat_mean_ms_ref"]).abs() < TOL["lat_ms"]
        m["ok"] = m[["ok_n", "ok_rate", "ok_dup", "ok_lat"]].all(axis=1)
        rows.append(m[["set", "bag", "cam", "n", "n_img", "rate_mean_hz", "rate_hdr_hz_ref",
                       "dup_consecutive_payload", "dup_payload", "lat_mean_ms", "lat_mean_ms_ref",
                       "ok_n", "ok_rate", "ok_dup", "ok_lat", "ok"]])
    out = pd.concat(rows, ignore_index=True)
    return out
