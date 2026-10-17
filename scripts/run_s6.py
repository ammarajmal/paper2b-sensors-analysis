import json
import itertools
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from bridgedeck import compare as C, paths
O=Path(paths.load()["outputs"]); R=paths.REPO/"results"; (R/"figures").mkdir(exist_ok=True)
frames=pd.read_parquet(O/"s4_pose_channels_by_frame.parquet")
cam=C.camera_table(frames); cam.to_csv(R/"s6_camera_by_condition.csv",index=False)
s3=pd.read_csv(R/"s3_spectra_by_stream.csv"); s3["rpm"]=s3.condition.str.extract(r"_(\d+)rpm").astype(int)
camdom=s3.groupby("rpm").f_refined.median().rename("cam_dom_hz")
cam=cam.merge(camdom,on="rpm",how="left")
e0=cam[cam.rpm==0].iloc[0]
lt={}; lf={}
for s in ("y2025","y2024"): lt[s],lf[s]=C.laser_table(s)
lt["y2025"].to_csv(R/"s6_laser_y2025_lines.csv",index=False); lt["y2024"].to_csv(R/"s6_laser_y2024_lines.csv",index=False)
w25=lt["y2025"].set_index("rpm").wind_ms
cam["wind_assumed_ms"]=cam.rpm.map(w25)
print("zero-wind line floors  camera Q1 (P1 y, mean cams, mm): %.4f | roll (P5 mean, rad): %.5f"%(e0["cam_mean_P1_y_mm_Afh"],e0["cam_mean_P5_roll_rad_Afa"]))
for s in lf: print("  laser floors",s,{k:round(v,5) for k,v in lf[s].items()})
json.dump({"camera_e0":{k:float(v) for k,v in e0.items() if str(k).startswith("cam_") and isinstance(v,(int,float,np.floating))},"laser":lf},open(R/"s6_floors.json","w"),indent=1,default=float)
# variants: (quantity, name, camera col, laser col, camera floor col, laser floor key, line, dom keys)
V=[]
for c in C.CAM_Q1: V.append(("Q1",f"cam_mean_{c}","las_heave_Afh",f"cam_mean_{c}_Afh","las_heave_Afh",C.FH,"las_bend_dom_hz"))
V.append(("Q1","cam3_P1_y_mm","las_heave_Afh","cam_cam3_P1_y_mm_Afh","las_heave_Afh",C.FH,"las_bend_dom_hz"))
for c in C.CAM_Q2: V.append(("Q2",f"cam_mean_{c}","las_pitch_Afa",f"cam_mean_{c}_Afa","las_pitch_Afa",C.FA,"las_tors_dom_hz"))
V.append(("Q2","cam3_P5_roll_rad","las_pitch_Afa","cam_cam3_P5_roll_rad_Afa","las_pitch_Afa",C.FA,"las_tors_dom_hz"))
V+= [("Q3","legacy_bend_line","las_bend_Afh","cam_legacy_bend_Afh","las_bend_Afh",C.FH,"las_bend_dom_hz"),("Q3","legacy_bend_rms","las_bend_rms","cam_legacy_bend_rms",None,C.FH,"las_bend_dom_hz"),
     ("Q4","legacy_tors_line","las_tors_Afa","cam_legacy_tors_Afa","las_tors_Afa",C.FA,"las_tors_dom_hz"),("Q4","legacy_tors_rms","las_tors_rms","cam_legacy_tors_rms",None,C.FA,"las_tors_dom_hz")]
def camcol(name): return name if name.startswith("cam_") and name in cam.columns else None
def pairs(session,arm):
    L=lt[session].copy()
    if arm=="A":
        P=cam[cam.rpm>0].merge(L,on="rpm",how="inner",suffixes=("","_las")); P["las_wind_ms"]=P.wind_ms; return P
    Ls=L.sort_values("wind_ms"); rows=[]
    for _,r in cam[cam.rpm>0].iterrows():
        u=r.wind_assumed_ms
        if not (Ls.wind_ms.min()<=u<=Ls.wind_ms.max()): continue
        d=r.to_dict(); near=Ls.iloc[(Ls.wind_ms-u).abs().argmin()]
        for k in Ls.columns:
            if k.startswith("las_") and not k.endswith("_dom_hz"): d[k]=float(np.interp(u,Ls.wind_ms,Ls[k]))
            elif k.endswith("_dom_hz"): d[k]=float(near[k])
        d["las_wind_ms"]=u; d["rpm_las_nearest"]=float(near.rpm); rows.append(d)
    return pd.DataFrame(rows)
