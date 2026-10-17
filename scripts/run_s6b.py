import json
import itertools
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from bridgedeck import compare as C, paths
R=paths.REPO/"results"
P=pd.read_csv(R/"s6_matched_pairs.csv"); P=P[(P.arm=="A")&(P.rpm<320)]
fl=json.load(open(R/"s6_floors.json")); camfl=fl["camera_e0"]; lasfl=fl["laser"]
K={"T0":{"y2025":1.0,"y2024":1.0},"T1":{"y2025":26.5/20,"y2024":15/20}}
Dd={"D0":{"y2025":1.0,"y2024":1.0},"D1":{"y2025":13/12,"y2024":10/8}}
Q={"Q1":("cam_mean_P1_y_mm_Afh","las_heave_Afh","mm",True,False,C.FH,"las_bend_dom_hz"),
   "Q2":("cam_mean_P5_roll_rad_Afa","las_pitch_Afa","rad",False,True,C.FA,"las_tors_dom_hz"),
   "Q3":("cam_legacy_bend_Afh","las_bend_Afh","mm",True,False,C.FH,"las_bend_dom_hz"),
   "Q4":("cam_legacy_tors_Afa","las_tors_Afa","mm",True,True,C.FA,"las_tors_dom_hz")}   # (cam col, laser col, unit, camera scales with tag, laser scales with d)
def rule_mask(S,session,q,rule):
    camc,lasc,_,_,_,line,dom=Q[q]
    if rule=="d_all": return pd.Series(True,index=S.index)
    if rule=="a_noise":
        cf=camfl.get(camc); lf=lasfl[session].get(lasc)
        return (S[camc]>=5*cf if cf is not None else True)&(S[lasc]>=5*lf if lf is not None else True)
    if rule=="b_spectrum": return ((S.cam_dom_hz-line).abs()<=0.10)&((S[dom]-line).abs()<=0.10)
rows=[]; closeness=[]; store={}
for tk,dk in itertools.product(K,Dd):
    combo=tk+dk
    for q,(camc,lasc,unit,cam_t,las_d,line,dom) in Q.items():
        for rule in ("d_all","a_noise","b_spectrum"):
            sel={}
            for s in ("y2025","y2024"):
                S=P[P.session==s].set_index("rpm").copy()
                m=rule_mask(S,s,q,rule)&(S[camc]>0)&(S[lasc]>0)
                S=S[m]; c=S[camc]*(K[tk][s] if cam_t else 1.0); l=S[lasc]*(Dd[dk][s] if las_d else 1.0); sel[s]=(c,l)
                if len(S)>=3:
                    mm=C.metrics_boot(c.to_numpy(),l.to_numpy()); mm.update(combo=combo,tag=tk,spacing=dk,session=s,quantity=q,rule=rule); rows.append(mm)
                    store[(combo,q,rule,s)]=(c.index.to_numpy(),c.to_numpy(),l.to_numpy())
            idx=sorted(set(sel["y2025"][0].index)&set(sel["y2024"][0].index))
            if len(idx)>=4:
                c25,l25=sel["y2025"][0].loc[idx].to_numpy(),sel["y2025"][1].loc[idx].to_numpy(); c24,l24=sel["y2024"][0].loc[idx].to_numpy(),sel["y2024"][1].loc[idx].to_numpy()
                rng=np.random.default_rng(11); E=lambda c,l: np.sqrt(np.mean(np.log10(c/l)**2))
                d0=E(c24,l24)-E(c25,l25); ds=[]
                for _ in range(2000):
                    i=rng.integers(0,len(idx),len(idx)); ds.append(E(c24[i],l24[i])-E(c25[i],l25[i]))
                m25,m24=C.metrics_once(c25,l25),C.metrics_once(c24,l24)
                closeness.append(dict(combo=combo,quantity=q,rule=rule,n=len(idx),E_2025=m25["E_log10"],E_2024=m24["E_log10"],dE=d0,dE_lo=np.percentile(ds,2.5),dE_hi=np.percentile(ds,97.5),P_2025_closer=float(np.mean(np.array(ds)>0)),
                    spearman_2025=m25["spearman"],spearman_2024=m24["spearman"],pearson_log_2025=m25["pearson_log"],pearson_log_2024=m24["pearson_log"]))
M=pd.DataFrame(rows); M.to_csv(R/"s6b_variant_metrics.csv",index=False)
Cl=pd.DataFrame(closeness); Cl["closer"]=(Cl.P_2025_closer>=0.95)&(Cl.spearman_2025>=Cl.spearman_2024-0.02)&(Cl.pearson_log_2025>=Cl.pearson_log_2024-0.02); Cl.to_csv(R/"s6b_variant_closeness.csv",index=False)
pd.set_option("display.width",220)
for q in ("Q1","Q2","Q3","Q4"):
    t=M[(M.quantity==q)&(M.rule=="d_all")].pivot(index="combo",columns="session",values=["median_ratio","E_log10"]).round(3)
    print(f"\n== {q} (rule d, 19 conditions): median camera/laser ratio and typical error E, by session"); print(t.to_string())
print("\n== closeness test 2025 vs 2024 by combination (rule d, 19 conditions)")
t=Cl[Cl.rule=="d_all"][["combo","quantity","E_2025","E_2024","dE","dE_lo","dE_hi","P_2025_closer","closer"]].round(3); print(t.to_string(index=False))
print("\n== closeness under rule a (noise) and b (spectrum): P(2025 closer)")
print(Cl[Cl.rule!="d_all"].pivot_table(index=["quantity","rule"],columns="combo",values="P_2025_closer").round(3).to_string())
fig,ax=plt.subplots(1,2,figsize=(11,4))
for a,q,ttl in zip(ax,("Q1","Q2"),("heave @ f_h","pitch @ f_alpha")):
    t=M[(M.quantity==q)&(M.rule=="d_all")].pivot(index="combo",columns="session",values="E_log10").reindex(["T0D0","T1D0","T0D1","T1D1"])
    x=np.arange(len(t)); a.bar(x-0.2,t.y2025,0.4,label="2025 laser"); a.bar(x+0.2,t.y2024,0.4,label="2024 laser"); a.set_xticks(x); a.set_xticklabels(t.index); a.set(ylabel="typical ratio error E (log10)",title=ttl+" (rule d, 19 conditions)"); a.legend(); a.grid(alpha=.3,axis="y")
fig.tight_layout(); fig.savefig(R/"figures"/"s6b_variants_E.png",dpi=130)
