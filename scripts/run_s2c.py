import json, numpy as np, pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
from bridgedeck import gate_rules as G, paths
O=Path(paths.load()["outputs"]); R=paths.REPO/"results"
dev=pd.read_parquet(O/"s2_detect/wtt_main/detections_ALL21.parquet").reset_index(drop=True)
val=pd.read_parquet(next((O/"s2_detect/wtt_5sec").glob("detections_*.parquet"))).reset_index(drop=True)
dev=G.add_speed(dev).reset_index(drop=True); val=G.add_speed(val).reset_index(drop=True)
sd,sv=G.stream_table(dev),G.stream_table(val); sd["ledger"]=sd.apply(G.ledger_class,axis=1)
print("dev: streams",len(sd),"missed frames",int(sd.miss.sum()),"| 5s: streams",len(sv),"missed frames",int(sv.miss.sum()),"in",sorted(set(sv[sv.miss>0].condition)))
print("largest speed among streams with no miss: dev %.2f, 5s %.2f px/frame"%(sd[sd.miss==0].speed_det_max.max(),sv[sv.miss==0].speed_det_max.max()))
res={}
pred=sd.apply(lambda r:r.max_speed>G.r1_threshold(r.side_px),axis=1); led=sd.ledger!="admissible"
print("R1 (speed > tag side/10 = %.2f px/frame): stream-level vs ledger"%(sd.side_px.median()/10)); print(pd.crosstab(pred.rename("R1_reject"),led.rename("ledger_nonadmissible")).to_string())
pv=sv.apply(lambda r:r.max_speed>G.r1_threshold(r.side_px),axis=1); print("R1 on 5s: rejected streams %d | streams with a miss %d | agreement %d/%d"%(pv.sum(),(sv.miss>0).sum(),((pv)==(sv.miss>0)).sum(),len(sv)))
t=G.r2_threshold(sd); res["R2_all"]=t
loco=[(c,G.r2_threshold(sd[sd.condition!=c])) for c in sd.condition.unique()]
bad=[c for c,tt in loco if ((sd[sd.condition==c].max_speed>tt)!=(sd[sd.condition==c].miss>0)).any()]
print("R2 midpoint %.2f px/frame; leave-one-condition-out range %.2f-%.2f; conditions misclassified when held out: %s"%(t,min(x for _,x in loco),max(x for _,x in loco),bad))
pr=(sv.max_speed>t); print("R2 on 5s: agreement %d/%d (rejected %d, with a miss %d)"%((pr==(sv.miss>0)).sum(),len(sv),pr.sum(),(sv.miss>0).sum()))
for p in (0.05,0.5):
    est,(lo,hi,nb)=G.cluster_boot_logistic(dev,p); res[f"R3_p{p}"]=[est,lo,hi]; print("R3 logistic P(miss)=%.2f: %.2f px/frame, cluster-bootstrap 95%% [%.2f, %.2f] (%d resamples)"%(p,est,lo,hi,nb))
y=(~dev.detected).astype(int); print("frame-level AUC of speed for misses: %.3f"%roc_auc_score(y,dev.speed))
fl=G.hampel_flags(dev); d=dev[dev.detected]
print("R4 Hampel(3 MAD) flags %d of %d detected frames; streams with a flag %d; flags inside e20: %d"%(fl.sum(),len(d),dev[fl].groupby(G.KEYS).ngroups,((dev.condition=="e20_320rpm")&fl).sum()))
rho=spearmanr(d.speed,d.decision_margin); print("Spearman speed vs margin: rho %.3f"%rho.statistic)
x=sd.copy(); m=x.max_speed.median(); x["robust_z"]=(x.max_speed-m)/(1.4826*(x.max_speed-m).abs().median())
print(x.sort_values("robust_z",ascending=False)[["condition","camera","max_speed","miss","robust_z"]].head(5).round(2).to_string(index=False))
sd.to_csv(R/"s2c_stream_table_dev.csv",index=False); sv.to_csv(R/"s2c_stream_table_val_5s.csv",index=False); json.dump(res,open(R/"s2c_summary.json","w"),indent=1,default=str)
