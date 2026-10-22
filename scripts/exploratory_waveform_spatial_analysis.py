#!/usr/bin/env python3
"""Exploratory waveform-shape and apparent spatial-response analysis.

The camera and laser campaigns are not synchronized. Therefore this script
does not compute waveform correlation or phase agreement; it computes only
session-independent spectral-shape and normalized-response diagnostics.
"""
from pathlib import Path
import hashlib, json, platform, subprocess, sys
import numpy as np
import pandas as pd
from scipy import signal

OUT=Path('exploratory_validation'); OUT.mkdir(exist_ok=True)
CAM=Path('/mnt/space/adev/research/phd/phd-research-advisory/03_PACKAGES/chat/CLAUDE_SCIENTIFIC_AUDIT_v3/40_PRIMARY_DERIVED_INPUTS/per_frame_detections.csv')
ZIP=Path('/mnt/phd_data/phd_master/98_legacy_imports/career_legacy_paper2_prework/laser_displacement.zip')

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

df=pd.read_csv(CAM)
df['rpm']=df.condition.str.extract(r'_(\d+)rpm').astype(int)
def detrend_rms(y):
 y=np.asarray(y,float); return float(np.std(signal.detrend(y),ddof=1))
def resample_psd(t,y,fs=60.0):
 t=np.asarray(t,float); y=signal.detrend(np.asarray(y,float));
 grid=np.arange(t[0],t[-1],1/fs)
 z=np.interp(grid,t,y)
 f,p=signal.periodogram(z,fs=fs,window='hann',detrend='constant',scaling='density')
 return f,p
def spectral_shape(f,p):
 m=(f>=0.5)&(f<=10.0); x=np.maximum(p[m],0); x=x/(x.sum() or 1); return f[m],x
def laser(rpm):
 rpms=[20,40,50,60,70,80,90,100,110,120,140,160,180,200,220,240,260,280,300,320]
 dnum=rpms.index(rpm)+1
 path=f'laser_displacement/등류/영角00/D{dnum:02d}'
 # archive uses the Korean directory spelling shown by unzip; discover robustly.
 listing=subprocess.check_output(['unzip','-Z1',str(ZIP)],text=True).splitlines()
 hits=[x for x in listing if x.endswith(f'/D{dnum:02d}') and '/등류/' in x]
 if not hits: raise FileNotFoundError(f'No D file for {rpm}: {path}')
 raw=np.loadtxt(__import__('io').BytesIO(subprocess.check_output(['unzip','-p',str(ZIP),hits[0]])))
 bpath=[x for x in listing if x.endswith('/D00') and '/등류/' in x][0]
 bias=np.loadtxt(__import__('io').BytesIO(subprocess.check_output(['unzip','-p',str(ZIP),bpath])))
 # Locate matching D00 spelling once if needed.
 if bias.ndim==1 or bias.shape[1]!=3:
  bias=np.loadtxt(__import__('io').BytesIO(subprocess.check_output(['unzip','-p',str(ZIP),bpath])))
 d=raw[:,:3]-bias.mean(axis=0); c=d[:,0]*2.7*10; s=d[:,1]*2.7*10
 return (c+s)/2,(s-c)*(20/13),len(d),len(d)/20.0

# Build camera waveform metrics and apparent three-camera response pattern.
cam_rows=[]; shape_rows=[]; grid_common=np.linspace(0.5,10,191)
laser_cache={}
for rpm in sorted(set(df.rpm)&set(range(20,321,10))):
 if rpm not in laser_cache:
  try: laser_cache[rpm]=laser(rpm)
  except Exception as e: continue
 lb,lt,ln,lfs=laser_cache[rpm]
 lf0,lpb0=resample_psd(np.arange(len(lb))/lfs,lb,lfs); lf1,lpt0=resample_psd(np.arange(len(lt))/lfs,lt,lfs)
 lf,lpb=spectral_shape(lf0,lpb0); lf_t,lpt=spectral_shape(lf1,lpt0)
 for cam in ['cam1','cam2','cam3']:
  q=df[(df.rpm==rpm)&(df.camera==cam)&(df.valid_for_gate==True)].sort_values('frame_idx')
  if len(q)<10: continue
  t=q.timestamp_s.to_numpy(float); y=q.centroid_y.to_numpy(float); rms=detrend_rms(y)
  cf,cp=resample_psd(t,y)
  cf,cp=spectral_shape(cf,cp)
  cpi=np.interp(grid_common,cf,cp); cpi/=cpi.sum() or 1
  lpi_b=np.interp(grid_common,lf,lpb); lpi_b/=lpi_b.sum() or 1
  lpi_t=np.interp(grid_common,lf_t,lpt); lpi_t/=lpi_t.sum() or 1
  cam_rows.append(dict(rpm=rpm,camera=cam,n_frames=len(q),camera_centroid_y_rms_px=rms,
                       camera_duration_s=float(t[-1]-t[0]),camera_fs_eff_hz=float(1/np.median(np.diff(t))),
                       camera_peak_hz=float(cf[np.argmax(cp)]),laser_bending_peak_hz=float(lf[np.argmax(lpb)]),laser_torsion_peak_hz=float(lf_t[np.argmax(lpt)]),
                       camera_vs_laser_bending_psd_cosine=float(np.dot(cpi,lpi_b)/(np.linalg.norm(cpi)*np.linalg.norm(lpi_b))),
                       camera_vs_laser_torsion_psd_cosine=float(np.dot(cpi,lpi_t)/(np.linalg.norm(cpi)*np.linalg.norm(lpi_t))),
                       admissibility='diagnostic-only' if rpm==320 and cam=='cam3' else ('rejected' if rpm==320 and cam in ['cam1','cam2'] else 'admissible')))
  shape_rows.append(dict(rpm=rpm,camera=cam,centroid_y_rms_px=rms))
