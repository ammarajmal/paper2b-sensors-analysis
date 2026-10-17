"""S2b analysis (docs/gates/S2b.md): raw (N) vs ECC-compensated (C) vs border-strip placebo (R)."""
import numpy as np, pandas as pd
from pathlib import Path
from bridgedeck import paths, spectral as S, pose
R = paths.REPO / "results"; O = Path(paths.load()["outputs"])
CONDS = ["e0_0rpm", "e7_90rpm", "e14_200rpm"]; CAMS = ["cam1", "cam2", "cam3"]
rows = []
for cond in CONDS:
    for cam in CAMS:
        d = pd.read_parquet(O / f"s2b_{cond}_{cam}.parquet"); dd = d[d.detected & d.cy_C.notna()].copy()
        # use only frames where the N stream passes the S2 admission (margin handled upstream: detected flag only here, as in the gate)
        t = dd.t.to_numpy(); r = dict(condition=cond, camera=cam, n=len(d), n_used=len(dd), nonconv_C=float((~dd.ok_C.astype(bool)).mean()), nonconv_R=float((~dd.ok_R.astype(bool)).mean()))
        def rms(y): y = y - np.median(y); y = y - np.polyval(np.polyfit(t, y, 1), t); return float(np.std(y))
        r.update(rms_N=rms(dd.cy.to_numpy()), rms_C=rms(dd.cy_C.to_numpy()), rms_R=rms(dd.cy_R.to_numpy()))
        tt, yy = S.prep(t, dd.cy.to_numpy()); f, ri = S.grid(tt[-1]); k = int(np.argmax(S.ls_scipy(tt, yy, f))); f0 = float(f[k]); r["f_dom_N"] = f0
        for v, col in (("N", "cy"), ("C", "cy_C"), ("R", "cy_R"), ("warpC", "ty_C"), ("warpR", "ty_R")):
            r[f"A_{v}"] = pose.line_amplitude(t, dd[col].to_numpy(), f0, 0.0)[0] if False else float(np.hypot(*np.linalg.lstsq(np.column_stack([np.cos(2 * np.pi * f0 * t), np.sin(2 * np.pi * f0 * t), np.ones_like(t)]), dd[col].to_numpy(), rcond=None)[0][:2]))
        rows.append(r)
D = pd.DataFrame(rows)
D["dA_C_pct"] = 100 * (D.A_C / D.A_N - 1); D["dA_R_pct"] = 100 * (D.A_R / D.A_N - 1); D["warp_over_tag_C"] = D.A_warpC / D.A_N; D["warp_over_tag_R"] = D.A_warpR / D.A_N
D.to_csv(R / "s2b_compensation.csv", index=False, float_format="%.8g")
pd.set_option("display.width", 220); print(D[["condition", "camera", "n_used", "nonconv_C", "rms_N", "rms_C", "rms_R", "f_dom_N", "A_N", "dA_C_pct", "dA_R_pct", "warp_over_tag_C", "warp_over_tag_R"]].round(4).to_string(index=False))
e0 = D[D.condition == "e0_0rpm"]; dyn = D[D.condition != "e0_0rpm"]
lowers = bool((e0.rms_C < e0.rms_N).all()); within2 = bool((dyn.dA_C_pct.abs() <= 2).all()); moves = bool(((dyn.warp_over_tag_C > 0.5)).any())
print(f"\nDECISION RULE: compensation lowers e0 RMS on all three cameras: {lowers} | e7/e14 amplitude within 2% on all three cameras: {within2} | => compensation kept: {lowers and within2}")
print(f"ADDITIONAL READING RULE: warp carries the tag line (warp/tag > 0.5) in {int((dyn.warp_over_tag_C > 0.5).sum())} of {len(dyn)} dynamic streams (C), {int((dyn.warp_over_tag_R > 0.5).sum())} (R placebo)")
