"""Stage S1: per-camera frame-timing census straight from the bags (images are never decoded).

Per image message we keep the header stamp, the bag record stamp, header seq, payload size and a
payload CRC32 (byte-identical consecutive frames = duplicates)."""

from __future__ import annotations

import zlib
from pathlib import Path

import numpy as np
import pandas as pd
from rosbags.highlevel import AnyReader

from . import paths


def read_bag(bag: Path) -> dict[str, dict[str, np.ndarray]]:
    rec: dict[str, dict[str, list]] = {}
    with AnyReader([bag]) as r:
        conns = [c for c in r.connections if c.msgtype.endswith("Image")]
        for c, t, raw in r.messages(connections=conns):
            m = r.deserialize(raw, c.msgtype)
            d = rec.setdefault(c.topic.split("/")[1], dict(h=[], r=[], s=[], n=[], k=[]))
            d["h"].append(m.header.stamp.sec * 10**9 + m.header.stamp.nanosec)
            d["r"].append(t)
            d["s"].append(m.header.seq)
            d["n"].append(len(m.data))
            d["k"].append(zlib.crc32(bytes(m.data)))
    return {cam: {k: np.asarray(v) for k, v in d.items()} for cam, d in rec.items()}


def summarize(set_name: str, bag: str, cam: str, d: dict[str, np.ndarray]) -> dict:
    h, r, s, k = (d[x].astype(np.int64) if x != "k" else d[x] for x in ("h", "r", "s", "k"))
    dh = np.diff(h) / 1e6
    med = float(np.median(dh))
    lat = (r - h) / 1e6
    return dict(
        set=set_name,
        bag=bag,
        cam=cam,
        n=len(h),
        dur_hdr_s=(h[-1] - h[0]) / 1e9,
        rate_hdr_hz=1000 / med,
        rate_mean_hz=(len(h) - 1) / ((h[-1] - h[0]) / 1e9),
        dt_sd_ms=dh.std(),
        dt_max_ms=dh.max(),
        dt_min_ms=dh.min(),
        n_gap_gt1p5=int((dh > 1.5 * med).sum()),
        n_gap_gt2p5=int((dh > 2.5 * med).sum()),
        lat_mean_ms=lat.mean(),
        lat_sd_ms=lat.std(),
        rec_eq_hdr=bool(np.all(r == h)),
        seq_missing=int(np.clip(np.diff(s) - 1, 0, None).sum()),
        hdr_nonmono=int((dh <= 0).sum()),
        dup_consecutive_payload=int((k[1:] == k[:-1]).sum()),
    )


def run(set_name: str, limit: int | None = None) -> pd.DataFrame:
    root = Path(paths.load()["bags"][set_name])
    bags = sorted(root.rglob("*.bag"))[:limit]
    out = paths.out_dir("s1_census", set_name)
    rows = []
    for b in bags:
        for cam, d in sorted(read_bag(b).items()):
            np.savez_compressed(
                out / f"{b.stem}__{cam}.npz",
                hdr=d["h"],
                rec=d["r"],
                seq=d["s"],
                size=d["n"],
                crc=d["k"],
            )
            rows.append(summarize(set_name, b.stem, cam, d))
    df = pd.DataFrame(rows)
    df.to_csv(out / "census_summary.csv", index=False)
    return df