def flags(P,v,session):
    q,name,lascol,camc,lfk,line,domk=v
    f={}
    camfloor=e0[camc] if camc in e0.index else np.nan
    a_c=P[camc]>=5*camfloor if np.isfinite(camfloor) else pd.Series(True,index=P.index)
    a_l=P[lascol]>=5*lf[session][lfk] if lfk else pd.Series(True,index=P.index)
    f["a_noise"]=a_c&a_l
    f["b_spectrum"]=((P.cam_dom_hz-line).abs()<=0.10)&((P[domk]-line).abs()<=0.10)
    # (c) wind band from the 2025 laser alone
    L25=lt["y2025"]; ok25=L25[L25[lascol]>=5*lf["y2025"][lfk]] if lfk else L25
    lo,hi=ok25.wind_ms.min(),ok25.wind_ms.max()
    f["c_windband"]=(P.las_wind_ms>=lo)&(P.las_wind_ms<=hi)
    f["d_all"]=pd.Series(True,index=P.index)
    return f
mrows=[]; pair_store={}
for session,arm in itertools.product(("y2025","y2024"),("A","B")):
    P=pairs(session,arm); pair_store[(session,arm)]=P
    for v in V:
        q,name,lascol,camc=v[0],v[1],v[2],v[3]
        if camc not in P.columns: continue
        F=flags(P,v,session)
        for rule,msk in F.items():
            sel=P[msk&P[camc].notna()&P[lascol].notna()&(P[camc]>0)&(P[lascol]>0)]
            sel_no320=sel[sel.rpm<320]
            for scope,S in (("20-300",sel_no320),("all",sel)):
                if len(S)<3: mrows.append(dict(session=session,arm=arm,quantity=q,variant=name,rule=rule,scope=scope,n=len(S)));continue
                m=C.metrics_boot(S[camc].to_numpy(),S[lascol].to_numpy()); m.update(session=session,arm=arm,quantity=q,variant=name,rule=rule,scope=scope); mrows.append(m)
M=pd.DataFrame(mrows); M.to_csv(R/"s6_metrics.csv",index=False)
allP=[]
for (s,a),P in pair_store.items(): allP.append(P.assign(session=s,arm=a))
pd.concat(allP).to_csv(R/"s6_matched_pairs.csv",index=False)
print("pairs: A 2025 %d (20-300: %d) | A 2024 %d | B 2025 %d | B 2024 %d"%(len(pair_store[("y2025","A")]),(pair_store[("y2025","A")].rpm<320).sum(),len(pair_store[("y2024","A")]),len(pair_store[("y2025","B")]),len(pair_store[("y2024","B")])))
# closeness test
crow=[]
for arm in ("A","B"):
    for v in V:
        q,name,lascol,camc=v[0],v[1],v[2],v[3]
        P5,P4=pair_store[("y2025",arm)],pair_store[("y2024",arm)]
        if camc not in P5.columns: continue
        F5,F4=flags(P5,v,"y2025"),flags(P4,v,"y2024")
        for rule in F5:
            s5=P5[F5[rule]&(P5.rpm<320)&(P5[camc]>0)&(P5[lascol]>0)].set_index("rpm"); s4=P4[F4[rule]&(P4.rpm<320)&(P4[camc]>0)&(P4[lascol]>0)].set_index("rpm")
            idx=sorted(set(s5.index)&set(s4.index))
            if len(idx)<4: continue
            cam_=s5.loc[idx,camc].to_numpy(); l25=s5.loc[idx,lascol].to_numpy(); l24=s4.loc[idx,lascol].to_numpy()
            d=C.paired_dE(cam_,l25,l24); m5=C.metrics_once(cam_,l25); m4=C.metrics_once(cam_,l24)
            d.update(arm=arm,quantity=q,variant=name,rule=rule,E_2025=m5["E_log10"],E_2024=m4["E_log10"],spearman_2025=m5["spearman"],spearman_2024=m4["spearman"],pearson_log_2025=m5["pearson_log"],pearson_log_2024=m4["pearson_log"]); crow.append(d)
