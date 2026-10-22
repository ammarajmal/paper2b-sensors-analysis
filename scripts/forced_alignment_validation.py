#!/usr/bin/env python3
"""Forced camera/laser alignment experiment.

This estimates a lag on one part of cross-session data and evaluates it on
held-out data. It is not physical synchronization or validation.
"""
from pathlib import Path
import io, subprocess, sys, platform, hashlib, json
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt

OUT=Path('exploratory_validation/forced_alignment'); OUT.mkdir(parents=True,exist_ok=True)
PLOTS=OUT/'plots'; PLOTS.mkdir(exist_ok=True)
CAM=Path('/mnt/space/adev/research/phd/phd-research-advisory/03_PACKAGES/chat/CLAUDE_SCIENTIFIC_AUDIT_v3/40_PRIMARY_DERIVED_INPUTS/per_frame_detections.csv')
ZIP=Path('/mnt/phd_data/phd_master/98_legacy_imports/career_legacy_paper2_prework/laser_displacement.zip')
DOM=Path('/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/analysis_2026-10-15/laser2025_vs_camera_dominant.csv')
RPM_LIST=[20,40,50,60,70,80,90,100,110,120,140,160,180,200,220,240,260,280,300,320]
FS=60.0

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def zscore(x):
 x=signal.detrend(np.asarray(x,float)); return (x-x.mean())/(x.std(ddof=1) or 1)
def archive_file(name):
 listing=subprocess.check_output(['unzip','-Z1',str(ZIP)],text=True).splitlines()
 hit=[x for x in listing if x.endswith('/'+name) and '/등류/' in x][0]
 return np.loadtxt(io.BytesIO(subprocess.check_output(['unzip','-p',str(ZIP),hit])))
def laser_wave(rpm):
 d=archive_file(f'D{RPM_LIST.index(rpm)+1:02d}'); bias=archive_file('D00').mean(axis=0); d=d[:,:3]-bias
 c=d[:,0]*2.7*10; s=d[:,1]*2.7*10
 return (c+s)/2,(s-c)*(20/13),len(d)/20
def uniform(t,y,fs=FS):
 t=np.asarray(t,float); grid=np.arange(t[0],min(t[-1],20.0),1/fs)
 return grid,zscore(np.interp(grid,t,np.asarray(y,float)))
def best_lag(a,b,maxlag=10.0):
 c=signal.correlate(a,b,mode='full',method='fft'); l=signal.correlation_lags(len(a),len(b),mode='full')/FS
 m=np.abs(l)<=maxlag; i=np.argmax(c[m]); return float(l[m][i]),float(c[m][i]/(len(a)-1))
def shift_for_lag(x,lag):
 n=int(round(lag*FS)); return x[n:] if n>=0 else x[:n]
def fit_phase(t,y,f):
 X=np.column_stack([np.cos(2*np.pi*f*t),np.sin(2*np.pi*f*t)])
 ab=np.linalg.lstsq(X,signal.detrend(y),rcond=None)[0]; return float(np.hypot(ab[0],ab[1])),float(np.arctan2(-ab[1],ab[0]))

