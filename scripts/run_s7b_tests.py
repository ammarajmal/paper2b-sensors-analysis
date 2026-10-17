"""S7b Part 2 (docs/gates/S7b.md): consistency tests T1-T7 on the S7 budget. Reads results only."""
import numpy as np, pandas as pd
from scipy.optimize import minimize
from bridgedeck import compare as C, paths

R = paths.REPO / "results"; SEED = 11; NB = 2000
B = pd.read_csv(R / "s7_budget_by_condition.csv")
P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.rpm < 320)]
SETS = {"rule_a": lambda d: d[d.rule_a], "all19": lambda d: d}


def reml(y, u):
    """Random-effects model y_i ~ N(mu, u_i^2 + tau^2) by REML; returns mu, tau."""
    def nll(p):
        mu, lt = p; v = u**2 + np.exp(2 * lt); w = 1 / v
        mu_hat = np.sum(w * y) / np.sum(w)
        return 0.5 * (np.sum(np.log(v)) + np.sum(w * (y - mu_hat) ** 2) + np.log(np.sum(w)))
    best = min((minimize(nll, [np.mean(y), lt0], method="Nelder-Mead") for lt0 in (-4, -2, -1, 0)), key=lambda r: r.fun)
    v = u**2 + np.exp(2 * best.x[1]); w = 1 / v
    return float(np.sum(w * y) / np.sum(w)), float(np.exp(best.x[1]))


def pb_slope(x, y):
    """Passing-Bablok (1983) slope and 95% CI; x, y already on the log scale."""
    n = len(x); s = []
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[j] - x[i], y[j] - y[i]
            if dx == 0 and dy == 0: continue
            sl = np.inf if dx == 0 else dy / dx
            if sl != -1: s.append(sl)
    s = np.sort(np.array(s)); N = len(s); K = int(np.sum(s < -1))
    b = np.median(s[K:]) if (N - K) > 0 else np.nan
    Cg = 1.96 * np.sqrt(n * (n - 1) * (2 * n + 5) / 18); M1 = int(round((N - Cg) / 2)); M2 = N - M1 + 1
    lo, hi = s[min(max(M1 + K - 1, 0), N - 1)], s[min(max(M2 + K - 1, 0), N - 1)]
    return float(b), float(lo), float(hi)


rows_t1, rows_t2, rows_t3, rows_t5, rows_t6, rows_t7 = [], [], [], [], [], []
for q in ("Q1", "Q2"):
    for s in ("y2025", "y2024"):
        for sn, f in SETS.items():
            d = f(B[(B.quantity == q) & (B.session == s)]).sort_values("rpm")
            y, u = d.ln_ratio.to_numpy(), d.u_R.to_numpy(); En = y / (2 * u)
            rows_t1.append(dict(quantity=q, session=s, set=sn, n=len(d), share_abs_En_le_1=float(np.mean(np.abs(En) <= 1)), conditions_En_gt_1=" ".join(str(int(r)) for r in d.rpm[np.abs(En) > 1])))
            birge = float(np.mean((y / u) ** 2)); mu, tau = reml(y, u)
            rng = np.random.default_rng(SEED); bs = []
            for _ in range(NB):
                i = rng.integers(0, len(y), len(y)); bs.append(reml(y[i], u[i]))
            bs = np.array(bs)
            rows_t2.append(dict(quantity=q, session=s, set=sn, n=len(d), birge=birge, mu_ln=mu, mu_lo=np.percentile(bs[:, 0], 2.5), mu_hi=np.percentile(bs[:, 0], 97.5), tau_ln=tau, tau_lo=np.percentile(bs[:, 1], 2.5), tau_hi=np.percentile(bs[:, 1], 97.5), median_u_R=float(np.median(u))))
# T3 laser versus laser
for q in ("Q1", "Q2"):
    for sn in SETS:
        a = B[(B.quantity == q) & (B.session == "y2025")].set_index("rpm"); b = B[(B.quantity == q) & (B.session == "y2024")].set_index("rpm")
        idx = sorted(set(a.index) & set(b.index))
        if sn == "rule_a": idx = [r for r in idx if a.rule_a[r] and b.rule_a[r]]
        y = np.log(a.las_amp[idx].to_numpy() / b.las_amp[idx].to_numpy()); u = np.sqrt(a.u_L[idx].to_numpy() ** 2 + b.u_L[idx].to_numpy() ** 2)
        mu, tau = reml(y, u)
        rows_t3.append(dict(quantity=q, set=sn, n=len(idx), birge=float(np.mean((y / u) ** 2)), mu_ln=mu, tau_ln=tau, sd_ln=float(np.std(y, ddof=1)), median_u=float(np.median(u)), share_abs_En_le_1=float(np.mean(np.abs(y / (2 * u)) <= 1))))