cm=pd.DataFrame(cam_rows); cm.to_csv(OUT/'EXPLORATORY_WAVEFORM_SPECTRAL_SHAPE.csv',index=False)
sh=pd.DataFrame(shape_rows)
wide=sh.pivot(index='rpm',columns='camera',values='centroid_y_rms_px').reset_index()
for c in ['cam1','cam2','cam3']: wide[f'{c}_relative_to_condition_max']=wide[c]/wide[['cam1','cam2','cam3']].max(axis=1)
wide['cam1_cam2_ratio']=wide.cam1/wide.cam2
wide['cam3_to_same_marker_mean_ratio']=wide.cam3/((wide.cam1+wide.cam2)/2)
wide.to_csv(OUT/'EXPLORATORY_APPARENT_SPATIAL_RESPONSE.csv',index=False)
sp=[]
for col in ['cam1_cam2_ratio','cam3_to_same_marker_mean_ratio','cam1_relative_to_condition_max','cam2_relative_to_condition_max','cam3_relative_to_condition_max']:
 for label,m in [('all_20',np.ones(len(wide),bool)),('rpm<320',wide.rpm<320),('rpm<320 excl 60,80',(wide.rpm<320)&~wide.rpm.isin([60,80]))]:
  x=wide.loc[m,col].dropna(); sp.append(dict(metric=col,subset=label,n=len(x),mean=float(x.mean()),median=float(x.median()),rmse_from_one=float(np.sqrt(np.mean((x-1)**2))),p10=float(x.quantile(.1)),p90=float(x.quantile(.9))))
pd.DataFrame(sp).to_csv(OUT/'EXPLORATORY_APPARENT_SPATIAL_RESPONSE_SUMMARY.csv',index=False)

summ=[]
for metric in ['camera_vs_laser_bending_psd_cosine','camera_vs_laser_torsion_psd_cosine']:
 for scope,m in [('all_available',np.ones(len(cm),bool)),('rpm<320',cm.rpm<320),('admitted_only',(cm.rpm<320))]:
  x=cm.loc[m,metric]; summ.append(dict(metric=metric,scope=scope,n=len(x),mean=float(x.mean()),median=float(x.median()),p10=float(x.quantile(.1)),p90=float(x.quantile(.9))))
pd.DataFrame(summ).to_csv(OUT/'EXPLORATORY_WAVEFORM_SPECTRAL_SHAPE_SUMMARY.csv',index=False)
manifest={str(p):sha(p) for p in [CAM,ZIP]}; (OUT/'EXPLORATORY_WAVEFORM_SOURCE_HASHES.json').write_text(json.dumps(manifest,indent=2)+'\n')

report='''# Exploratory Waveform, Spectral-Shape, and Apparent Spatial-Response Study

**STATUS: EXPLORATORY ONLY — NOT WAVEFORM VALIDATION AND NOT MODAL IDENTIFICATION.**

Camera centroid-y traces and laser D-file traces were processed independently. Because the campaigns are not synchronized, no camera–laser Pearson waveform correlation, cross-correlation lag, phase error, coherence, or time-domain RMSE was computed. Such values would be physically uninterpretable across separate acquisitions.

The analysis instead reports:

- camera centroid-y RMS in pixels;
- camera and laser dominant spectral frequencies;
- normalized 0.5–10 Hz spectral-envelope cosine similarity;
- camera cam1/cam2 same-marker response ratios;
- cam3 relative response to the mean of cam1/cam2.

The cam1/cam2/cam3 response table is an **apparent observation-path response pattern**, not a mode shape. Pixel RMS is not a calibrated displacement amplitude, and cam3 differs in marker location, angle, standoff, and optical path.

For genuine waveform-level validation, reacquire the camera and laser signals simultaneously with a common timing signal, use the same physical point and observable, calibrate both in common units, and compare aligned windows with predeclared metrics and uncertainty.
'''
(OUT/'EXPLORATORY_WAVEFORM_SPATIAL_REPORT.md').write_text(report)
(OUT/'EXPLORATORY_WAVEFORM_RUNTIME.txt').write_text(f'python={sys.version}\nplatform={platform.platform()}\nrows={len(cm)}\nlaser_source_zip_sha256={sha(ZIP)}\n')
print(report); print(cm.groupby('camera').size()); print(cm[['camera_vs_laser_bending_psd_cosine','camera_vs_laser_torsion_psd_cosine']].describe())
