"""S8a (docs/gates/S8.md addendum): rebuilt-pipeline correlations on the manuscripts' own 16-condition set (19 matched RPM minus 60, 80, 300). EXPLORATORY."""
import numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr
from bridgedeck import paths
R = paths.REPO / "results"
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.session == "y2024") & (P.rpm < 320)]
assert len(P) == 19
rows = []
for scope, d in (("all19", P), ("paperset16", P[~P.rpm.isin([60, 80, 300])])):
    assert len(d) == (19 if scope == "all19" else 16)
    for q, c, l in (("bending", "cam_legacy_bend_rms", "las_bend_rms"), ("torsion", "cam_legacy_tors_rms", "las_tors_rms")):
        x, y = d[c].to_numpy(), d[l].to_numpy()
        rows.append(dict(scope=scope, quantity=q, n=len(d), pearson_lin=pearsonr(x, y)[0], spearman=spearmanr(x, y)[0], mean_ratio=float(np.mean(x / y)),
                         rmse_mm=float(np.sqrt(np.mean((x - y) ** 2))), mae_mm=float(np.mean(np.abs(x - y))), slope_through_origin=float((x @ y) / (y @ y)), slope_ols=float(np.polyfit(y, x, 1)[0])))
out = pd.DataFrame(rows); out.to_csv(R / "paperset_check.csv", index=False, float_format="%.12g"); print(out.round(4).to_string(index=False))
