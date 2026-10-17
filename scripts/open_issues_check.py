"""Open-issue checks of 2026-10-17: (1) tag size from the ruler in the images, (2) scale sensitivity, (3) laser head spacing implied by the camera angle.
Consistency checks only: nothing here changes any pipeline value."""
import numpy as np, cv2, pandas as pd
from pathlib import Path
from scipy.signal import find_peaks, medfilt
from rosbags.highlevel import AnyReader
from bridgedeck import paths, pose
R = paths.REPO / "results"; (R / "figures").mkdir(exist_ok=True)
print("== 1. tag size from the ruler graduations (e0_0rpm frame 0; ruler ticks assumed 5 mm: printed numbers 10 and 5 are 10 ticks apart, read as cm)")
bag = next(Path(paths.load()["bags"]["wtt_main"]).rglob("e0_0rpm*.bag")); imgs = {}
with AnyReader([bag]) as r:
    for cam in ("cam1", "cam3"):
        c = [c for c in r.connections if c.topic == f"/sony_{cam}/image_raw/compressed"]
        _, t, raw = next(r.messages(connections=c)); m = r.deserialize(raw, c[0].msgtype)
        imgs[cam] = cv2.cvtColor(cv2.imdecode(np.frombuffer(bytes(m.data), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY).astype(float)
det = pd.read_parquet(Path(paths.load()["outputs"]) / "s2_detect/wtt_main/detections_ALL21.parquet")
cfg = {"cam1": dict(rows=(250, 345), xs=[(20, 830), (1380, 1900)]), "cam3": dict(rows=(895, 960), xs=[(20, 420), (1000, 1260), (1540, 1900)])}
for cam, cf in cfg.items():
    g = det[(det.condition == "e0_0rpm") & (det.camera == cam) & det.detected]
    K, D = pose.intrinsics(cam); side = float(np.median(pose.side_len(pose.undistort(pose.corners_of(g), K, D))))
    im = imgs[cam]; y0, y1 = cf["rows"]; prof = im[y0:y1].mean(axis=0); hp = -(prof - medfilt(prof, 31)); pk_all = []
    for x0, x1 in cf["xs"]:
        pk, _ = find_peaks(hp[x0:x1], prominence=np.std(hp[x0:x1]) * 1.2, distance=40); pk_all += list(pk + x0)
    pk_all = np.array(sorted(pk_all)); d = np.diff(pk_all); ok = d[(d > 40) & (d < 150)]
    mod = np.median(ok); k = np.round((pk_all - pk_all[0]) / mod); A = np.vstack([k, np.ones_like(k)]).T; coef, *_ = np.linalg.lstsq(A, pk_all, rcond=None)
    clean = ok[(ok > 70) & (ok < 75)]
    print(f"{cam}: tag side {side:.2f} px; tick period {coef[0]:.2f} px (comb fit, {int(k.max())} intervals) / {clean.mean():.2f} px (mean of {len(clean)} clean spacings) -> tag = {5*side/coef[0]:.2f} mm / {5*side/clean.mean():.2f} mm")
    if cam == "cam1":
        vis = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        for x in pk_all: cv2.line(vis, (int(x), y0 - 30), (int(x), y1 + 30), (0, 255, 0), 2)
        cv2.imwrite(str(R / "figures/ruler_ticks_cam1.png"), cv2.resize(vis, (1280, 720)))
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.rpm < 320)]; rng = np.random.default_rng(11)
E = lambda c, l: np.sqrt(np.mean(np.log10(c / l) ** 2))
print("\n== 2. camera scale sensitivity on the primary heave error E (arm A, 19 conditions)")
for s in ("y2025", "y2024"):
    d = P[(P.session == s) & (P.cam_mean_P1_y_mm_Afh > 0) & (P.las_heave_Afh > 0)]; c = d.cam_mean_P1_y_mm_Afh.to_numpy(); l = d.las_heave_Afh.to_numpy()
    ks = np.linspace(0.5, 2.0, 301); Ek = [E(c * k, l) for k in ks]; kopt = ks[int(np.argmin(Ek))]
    bs = [ks[int(np.argmin([E(c[i] * k, l[i]) for k in ks]))] for i in (rng.integers(0, len(c), len(c)) for _ in range(500))]
    print(f"{s}: E at -2.5%/0/+2.5% = {E(c*.975,l):.3f}/{E(c,l):.3f}/{E(c*1.025,l):.3f}; E-minimising scale x{kopt:.2f} (tag {20*kopt:.1f} mm), bootstrap 95% [{np.percentile(bs,2.5):.2f}, {np.percentile(bs,97.5):.2f}]")
print("\n== 3. head spacing d implied by the camera's pitch angle (consistency check, not a calibration)")
dass = {"y2025": 13.0, "y2024": 10.0}
for s in ("y2025", "y2024"):
    d = P[(P.session == s) & ((P.cam_dom_hz - 3.0982).abs() <= 0.10) & ((P.las_tors_dom_hz - 3.0982).abs() <= 0.10) & (P.cam_mean_P5_roll_rad_Afa > 0.004) & (P.las_pitch_Afa > 0.004)]
    r = (d.cam_mean_P5_roll_rad_Afa / d.las_pitch_Afa).to_numpy(); bs = [np.median(dass[s] / r[rng.integers(0, len(r), len(r))]) for _ in range(2000)]
    print(f"{s}: conditions {d.rpm.astype(int).tolist()}; camera/laser pitch ratio median {np.median(r):.3f}; implied d {np.median(dass[s]/r):.1f} cm [{np.percentile(bs,2.5):.1f}, {np.percentile(bs,97.5):.1f}] vs vendor {dass[s]:.0f} cm; ratio if the vendor halving were right: {np.median(r)/2:.2f}")
