"""Stage S1: per-camera frame timing census, independent of the earlier g2 extraction.
Reads each bag once (messages only; images are never decoded) and records, per image message:
header stamp, bag record stamp, header seq, payload size, payload CRC32 (duplicate-frame detection).
Writes one NPZ per (bag, camera) plus census_summary.csv. Inputs are read-only.
Usage: census.py <set: wtt_main|wtt_5sec|static> <out_dir>"""
import sys, zlib, csv, glob, os, json, time
from pathlib import Path
import numpy as np, yaml
from rosbags.highlevel import AnyReader

cfg = yaml.safe_load(open(Path(__file__).parents[1] / "config/paths.yaml"))
which, out = sys.argv[1], Path(sys.argv[2]); (out / "series").mkdir(parents=True, exist_ok=True)
bags = sorted(glob.glob(cfg["bags"][which] + "/**/*.bag", recursive=True))
rows = []
for b in bags:
    t0 = time.time(); name = Path(b).stem
    rec = {}; 
    with AnyReader([Path(b)]) as r:
        conns = [c for c in r.connections if c.msgtype.endswith("Image") or c.msgtype.endswith("CompressedImage")]
        for c, t, raw in r.messages(connections=conns):
            m = r.deserialize(raw, c.msgtype)
            cam = c.topic.split("/")[1]
            d = rec.setdefault(cam, dict(h=[], r=[], s=[], n=[], k=[]))
            d["h"].append(m.header.stamp.sec * 10**9 + m.header.stamp.nanosec); d["r"].append(t)
            d["s"].append(m.header.seq); d["n"].append(len(m.data)); d["k"].append(zlib.crc32(bytes(m.data)))
    for cam, d in sorted(rec.items()):
        h = np.array(d["h"], np.int64); r_ = np.array(d["r"], np.int64); s = np.array(d["s"], np.int64); k = np.array(d["k"], np.uint32)
        np.savez_compressed(out / "series" / f"{name}__{cam}.npz", hdr=h, rec=r_, seq=s, size=np.array(d["n"]), crc=k)
        dh = np.diff(h) / 1e6; dr = np.diff(r_) / 1e6; lat = (r_ - h) / 1e6
        med = np.median(dh)
        rows.append(dict(set=which, bag=name, cam=cam, n=len(h),
            dur_hdr_s=(h[-1] - h[0]) / 1e9, rate_hdr_hz=1000 / med, rate_mean_hz=(len(h) - 1) / ((h[-1] - h[0]) / 1e9),
            dt_sd_ms=dh.std(), dt_max_ms=dh.max(), dt_min_ms=dh.min(),
            n_gap_gt1p5=int((dh > 1.5 * med).sum()), n_gap_gt2p5=int((dh > 2.5 * med).sum()),
            lat_mean_ms=lat.mean(), lat_sd_ms=lat.std(), rec_eq_hdr=bool(np.all(r_ == h)),
            seq_missing=int((np.diff(s) - 1).clip(min=0).sum()), hdr_nonmono=int((dh <= 0).sum()),
            dup_consecutive_payload=int((k[1:] == k[:-1]).sum())))
    print(f"{name}: {len(rec)} cams, {time.time()-t0:.0f}s", flush=True)
keys = list(rows[0]); 
with open(out / "census_summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
print("DONE", len(bags), "bags", len(rows), "streams")