df=pd.read_csv(CAM); df['rpm']=df.condition.str.extract(r'_(\d+)rpm').astype(int)
dom=pd.read_csv(DOM)
wave=[]; phase_rows=[]; plot_rpms=[20,70,80,140,200,300,320]
for rpm in RPM_LIST:
 lb,lt,lfs=laser_wave(rpm); lt0=np.arange(len(lb))/lfs; lgrid,lbz=uniform(lt0,lb); _,ltz=uniform(lt0,lt)
 lf,lp=signal.periodogram(signal.detrend(lb),fs=lfs); m=(lf>=.5)&(lf<=10); bend_f=float(lf[m][np.argmax(lp[m])])
 lf2,lp2=signal.periodogram(signal.detrend(lt),fs=lfs); m2=(lf2>=.5)&(lf2<=10); tors_f=float(lf2[m2][np.argmax(lp2[m2])])
 for cam in ['cam1','cam2','cam3']:
  q=df[(df.rpm==rpm)&(df.camera==cam)&(df.valid_for_gate==True)].sort_values('frame_idx')
  if len(q)<100: continue
  cg,cz=uniform(q.timestamp_s.to_numpy(),q.centroid_y.to_numpy()); n=min(len(cz),len(lbz)); cz=cz[:n]; bz=lbz[:n]; tz=ltz[:n]; cg=cg[:n]
  split=int(.6*n); train=slice(0,split); test=slice(split,None)
  for target,ref,f0 in [('bending',bz,bend_f),('torsion',tz,tors_f)]:
   lag,train_corr=best_lag(cz[train],ref[train])
   # Apply the fixed lag in time coordinates, then interpolate both signals
   # onto the same corrected elapsed-time grid. This avoids ambiguous array
   # slicing when the lag is negative.
   ref_time=lgrid[:len(ref)]+lag; lo=max(cg[0],ref_time[0]); hi=min(cg[-1],ref_time[-1]); aligned_t=np.arange(lo,hi,1/FS)
   aligned_cam=np.interp(aligned_t,cg,cz); aligned_ref=np.interp(aligned_t,ref_time,ref)
   aligned_split=lo+0.6*(hi-lo); train_m=aligned_t<aligned_split; test_m=~train_m
   obs=aligned_cam[test_m]; pred=aligned_ref[test_m]; ntest=min(len(pred),len(obs)); pred=pred[:ntest]; obs=obs[:ntest]
   test_corr=float(np.corrcoef(obs,pred)[0,1]) if ntest>2 else np.nan; rmse=float(np.sqrt(np.mean((obs-pred)**2))) if ntest else np.nan
   if ntest>64:
    fcoh,coh=signal.coherence(obs,pred,fs=FS,nperseg=min(512,max(64,ntest//3))); band=(fcoh>=max(.5,f0-.1))&(fcoh<=f0+.1); coh_at=float(np.max(coh[band])) if band.any() else np.nan
    fcs,cs=signal.csd(obs,pred,fs=FS,nperseg=min(512,max(64,ntest//3))); band=(fcs>=max(.5,f0-.1))&(fcs<=f0+.1); phase=float(np.angle(cs[band][np.argmax(np.abs(cs[band]))])) if band.any() else np.nan
   else: coh_at=np.nan; phase=np.nan
   wave.append(dict(rpm=rpm,camera=cam,target=target,n_total=n,lag_s=lag,train_corr=train_corr,test_corr=test_corr,test_zscore_rmse=rmse,coherence_near_target=coh_at,phase_error_rad=phase,laser_target_frequency_hz=f0,admissibility='diagnostic-only' if rpm==320 and cam=='cam3' else ('rejected' if rpm==320 and cam in ['cam1','cam2'] else 'admissible')))
   if rpm in plot_rpms and cam=='cam1' and target=='bending':
    k=min(len(cg),len(lgrid)); tt=np.arange(k)/FS; fig,ax=plt.subplots(3,1,figsize=(10,8))
    ax[0].plot(cg[:k],cz[:k],label='camera centroid-y'); ax[0].plot(lgrid[:k],bz[:k],label='laser bending'); ax[0].axvline(cg[0]+split/FS,color='k',ls='--'); ax[0].legend(); ax[0].set_ylabel('z-score')
    ax[1].plot(aligned_t[train_m],aligned_cam[train_m],label='camera aligned train'); ax[1].plot(aligned_t[train_m],aligned_ref[train_m],label='laser aligned train'); ax[1].set_title(f'RPM {rpm}: fixed lag={lag:.3f} s, train corr={train_corr:.3f}'); ax[1].legend(); ax[1].set_ylabel('z-score')
    ax[2].plot(aligned_t[test_m],aligned_cam[test_m],label='camera aligned held-out'); ax[2].plot(aligned_t[test_m],aligned_ref[test_m],label='laser aligned held-out'); ax[2].set_title(f'held-out corr={test_corr:.3f}, RMSE={rmse:.3f}, coherence={coh_at:.3f}'); ax[2].legend(); ax[2].set_xlabel('Corrected elapsed time (s)'); ax[2].set_ylabel('z-score'); fig.tight_layout(); fig.savefig(PLOTS/f'forced_alignment_rpm{rpm:03d}_cam1_bending.png',dpi=160); plt.close(fig)
  amp,ph=fit_phase(cg,cz,bend_f); phase_rows.append(dict(rpm=rpm,camera=cam,target='bending',frequency_hz=bend_f,amplitude_z=amp,phase_rad=ph))
  amp,ph=fit_phase(cg,cz,tors_f); phase_rows.append(dict(rpm=rpm,camera=cam,target='torsion',frequency_hz=tors_f,amplitude_z=amp,phase_rad=ph))

w=pd.DataFrame(wave); w.to_csv(OUT/'FORCED_ALIGNMENT_WAVEFORM_RESULTS.csv',index=False)
ph=pd.DataFrame(phase_rows); ph['relative_phase_to_cam1_rad']=ph['phase_rad']-ph.groupby(['rpm','target']).phase_rad.transform('first'); ph['relative_phase_to_cam1_deg']=np.rad2deg(np.angle(np.exp(1j*ph.relative_phase_to_cam1_rad))); ph.to_csv(OUT/'APPARENT_CAMERA_PHASE_MODE_SHAPE.csv',index=False)
summ=[]
for target in ['bending','torsion']:
 for subset,m in [('all_admissible',(w.target==target)&(w.admissibility=='admissible')),('rpm<320_admissible',(w.target==target)&(w.admissibility=='admissible')&(w.rpm<320))]:
  g=w[m]
  for col in ['train_corr','test_corr','test_zscore_rmse','coherence_near_target','phase_error_rad']:
   x=g[col].dropna(); summ.append(dict(target=target,subset=subset,metric=col,n=len(x),mean=float(x.mean()),median=float(x.median()),p10=float(x.quantile(.1)),p90=float(x.quantile(.9))))
pd.DataFrame(summ).to_csv(OUT/'FORCED_ALIGNMENT_SUMMARY.csv',index=False)
manifest={str(p):sha(p) for p in [CAM,ZIP,DOM]}; (OUT/'FORCED_ALIGNMENT_SOURCE_HASHES.json').write_text(json.dumps(manifest,indent=2)+'\n')
report='''# Forced Camera–Laser Alignment Experiment

**STATUS: EXPLORATORY ONLY — NOT TRUE SYNCHRONIZATION, VALIDATION, OR MODAL IDENTIFICATION.**

The lag was estimated by maximizing correlation on the first 60% of each condition and then applied unchanged to the remaining 40%. This tests whether apparent agreement transfers to held-out samples; it does not recover a physical historical start time.

`FORCED_ALIGNMENT_WAVEFORM_RESULTS.csv` contains lag, training correlation, held-out correlation, standardized waveform RMSE, conditional coherence, and conditional phase. `APPARENT_CAMERA_PHASE_MODE_SHAPE.csv` contains fitted camera phase/amplitude at laser target frequencies relative to cam1. `plots/` contains clean selected-condition plots.

High training correlation is expected to be partly manufactured by lag optimization. Held-out correlation, coherence, and phase remain conditional diagnostics because the acquisitions were separate. The phase table is an apparent camera phase pattern, not a structural mode shape: cam1/cam2 view the same marker, cam3 views a different marker, and the signals are not spatially calibrated into common physical degrees of freedom.

True waveform accuracy requires simultaneous acquisition, a common hardware clock or pulse, the same physical observable, calibrated common units, known spatial registration, and predeclared alignment and acceptance rules. Modal identification additionally requires multiple spatial points, reliable phase relationships, mode-shape completeness, and a structural reference or model.
'''
(OUT/'FORCED_ALIGNMENT_REPORT.md').write_text(report); (OUT/'FORCED_ALIGNMENT_RUNTIME.txt').write_text(f'python={sys.version}\nplatform={platform.platform()}\nwaveform_rows={len(w)}\nphase_rows={len(ph)}\nlag_training_fraction=0.60\nheldout_fraction=0.40\n')
print(report); print(w.groupby('target')[['train_corr','test_corr','test_zscore_rmse','coherence_near_target']].median())
