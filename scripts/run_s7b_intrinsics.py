"""S7b intrinsics sensitivity (deterministic, NOT an uncertainty): change in line amplitude when distortion is zeroed and fx, fy are changed by +/-5%."""
import numpy as np, pandas as pd
from pathlib import Path
from bridgedeck import paths, pose
R = paths.REPO / "results"; O = Path(paths.load()["outputs"]); FH, FA = 1.4318, 3.0982
det = pd.read_parquet(O / "s2_detect/wtt_main/detections_ALL21.parquet"); rows = []
for cond in ("e7_90rpm", "e14_200rpm", "e11_140rpm"):
    for cam in ("cam1", "cam2", "cam3"):
        g = det[(det.condition == cond) & (det.camera == cam) & det.detected & (det.decision_margin >= 30)].sort_values("frame_idx")
        K0, D0 = pose.intrinsics(cam); c = pose.corners_of(g); t = g.timestamp_s.to_numpy()
        def amps(K, D):
            cu = pose.undistort(c, K, D); cy = cu.mean(axis=1)[:, 1]; y1 = (cy - np.median(cy)) * (pose.TAG_MM / np.median(pose.side_len(cu)))
            ang = pose.edge_angle(cu); return pose.line_amplitude(t, y1, FH, 0.08)[0], pose.line_amplitude(t, ang - np.median(ang), FA, 0.08)[0]
        base = amps(K0, D0)
        for name, K, D in (("D_zero", K0, np.zeros_like(D0)), ("fx_fy_+5%", K0 * np.array([[1.05, 1, 1], [1, 1.05, 1], [1, 1, 1]]), D0), ("fx_fy_-5%", K0 * np.array([[.95, 1, 1], [1, .95, 1], [1, 1, 1]]), D0)):
            a = amps(K, D); rows.append(dict(condition=cond, camera=cam, variant=name, d_rel_heave=a[0] / base[0] - 1, d_rel_pitch=a[1] / base[1] - 1))
d = pd.DataFrame(rows); d.to_csv(R / "s7b_intrinsics_sensitivity.csv", index=False, float_format="%.8g")
print(d.groupby("variant")[["d_rel_heave", "d_rel_pitch"]].agg(lambda x: float(np.max(np.abs(x)))).round(6).to_string())
