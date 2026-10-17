"""S10 (docs/gates/S10.md): independent session-difference evidence (2a-2d) and onset-aligned comparison (3). Nothing is tuned on the 2025 laser."""
import json
import numpy as np, pandas as pd
from bridgedeck import compare as C, paths
R = paths.REPO / "results"
B = pd.read_csv(R / "s7_budget_by_condition.csv"); P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.rpm < 320)]
pd.set_option("display.width", 220)
ref = pd.DataFrame(json.load(open(R / "reference_frequencies_free_vibration.json")))
print("== 2a free-decay frequencies by session/mode (Hz), fit [lo, hi]"); print(ref.groupby(["session", "mode"]).agg(n=("f_fit_hz", "size"), f=("f_fit_hz", "median"), lo=("f_fit_lo", "min"), hi=("f_fit_hi", "max")).round(4).to_string())
print("\n== 2b within-session window scatter L2 (median over all 19 / rule a)")
print(B.groupby(["quantity", "session"]).L2.median().round(3).to_string())
print("\n== 2c wind speed per RPM, ratio 2025/2024")
w = P.pivot(index="rpm", columns="session", values="wind_ms"); w["ratio"] = w.y2025 / w.y2024; print(w.round(3).T.to_string())
on = {}
print("\n== 2d onset RPM per instrument (heave: max Q1 amplitude in 50-90; torsion: max Q2 amplitude in 70-110)")
for q, lo, hi in (("Q1", 50, 90), ("Q2", 70, 110)):
    for s in ("y2025", "y2024"):
        d = B[(B.quantity == q) & (B.session == s) & B.rpm.between(lo, hi)]
        on[(q, s, "cam")] = int(d.rpm[d.cam_amp.idxmax()]); on[(q, s, "las")] = int(d.rpm[d.las_amp.idxmax()])
        print(q, s, "camera", on[(q, s, "cam")], "laser", on[(q, s, "las")])
print("\n== 3 onset-aligned comparison (offset fixed from 2d; laser curve interpolated in log-amplitude at RPM + offset)")
rows = []
for q in ("Q1", "Q2"):
    for s in ("y2025", "y2024"):
        d = B[(B.quantity == q) & (B.session == s)].sort_values("rpm"); L = P[P.session == s].sort_values("rpm")
        lasfull = d.set_index("rpm").las_amp; off = on[(q, s, "cam")] - on[(q, s, "las")]
        base = C.metrics_once(d.cam_amp.to_numpy(), d.las_amp.to_numpy())["E_log10"]
        x = d.rpm.to_numpy(float); lx = lasfull.index.to_numpy(float); ly = np.log(lasfull.to_numpy())
        for lab, o in (("baseline_offset0", 0), ("aligned", off)):
            sh = x + o; ok = (sh >= lx.min()) & (sh <= lx.max()); li = np.exp(np.interp(sh[ok], lx, ly))
            m = C.metrics_once(d.cam_amp.to_numpy()[ok], li)
            rows.append(dict(quantity=q, session=s, variant=lab, offset_rpm=o, n=int(ok.sum()), dropped=int((~ok).sum()), E=m["E_log10"], median_ratio=m["median_ratio"], pearson_log=m["pearson_log"], spearman=m["spearman"]))
        rows[-2]["E_check_vs_S6"] = base
T = pd.DataFrame(rows); T.to_csv(R / "s10_onset_aligned.csv", index=False, float_format="%.8g"); print(T.round(3).to_string(index=False))
