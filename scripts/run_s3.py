import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.timeseries import LombScargle
from scipy.stats import binom

from bridgedeck import paths
from bridgedeck import spectral as S

O=Path(paths.load()["outputs"]); R=paths.REPO/"results"
det=pd.read_parquet(O/"s2_detect/wtt_main/detections_ALL21.parquet")
PUB="/mnt/phd_data/phd_master/05_publications/p02_sensors_mdpi_releases/PAPER2_FINAL_AUDIT_2026-10-01/02_SUPPLEMENT/data/S10_ADMITTED_RETAINED_PEAKS_JOINED.csv"
pub={(r["condition"],r["camera"]):float(r["peak_frequency_hz"]) for r in csv.DictReader(open(PUB)) if r["peak_rank"]=="1"}
FH,FA=1.4318,3.0982
rows=[]
streams=[(c,k) for c in sorted(det.condition.unique(),key=lambda s:int(s.split("_")[1].replace("rpm",""))) for k in ("cam1","cam2","cam3") if not (c.startswith("e20") and k!="cam3")]
for cond,cam in streams:
    idx,t,y=S.stream_series(det,cond,cam)
    tt,yy=S.prep(t,y); T=tt[-1]; f,ri=S.grid(T)
    f0,p0=S.peak(tt,yy,f)
    pk=S.top_peaks(f,p0,3)
    # E1 generalised LS (astropy)
    ls=LombScargle(tt,yy,fit_mean=True,center_data=True); p1=ls.power(f,normalization="standard",method="cython"); k1=int(np.argmax(p1)); f1=float(f[k1])
    fap=S.baluev_fap(tt,yy,f,float(p1[k1]))
    # E2 header stamps
    _,th,yh=S.stream_series(det,cond,cam,"stamp_hdr_ns"); tth,yyh=S.prep(th,yh); f2,_=S.peak(tth,yyh,f)
    # E3 interp60, E4 nominal index
    g,yg=S.interp60(t-t[0],y); tg,yg=S.prep(g,yg); f3,_=S.peak(tg,yg,f)
    tn,yn=S.prep(idx/60.0,y); f4,_=S.peak(tn,yn,f)
    fhat=S.fit_sinusoid_freq(tt,yy,f0,ri); lo,hi=S.boot_interval(tt,yy,fhat,ri)
    rows.append(dict(condition=cond,camera=cam,n=len(t),T=T,RI=ri,f_published=pub.get((cond,cam),np.nan),f_E0=f0,f_E1=f1,f_E2_hdr=f2,f_E3_interp60=f3,f_E4_nominal=f4,
        f_refined=fhat,f_lo=lo,f_hi=hi,power_E0=float(p0.max()),fap_baluev=fap,top3=json.dumps([round(a,3) for a,_ in pk]),
        d_pub_RI=abs(f0-pub[(cond,cam)])/ri if (cond,cam) in pub else np.nan,d_E1_RI=abs(f1-f0)/ri,d_hdr_RI=abs(f2-f0)/ri,d_i60_RI=abs(f3-f0)/ri,d_nom_RI=abs(f4-f0)/ri,
        err_fh=min([abs(a-FH)/FH for a,_ in pk if abs(a-FH)<=0.3] or [np.nan]),err_fa=min([abs(a-FA)/FA for a,_ in pk if abs(a-FA)<=0.3] or [np.nan])))
d=pd.DataFrame(rows); d.to_csv(R/"s3_spectra_by_stream.csv",index=False)
a=d[d.f_published.notna()]
print("streams",len(d),"(60 admitted + e20 cam3 diagnostic)")
print("A reproduction: within 0.5 RI of published rank-1: %d / %d ; max %.3f RI ; exact(<1e-6): %d"%((a.d_pub_RI<=0.5).sum(),len(a),a.d_pub_RI.max(),(a.d_pub_RI<1e-6).sum()))
print("B E1 vs E0 within 0.5 RI: %d / %d (%.0f%%); outliers: %s"%((d.d_E1_RI<=0.5).sum(),len(d),100*(d.d_E1_RI<=0.5).mean(),d[d.d_E1_RI>0.5][["condition","camera","f_E0","f_E1","d_E1_RI"]].round(3).values.tolist()))
print("C header-stamp shift: median %.4f RI, max %.3f RI | interp60: median %.4f max %.3f | nominal idx: median %.4f max %.3f (stream %s)"%(d.d_hdr_RI.median(),d.d_hdr_RI.max(),d.d_i60_RI.median(),d.d_i60_RI.max(),d.d_nom_RI.median(),d.d_nom_RI.max(),d.loc[d.d_nom_RI.idxmax(),["condition","camera"]].tolist()))
print("D FAP<0.01 (Baluev): %d / %d ; FAP>=0.01 streams: %s"%((d.fap_baluev<0.01).sum(),len(d),d[d.fap_baluev>=0.01][["condition","camera","fap_baluev"]].round(4).values.tolist()))
# permutation check
rng=np.random.default_rng(3); perm=[]
for cond,cam in (("e0_0rpm","cam1"),("e5_70rpm","cam1"),("e7_90rpm","cam1"),("e7_90rpm","cam3"),("e14_200rpm","cam1"),("e19_300rpm","cam2")):
    idx,t,y=S.stream_series(det,cond,cam); tt,yy=S.prep(t,y); f,ri=S.grid(tt[-1]); pobs=S.peak(tt,yy,f)[1].max()
    mx=np.array([S.ls_scipy(tt,rng.permutation(yy),f).max() for _ in range(1000)]); emp=(1+(mx>=pobs).sum())/1001
    bal=d[(d.condition==cond)&(d.camera==cam)].fap_baluev.iloc[0]; perm.append((cond,cam,bal,emp))
    print("   perm-FAP %s %s: Baluev %.2e, permutation %.2e (floor %.1e)"%(cond,cam,bal,emp,1/1001))
# E chance baseline
adm=d[~((d.condition=="e20_320rpm"))]
near=((adm.f_E0-FH).abs()<=adm.RI)|((adm.f_E0-FA).abs()<=adm.RI); pr=(4*adm.RI/9.5)
exp_=pr.sum(); obs=int(near.sum()); pval=1-binom.cdf(obs-1,len(adm),pr.mean())
print("E stream level: dominant peak within 1 RI of f_h or f_alpha: observed %d / %d, expected by chance %.1f, binomial p %.2g"%(obs,len(adm),exp_,pval))
adm=adm.assign(near=near.values); cc=adm.groupby("condition").near.sum(); k=int((cc>=2).sum()); pc=1-binom.cdf(k-1,len(cc),float(binom.sf(1,3,pr.mean())))
print("  condition level (>=2 of 3 cameras): %d / %d conditions ; chance prob per condition %.3f ; binomial p %.2g"%(k,len(cc),binom.sf(1,3,pr.mean()),pc))
print("F recovery error median: f_h %.2f%% (n=%d), f_alpha %.2f%% (n=%d)"%(100*d.err_fh.median(),d.err_fh.notna().sum(),100*d.err_fa.median(),d.err_fa.notna().sum()))
print("peak CI half-width median %.4f Hz ; max %.4f Hz"%(((d.f_hi-d.f_lo)/2).median(),((d.f_hi-d.f_lo)/2).max()))
json.dump(dict(perm=perm),open(R/"s3_summary.json","w"),indent=1,default=float)
