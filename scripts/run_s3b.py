"""S3b (docs/gates/S3b.md): timebase shifts on refined (sinusoid-fit) frequencies, in Rayleigh intervals."""
import numpy as np, pandas as pd
from pathlib import Path
from bridgedeck import paths
from bridgedeck import spectral as S

O = Path(paths.load()["outputs"]); R = paths.REPO / "results"
det = pd.read_parquet(O / "s2_detect/wtt_main/detections_ALL21.parquet")
s3 = pd.read_csv(R / "s3_spectra_by_stream.csv")


def refined(t, y, f):
    tt, yy = S.prep(t, y); p = S.ls_scipy(tt, yy, f); f0 = float(f[int(np.argmax(p))])
    return S.fit_sinusoid_freq(tt, yy, f0, S.grid(tt[-1])[1])


rows = []
for _, r in s3.iterrows():
    cond, cam = r.condition, r.camera
    idx, t, y = S.stream_series(det, cond, cam)
    tt, _ = S.prep(t, y); f, ri = S.grid(tt[-1])
    f_rec = refined(t, y, f)
    _, th, yh = S.stream_series(det, cond, cam, "stamp_hdr_ns")
    out = dict(condition=cond, camera=cam, RI=ri, f_rec=f_rec, f_rec_s3=r.f_refined, f_hdr=refined(th, yh, f))
    g, yg = S.interp60(t - t[0], y); out["f_i60"] = refined(g, yg, f)
    g, yg = S.interp60(t - t[0], y, fs=59.94); out["f_i5994"] = refined(g, yg, f)
    out["f_nom"] = refined(idx / 60.0, y, f)
    for k in ("hdr", "i60", "i5994", "nom"):
        out[f"s_{k}_RI"] = abs(out[f"f_{k}"] - f_rec) / ri
    rows.append(out)
d = pd.DataFrame(rows); d.to_csv(R / "s3b_timebase_refined.csv", index=False, float_format="%.12g")
a = d[d.condition != "e20_320rpm"]
print("criterion 1 max |f_rec - S3 f_refined| (Hz):", float(np.max(np.abs(d.f_rec - d.f_rec_s3))))
print("criterion 2 missing values:", int(d[[c for c in d if c.startswith(("f_", "s_"))]].isna().sum().sum()), "streams", len(d))
print("admitted streams", len(a))
for k, lab in (("hdr", "header stamps"), ("i60", "uniform 60 Hz"), ("i5994", "uniform 59.94 Hz"), ("nom", "nominal 60 Hz index")):
    c = a[f"s_{k}_RI"]; print(f"{lab:22s} max {c.max():.3f} median {c.median():.3f} streams>0.1: {(c > 0.1).sum()}")
print("diagnostic e20 cam3:", d[d.condition == "e20_320rpm"][[c for c in d if c.startswith("s_")]].round(3).to_dict("records"))
