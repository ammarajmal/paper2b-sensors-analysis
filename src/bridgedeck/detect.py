"""Stage S2: AprilTag detection on the wind-tunnel bags (gate: docs/gates/S2.md).

Decode path (pinned in the gate): JPEG -> cv2.IMREAD_COLOR (BGR) -> grey = (299*R + 587*G + 114*B) // 1000.
Detector: official AprilRobotics v3.4.5 wrapper, tag36h11, threads=1, maxhamming=0, decimate=1.0, blur=0.0, refine_edges=True.
Both the driver header stamp and the bag record stamp are stored.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from rosbags.highlevel import AnyReader

from . import paths

DETECTOR_KW = {"threads": 1, "maxhamming": 0, "decimate": 1.0, "blur": 0.0, "refine_edges": True}
EXPECTED_ID = 0
COLS = (
    [
        "condition",
        "camera",
        "frame_idx",
        "timestamp_s",
        "stamp_hdr_ns",
        "stamp_rec_ns",
        "detected",
        "tag_id",
        "decision_margin",
        "hamming",
        "centroid_x",
        "centroid_y",
    ]
    + [f"corner{k}_{a}" for k in range(4) for a in "xy"]
    + ["raw_num_detections"]
)


def to_grey(buf: bytes) -> np.ndarray:
    bgr = cv2.imdecode(np.frombuffer(buf, np.uint8), cv2.IMREAD_COLOR)
    b, g, r = (bgr[..., i].astype(np.int64) for i in range(3))
    return ((r * 299 + g * 587 + b * 114) // 1000).astype(np.uint8)


def detect_stream(args: tuple[str, str, str]) -> pd.DataFrame:
    bag, cam, cond = args
    from apriltag import apriltag  # imported here: one detector per process

    det = apriltag("tag36h11", **DETECTOR_KW)
    rows = []
    with AnyReader([Path(bag)]) as r:
        first_rec = min(
            t
            for c, t, _ in r.messages(
                connections=[c for c in r.connections if c.msgtype.endswith("CompressedImage")]
            )
        )
        conns = [c for c in r.connections if c.topic == f"/sony_{cam}/image_raw/compressed"]
        for i, (c, t, raw) in enumerate(r.messages(connections=conns)):
            m = r.deserialize(raw, c.msgtype)
            hdr = m.header.stamp.sec * 10**9 + m.header.stamp.nanosec
            d = det.detect(to_grey(bytes(m.data)))
            row = dict.fromkeys(COLS, np.nan)
            row.update(
                condition=cond,
                camera=cam,
                frame_idx=i,
                timestamp_s=(t - first_rec) / 1e9,
                stamp_hdr_ns=hdr,
                stamp_rec_ns=t,
                detected=False,
                raw_num_detections=len(d),
            )
            ok = [x for x in d if x["id"] == EXPECTED_ID]
            if ok:
                x = ok[0]
                lb = np.asarray(x["lb-rb-rt-lt"], float)
                row.update(
                    detected=True,
                    tag_id=x["id"],
                    decision_margin=x["margin"],
                    hamming=x["hamming"],
                    centroid_x=x["center"][0],
                    centroid_y=x["center"][1],
                )
                for k in range(4):
                    row[f"corner{k}_x"], row[f"corner{k}_y"] = lb[k]
            rows.append(row)
    return pd.DataFrame(rows, columns=COLS)


def run(set_name: str, conditions: list[str], workers: int = 9) -> pd.DataFrame:
    root = Path(paths.load()["bags"][set_name])
    jobs = []
    for cond in conditions:
        bag = next(root.rglob(f"{cond}*.bag"))
        jobs += [(str(bag), cam, cond) for cam in ("cam1", "cam2", "cam3")]
    out = paths.out_dir("s2_detect", set_name)
    with ProcessPoolExecutor(workers) as ex:
        frames = list(ex.map(detect_stream, jobs))
    df = pd.concat(frames, ignore_index=True)
    df.to_parquet(out / f"detections_{'_'.join(conditions)}.parquet", index=False)
    return df
