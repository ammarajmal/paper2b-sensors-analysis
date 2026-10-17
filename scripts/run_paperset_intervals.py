"""S8b (docs/gates/S8.md addendum): bootstrap intervals, leave-one-out range and log-scale r on the manuscripts' 16-condition set. EXPLORATORY.
Method: percentile bootstrap over conditions (2,000 resamples, seed 11, resampling pairs); OLS fit cam = slope x LDS + intercept."""
import numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr
from bridgedeck import paths
R = paths.REPO / "results"; NB = 2000
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.session == "y2024") & (P.rpm < 320)]
P = P[~P.rpm.isin([60, 80, 300])]; assert len(P) == 16


def stats(x, y):
    sl, ic = np.polyfit(y, x, 1)
    return dict(pearson_lin=pearsonr(x, y)[0], spearman=spearmanr(x, y)[0], mean_ratio=np.mean(x / y), ratio_sd=np.std(x / y, ddof=1), mae_mm=np.mean(np.abs(x - y)),
                rmse_mm=np.sqrt(np.mean((x - y) ** 2)), slope_ols=sl, intercept_ols=ic, pearson_log=pearsonr(np.log(x), np.log(y))[0])


rows = []
for q, c, l in (("bending", "cam_legacy_bend_rms", "las_bend_rms"), ("torsion", "cam_legacy_tors_rms", "las_tors_rms")):
    x, y = P[c].to_numpy(), P[l].to_numpy(); est = stats(x, y); rng = np.random.default_rng(11); bs = []
    while len(bs) < NB:
        i = rng.integers(0, len(x), len(x))
        if np.ptp(y[i]) > 0 and np.ptp(x[i]) > 0: bs.append(stats(x[i], y[i]))
    bs = pd.DataFrame(bs)
    for k, v in est.items():
        rows.append(dict(scope="paperset16", quantity=q, stat=k, estimate=v, ci_lo=np.percentile(bs[k], 2.5), ci_hi=np.percentile(bs[k], 97.5)))
    loo = [pearsonr(np.delete(x, i), np.delete(y, i))[0] for i in range(len(x))]
    rows.append(dict(scope="paperset16", quantity=q, stat="loo_r", estimate=np.nan, ci_lo=min(loo), ci_hi=max(loo)))
out = pd.DataFrame(rows); out.to_csv(R / "paperset_intervals.csv", index=False, float_format="%.12g"); print(out.round(4).to_string(index=False))