Cl=pd.DataFrame(crow); Cl["secondary_ok"]=(Cl.spearman_2025>=Cl.spearman_2024-0.02)&(Cl.pearson_log_2025>=Cl.pearson_log_2024-0.02)
Cl["closer"]=(Cl.P_2025_closer>=0.95)&Cl.secondary_ok; Cl.to_csv(R/"s6_closeness.csv",index=False)
prim=Cl[(Cl.arm=="A")&(Cl.rule=="d_all")&(Cl.variant.isin(["cam_mean_P1_y_mm","cam_mean_P5_roll_rad"]))]
print("\nPRIMARY closeness (arm A, all matched 20-300, mean-of-cameras P1 heave / P5 roll):"); print(prim[["quantity","n","E_2025","E_2024","dE","dE_lo","dE_hi","P_2025_closer","spearman_2025","spearman_2024","pearson_log_2025","pearson_log_2024","closer"]].round(3).to_string(index=False))
print("OVERALL 2025 judged closer (both Q1 and Q2):",bool(prim.closer.all() and len(prim)==2))
print("\nall variants x rules x arms: 2025 closer in %d of %d (%.0f%%)"%(Cl.closer.sum(),len(Cl),100*Cl.closer.mean()))
print(Cl.groupby("quantity").closer.mean().round(2).to_dict(), "| by rule:",Cl.groupby("rule").closer.mean().round(2).to_dict())
# primary table
pm=M[(M.arm=="A")&(M.rule=="d_all")&(M.scope=="20-300")&(M.variant.isin(["cam_mean_P1_y_mm","cam_mean_P5_roll_rad"]))]
print("\nPRIMARY metrics:"); print(pm[["session","quantity","n","median_ratio","median_ratio_lo","median_ratio_hi","E_log10","gsd_ratio","pearson_log","spearman","deming_slope_log"]].round(3).to_string(index=False))
# figures
for q,camc,lascol,lab,unit in (("Q1","cam_mean_P1_y_mm_Afh","las_heave_Afh","heave amplitude at f_h","mm"),("Q2","cam_mean_P5_roll_rad_Afa","las_pitch_Afa","pitch amplitude at f_alpha","rad")):
    fig,ax=plt.subplots(1,3,figsize=(15,4.3))
    for s,col in (("y2025","tab:blue"),("y2024","tab:red")):
        P=pair_store[(s,"A")]; P=P[(P[camc]>0)&(P[lascol]>0)]
        ax[0].loglog(P[lascol],P[camc],"o",color=col,label=s); ax[1].semilogy(P.rpm,P[camc]/P[lascol],"o-",color=col,label=s)
        ax[2].semilogy(P.rpm,P[lascol],"s--",color=col,alpha=.7,label=f"laser {s}")
    ax[2].semilogy(cam[cam.rpm>0].rpm,cam[cam.rpm>0][camc],"k^-",label="camera")
    lim=[min(ax[0].get_xlim()[0],ax[0].get_ylim()[0]),max(ax[0].get_xlim()[1],ax[0].get_ylim()[1])]; ax[0].plot(lim,lim,"k:"); ax[0].set(xlabel=f"laser {lab} ({unit})",ylabel=f"camera ({unit})",title="camera vs laser, 1:1 dotted")
    ax[1].axhline(1,color="k",ls=":"); ax[1].set(xlabel="RPM",ylabel="camera / laser",title="ratio (arm A)"); ax[2].set(xlabel="RPM",ylabel=f"amplitude ({unit})",title=lab)
    for a in ax: a.legend(); a.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(R/"figures"/f"s6_{q}_primary.png",dpi=130); plt.close(fig)
print("figures written")
