"""S9 Step 2 (docs/gates/S9.md): classify each condition's camera-versus-laser disagreement (laser used here, AFTER the camera-only flags were committed)."""
import numpy as np, pandas as pd
from bridgedeck import paths
R = paths.REPO / "results"
F = pd.read_csv(R / "s9_condition_flags.csv"); S = pd.read_csv(R / "s9_stream_flags.csv")
B = pd.read_csv(R / "s7_budget_by_condition.csv"); P = pd.read_csv(R / "s6_matched_pairs.csv"); P = P[(P.arm == "A") & (P.rpm < 320)]
rows = []
for q, domcol in (("Q1", "las_bend_dom_hz"), ("Q2", "las_tors_dom_hz")):
    for s in ("y2025", "y2024"):
        for _, f in F.iterrows():
            b = B[(B.session == s) & (B.quantity == q) & (B.condition == f.condition)].iloc[0]; p = P[(P.session == s) & (P.condition == f.condition)].iloc[0]
            flags = [k for k, v in (("F1", f.F1), ("F3", f[f"{q}_F3"]), ("F4", f[f"{q}_F4"]), ("F5", f[f"{q}_F5"]), ("F6", f.F6)) if v]   # F2 has no within-camera flag
            diag = [k for k in flags if k != "F5"]
            las_floor_hit = bool(b.las_amp < 5 * b.las_floor); cam_floor_hit = bool(f[f"{q}_F7"]); df_hz = abs(p.cam_dom_hz - p[domcol])
            def rest():
                if cam_floor_hit or las_floor_hit: return "c_noise_floor"
                return "b_regime_mismatch" if df_hz > 0.10 else "d_unexplained"
            v0 = "a_camera_defect" if flags else rest()                              # literal gate order, F5 included
            v1 = "a_camera_defect" if diag else rest()                               # F5 excluded (declared non-diagnostic at Step 1)
            v2 = "c_noise_floor" if cam_floor_hit else ("a_camera_defect" if diag else rest())   # floor first: below the floor the F-tests are void
            typ = v1
            rows.append(dict(quantity=q, session=s, condition=f.condition, rpm=int(f.rpm), type=v1, type_literal=v0, type_floor_first=v2, flags=" ".join(flags), cam_floor=cam_floor_hit, las_floor=bool(las_floor_hit), dom_diff_hz=float(df_hz), ln_ratio=float(b.ln_ratio), abs_ln=abs(float(b.ln_ratio)), u_R=float(b.u_R)))
D = pd.DataFrame(rows)
# V3 (added after seeing V0-V2, labelled as such): onset jump = the amplitude step between neighbouring RPM differs between camera and laser by more than a factor of 5 (gate clause 'amplitude ratio between neighbouring RPM changes in one session only')
D["jump"] = False
for (q, s_), g in B.groupby(["quantity", "session"]):
    g = g.sort_values("rpm").reset_index(drop=True); step = np.log(g.cam_amp / g.cam_amp.shift(1)) - np.log(g.las_amp / g.las_amp.shift(1))
    for i in range(1, len(g)):
        if abs(step[i]) > np.log(5): D.loc[(D.quantity == q) & (D.session == s_) & (D.rpm == g.rpm[i]), "jump"] = True
D["type_onset_jump"] = np.where(D.type_floor_first.eq("d_unexplained") & D.jump, "b_regime_mismatch", D.type_floor_first)
D.to_csv(R / "s9_classification.csv", index=False, float_format="%.8g")
pd.set_option("display.width", 220)
print("== primary (gate + Step 1 declaration: F5 excluded)"); print(D.groupby(["quantity", "session", "type"]).agg(n=("rpm", "count"), median_abs_ln=("abs_ln", "median"), max_abs_ln=("abs_ln", "max")).round(3).to_string())
print()
for (q, s), g in D.groupby(["quantity", "session"]):
    print(q, s, {t: sorted(x.rpm.tolist()) for t, x in g.groupby("type")})
for col, lab in (("type_literal", "literal gate order"), ("type_floor_first", "floor-first"), ("type_onset_jump", "floor-first + onset-jump (V3, added after V0-V2)")):
    print("==", lab); print(D.groupby(["quantity", "session", col]).agg(n=("rpm", "count"), median_abs_ln=("abs_ln", "median")).round(3).to_string())
D["sq"] = D.ln_ratio ** 2
for col in ("type", "type_floor_first", "type_onset_jump"):
    print("== share of the total squared ln-ratio by class:", col); print((D.groupby(["quantity", "session", col]).sq.sum() / D.groupby(["quantity", "session"]).sq.sum()).round(3).unstack().fillna(0).to_string())
print("onset-jump conditions:", {(q, s_): sorted(g.rpm[g.jump].tolist()) for (q, s_), g in D.groupby(["quantity", "session"])})
print("each condition classified exactly once per quantity/session:", bool((D.groupby(["quantity", "session", "condition"]).size() == 1).all()), "| rows", len(D))