# T4 cam1 versus cam2 (same marker)
rows_t4 = []
fl = pd.read_json(R / "s6_floors.json")["camera_e0"] if False else None
import json; floors = json.load(open(R / "s6_floors.json"))["camera_e0"]
for q, col, suf, lab in (("Q1", "P1_y_mm", "Afh", "heave"), ("Q2", "P5_roll_rad", "Afa", "pitch")):
    a1, a2 = P[f"cam_cam1_{col}_{suf}"].to_numpy(), P[f"cam_cam2_{col}_{suf}"].to_numpy()
    f1, f2 = floors[f"cam_cam1_{col}_{suf}"], floors[f"cam_cam2_{col}_{suf}"]
    ok = (a1 > 5 * f1) & (a2 > 5 * f2); y = np.log(a1 / a2); u = np.sqrt((f1 / a1) ** 2 + (f2 / a2) ** 2)
    for sn, m in (("both_above_5x_floor", ok), ("all19", np.ones(len(y), bool))):
        rows_t4.append(dict(quantity=q, set=sn, n=int(m.sum()), median_ln=float(np.median(y[m])), mad_ln=float(1.4826 * np.median(np.abs(y[m] - np.median(y[m])))), birge_vs_floor_only_budget=float(np.mean((y[m] / u[m]) ** 2)), max_abs_ln=float(np.max(np.abs(y[m])))))
# T5 Passing-Bablok vs Deming (log10 scale), T6 influence, T7 permutation
for q, camcol, lascol in (("Q1", "cam_mean_P1_y_mm_Afh", "las_heave_Afh"), ("Q2", "cam_mean_P5_roll_rad_Afa", "las_pitch_Afa")):
    for s in ("y2025", "y2024"):
        S = P[P.session == s].set_index("rpm")
        d = B[(B.quantity == q) & (B.session == s)].set_index("rpm")
        for sn in SETS:
            idx = [r for r in S.index if (sn == "all19" or d.rule_a.get(r, False)) and S[camcol][r] > 0 and S[lascol][r] > 0]
            x, y = np.log10(S[lascol][idx].to_numpy()), np.log10(S[camcol][idx].to_numpy())
            b, lo, hi = pb_slope(x, y); dm = C.deming_slope(x, y)
            rows_t5.append(dict(quantity=q, session=s, set=sn, n=len(idx), pb_slope=b, pb_lo=lo, pb_hi=hi, deming_slope=dm, rel_diff=(dm - b) / b))
            cam, las = S[camcol][idx].to_numpy(), S[lascol][idx].to_numpy(); full = C.metrics_once(cam, las)
            for k, r in enumerate(idx):
                m = np.ones(len(idx), bool); m[k] = False; mm = C.metrics_once(cam[m], las[m])
                rows_t6.append(dict(quantity=q, session=s, set=sn, rpm_removed=int(r), dE=mm["E_log10"] - full["E_log10"], d_pearson_log=mm["pearson_log"] - full["pearson_log"], d_deming=mm["deming_slope_log"] - full["deming_slope_log"], d_median_ratio=mm["median_ratio"] - full["median_ratio"]))
    for sn in SETS:
        S25, S24 = P[P.session == "y2025"].set_index("rpm"), P[P.session == "y2024"].set_index("rpm")
        d25, d24 = B[(B.quantity == q) & (B.session == "y2025")].set_index("rpm"), B[(B.quantity == q) & (B.session == "y2024")].set_index("rpm")
        idx = [r for r in S25.index if r in S24.index and S25[camcol][r] > 0 and S25[lascol][r] > 0 and S24[lascol][r] > 0 and (sn == "all19" or (d25.rule_a.get(r, False) and d24.rule_a.get(r, False)))]
        e25 = np.log10(S25[camcol][idx].to_numpy() / S25[lascol][idx].to_numpy()) ** 2; e24 = np.log10(S25[camcol][idx].to_numpy() / S24[lascol][idx].to_numpy()) ** 2
        dE = lambda a, b_: np.sqrt(np.mean(b_)) - np.sqrt(np.mean(a))
        obs = dE(e25, e24); rng = np.random.default_rng(SEED); cnt = 0; NP = 10000
        for _ in range(NP):
            sw = rng.random(len(idx)) < 0.5; a = np.where(sw, e24, e25); b_ = np.where(sw, e25, e24)
            cnt += dE(a, b_) >= obs
        rows_t7.append(dict(quantity=q, set=sn, n=len(idx), dE_obs=float(obs), p_one_sided_2025_closer=float((cnt + 1) / (NP + 1))))
out = {"t1_en": rows_t1, "t2_birge_reml": rows_t2, "t3_laser_vs_laser": rows_t3, "t4_cam1_vs_cam2": rows_t4, "t5_passing_bablok": rows_t5, "t6_influence": rows_t6, "t7_permutation": rows_t7}
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
for k, v in out.items():
    df = pd.DataFrame(v); df.to_csv(R / f"s7b_{k}.csv", index=False, float_format="%.10g")
    if k != "t6_influence": print(f"\n== {k}\n" + df.round(3).to_string(index=False))
t6 = pd.DataFrame(out["t6_influence"]); print("\n== t6 largest |dE| per group (top 3 removed conditions)")
for g, d in t6.groupby(["quantity", "session", "set"]): print(g, d.reindex(d.dE.abs().sort_values(ascending=False).index).head(3)[["rpm_removed", "dE", "d_pearson_log", "d_deming"]].round(3).values.tolist())
