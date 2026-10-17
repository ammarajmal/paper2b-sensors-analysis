"""S2b (docs/gates/S2b.md): raw vs ECC-compensated marker centroid_y at e0, e7, e14, cam1-3. One process per stream."""
import os, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import cv2, numpy as np, pandas as pd
cv2.setNumThreads(1)
from rosbags.highlevel import AnyReader
from bridgedeck import paths, spectral as S
from bridgedeck.detect import to_grey

R = paths.REPO / "results"; O = Path(paths.load()["outputs"])
CONDS = ["e0_0rpm", "e7_90rpm", "e14_200rpm"]; CAMS = ["cam1", "cam2", "cam3"]
CRIT = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-6)
det = pd.read_parquet(O / "s2_detect/wtt_main/detections_ALL21.parquet")


def small(g):
    return cv2.resize(g, (g.shape[1] // 2, g.shape[0] // 2), interpolation=cv2.INTER_AREA)


def ecc(ref, cur, mask):
    w = np.eye(2, 3, dtype=np.float32)
    try:
        _, w = cv2.findTransformECC(ref, cur, w, cv2.MOTION_AFFINE, CRIT, mask, 5)
        return w, True
    except cv2.error:
        return np.eye(2, 3, dtype=np.float32), False


def run_stream(args):
    cond, cam = args
    d = det[(det.condition == cond) & (det.camera == cam)].sort_values("frame_idx").reset_index(drop=True)
    bag = next(Path(paths.load()["bags"]["wtt_main"]).rglob(f"{cond}*.bag"))
    rows = []; ref = None
    with AnyReader([bag]) as r:
        conns = [c for c in r.connections if c.topic == f"/sony_{cam}/image_raw/compressed"]
        for i, (c, t, raw) in enumerate(r.messages(connections=conns)):
            if os.environ.get("S2B_LIMIT") and i >= int(os.environ["S2B_LIMIT"]):
                break
            g = small(to_grey(bytes(r.deserialize(raw, c.msgtype).data)))
            q = d.iloc[i]; assert q.frame_idx == i
            out = dict(condition=cond, camera=cam, frame_idx=i, t=q.timestamp_s, cy=q.centroid_y, cx=q.centroid_x, detected=bool(q.detected))
            if ref is None:
                ref = g
            if not q.detected:
                rows.append(out); continue
            xs = np.array([q[f"corner{k}_x"] for k in range(4)]) / 2; ys = np.array([q[f"corner{k}_y"] for k in range(4)]) / 2
            m = np.full(g.shape, 255, np.uint8); pad = 10  # 20 px at full resolution
            m[max(0, int(ys.min()) - pad):int(ys.max()) + pad + 1, max(0, int(xs.min()) - pad):int(xs.max()) + pad + 1] = 0
            w, ok = ecc(ref, g, m)
            # warp maps reference coordinates to current coordinates; compensated marker = inverse warp of the current marker
            A = np.vstack([w, [0, 0, 1]]).astype(np.float64); Ai = np.linalg.inv(A)
            p = Ai @ np.array([q.centroid_x / 2, q.centroid_y / 2, 1.0])
            out.update(cy_C=p[1] * 2, ok_C=ok, ty_C=w[1, 2] * 2)
            # placebo: border strip farthest from the tag (left or right 100 px at full resolution = 50 px)
            m2 = np.zeros(g.shape, np.uint8); far_left = (xs.mean() > g.shape[1] / 2)
            if far_left: m2[:, :50] = 255
            else: m2[:, -50:] = 255
            w2, ok2 = ecc(ref, g, m2)
            A2 = np.vstack([w2, [0, 0, 1]]).astype(np.float64); p2 = np.linalg.inv(A2) @ np.array([q.centroid_x / 2, q.centroid_y / 2, 1.0])
            out.update(cy_R=p2[1] * 2, ok_R=ok2, ty_R=w2[1, 2] * 2)
            rows.append(out)
    df = pd.DataFrame(rows); df.to_parquet(O / (("smoke_" if os.environ.get("S2B_LIMIT") else "") + f"s2b_{cond}_{cam}.parquet")); return cond, cam, len(df)


if __name__ == "__main__":
    jobs = [(c, k) for c in CONDS for k in CAMS if not (O / f"s2b_{c}_{k}.parquet").exists()]   # resume: finished streams are kept
    print("streams to do:", len(jobs), flush=True)
    with ProcessPoolExecutor(max_workers=4) as ex:
        for res in ex.map(run_stream, jobs):
            print("done", res, flush=True)
