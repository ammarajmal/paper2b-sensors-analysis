#!/usr/bin/env python3
"""Exploratory camera/laser comparison; never edits canonical project files."""
from pathlib import Path
import hashlib, json, platform, sys
import numpy as np
import pandas as pd

OUT = Path("exploratory_validation")
OUT.mkdir(exist_ok=True)
CAM_PEAKS = Path("/mnt/space/adev/research/phd/phd-research-advisory/03_PACKAGES/chat/CLAUDE_SCIENTIFIC_AUDIT_v3/30_RESULTS/25A_REFERENCE_BLIND_PEAKS_FROZEN.csv")
LASER = Path("/mnt/phd_data/phd_master/05_publications/p02_sensors_windtunnel/scripts/table_2025_ldv_primary.csv")
CAM_LASER = Path("/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/analysis_2026-10-15/laser2025_vs_camera_dominant.csv")
RAW_LASER = Path("/mnt/phd_data/phd_master/04_code_software/bridgedeck-vision-pipeline/working_tree/results/laser_y2025_by_condition.csv")

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

peaks=pd.read_csv(CAM_PEAKS); laser=pd.read_csv(LASER); dom=pd.read_csv(CAM_LASER); raw=pd.read_csv(RAW_LASER)
for d in [peaks,laser,dom,raw]: d['rpm']=d['rpm'].astype(int)
rows=[]
for rpm in sorted(set(laser.rpm)&set(peaks.rpm)&set(dom.rpm)):
    bend=float(dom.loc[dom.rpm==rpm,'laser_bend_dom_hz'].iloc[0]); tors=float(dom.loc[dom.rpm==rpm,'laser_tors_dom_hz'].iloc[0])
    for cam in ['cam1','cam2','cam3']:
        p=peaks[(peaks.rpm==rpm)&(peaks.camera==cam)].sort_values('peak_rank')
        for target_name,target in [('bend',bend),('torsion',tors)]:
            q=p.assign(abs_error_hz=(p.peak_frequency_hz-target).abs())
            best=q.sort_values(['abs_error_hz','peak_rank']).iloc[0]; ray=float(best.rayleigh_resolution_hz)
            rows.append(dict(rpm=rpm,camera=cam,laser_target=target_name,laser_frequency_hz=target,
                             camera_best_peak_rank=int(best.peak_rank),camera_best_frequency_hz=float(best.peak_frequency_hz),
                             absolute_error_hz=float(best.abs_error_hz),signed_error_hz=float(best.peak_frequency_hz-target),
                             error_rayleigh=float(best.abs_error_hz/ray),within_one_rayleigh=bool(best.abs_error_hz<=ray),
                             admissibility='diagnostic-only' if (rpm==320 and cam=='cam3') else ('rejected' if rpm==320 and cam in ['cam1','cam2'] else 'admissible')))
match=pd.DataFrame(rows); match.to_csv(OUT/'EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv',index=False)

def stats(g):
    x=g.absolute_error_hz.to_numpy(float)
    return pd.Series(dict(n=len(g),mean_abs_error_hz=x.mean(),median_abs_error_hz=np.median(x),rmse_hz=np.sqrt(np.mean(x*x)),
                          p90_abs_error_hz=np.percentile(x,90),mean_signed_error_hz=g.signed_error_hz.mean(),within_one_rayleigh_fraction=g.within_one_rayleigh.mean()))
summ=[]
for target in ['bend','torsion']:
    for cams in [['cam1','cam2'],['cam3'],['cam1','cam2','cam3']]:
        for subset,label in [(match.rpm<320,'rpm<320'),((match.rpm<320)&(match.rpm!=60)&(match.rpm!=80),'rpm<320 excl 60,80')]:
            g=match[(match.laser_target==target)&match.camera.isin(cams)&subset]
            s=stats(g); s['laser_target']=target; s['camera_scope']='+'.join(cams); s['subset']=label; summ.append(s)
pd.DataFrame(summ).to_csv(OUT/'EXPLORATORY_CAMERA_LASER_FREQUENCY_SUMMARY.csv',index=False)

# Dominant-peak comparison is kept separate from nearest-of-five matching because
# selecting the nearest retained peak can be optimistic for a correspondence test.
dom_rows=[]
for target_col,target_name in [('laser_bend_dom_hz','bend'),('laser_tors_dom_hz','torsion')]:
    for cam in ['cam1','cam2','cam3']:
        g=dom[dom.rpm<320].copy(); err=g[cam]-g[target_col]
        dom_rows.append(dict(laser_target=target_name,camera=cam,n=len(g),mean_abs_error_hz=float(err.abs().mean()),
                             median_abs_error_hz=float(err.abs().median()),within_0_1_hz=float((err.abs()<=.1).mean()),
                             within_0_2_hz=float((err.abs()<=.2).mean()),mean_signed_error_hz=float(err.mean())))
pd.DataFrame(dom_rows).to_csv(OUT/'EXPLORATORY_CAMERA_LASER_DOMINANT_SUMMARY.csv',index=False)

# RMS amplitude comparison is exploratory only: these are condition-level values from different sessions.
a=[]
for _,r in laser.iterrows():
    a.append(dict(rpm=int(r.rpm),camera_bend_rms_mm=float(r.cam_bend_rms),laser_bend_rms_mm=float(r.ldv_bend_rms),bend_ratio=float(r.bend_ratio),
                  camera_torsion_rms_mm=float(r.cam_tors_rms),laser_torsion_rms_mm=float(r.ldv_tors_rms),torsion_ratio=float(r.tors_ratio),flag=str(r.flag)))
ampl=pd.DataFrame(a); ampl.to_csv(OUT/'EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv',index=False)
def corr_summary(x,y):
    return dict(n=len(x),pearson_r=float(np.corrcoef(x,y)[0,1]),rmse_mm=float(np.sqrt(np.mean((x-y)**2))),mean_ratio=float(np.mean(x/y)),median_ratio=float(np.median(x/y)))
amp_s=[]
for name,x,y in [('bending',ampl.camera_bend_rms_mm,ampl.laser_bend_rms_mm),('torsion',ampl.camera_torsion_rms_mm,ampl.laser_torsion_rms_mm)]:
    for label,m in [('all_20',np.ones(len(ampl),bool)),('excluding_320',ampl.rpm<320),('excluding_320_60_80',(ampl.rpm<320)&~ampl.rpm.isin([60,80]))]:
        d=corr_summary(x[m].to_numpy(),y[m].to_numpy()); d.update(metric=name,subset=label); amp_s.append(d)
pd.DataFrame(amp_s).to_csv(OUT/'EXPLORATORY_CAMERA_LASER_RMS_SUMMARY.csv',index=False)

manifest={str(p):sha(p) for p in [CAM_PEAKS,LASER,CAM_LASER,RAW_LASER]}
(OUT/'EXPLORATORY_SOURCE_HASHES.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'EXPLORATORY_RUNTIME.txt').write_text('\n'.join([f'python={sys.version}',f'platform={platform.platform()}',f'camera_rows={len(peaks)}',f'laser_rows={len(laser)}',f'frequency_match_rows={len(match)}','mapping=D01..D20 to e1_20rpm..e20_320rpm by RPM; cross-session exploratory comparison']))

report=f'''# Exploratory Camera–Laser Accuracy and Modal-Interpretation Study

**STATUS: EXPLORATORY ONLY — NOT MANUSCRIPT-AUTHORIZED.**

This report is for experimental-design understanding. It does not promote any result to camera accuracy, simultaneous validation, or structural modal identification.

## Inputs and mapping

- Frozen camera peaks: `{CAM_PEAKS}`; 315 rows, five reference-blind peaks per stream.
- 2025 laser condition table: `{LASER}`; 20 conditions, 20–320 RPM.
- Historical dominant-frequency join table: `{CAM_LASER}`.
- Raw-derived laser summary: `{RAW_LASER}`.
- Condition-level mapping: laser D01–D20 to camera e1_20rpm–e20_320rpm by RPM. The campaigns were not synchronized.

For every camera and each laser bending/torsional dominant frequency, the closest of the camera's five retained peaks was selected. This is a sensitivity-oriented nearest-peak comparison, not a pre-registered validation rule.

## Interpretation boundary

Frequency correspondence can be quantified directly. RMS amplitude ratios are only condition-level cross-session comparisons, not same-waveform accuracy. Modal identification cannot be established from dominant-frequency agreement alone; it requires mode-shape information, spatially registered observables, and a defined structural/modal reference.

Two frequency views are reported separately: `EXPLORATORY_CAMERA_LASER_DOMINANT_SUMMARY.csv` compares each camera's rank-1 peak with each laser dominant frequency; `EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv` selects the closest among five retained camera peaks. The latter is intentionally optimistic and must not be presented as an unbiased validation result.

The camera cam1/cam2 pair observes the same marker, while cam3 uses a different camera–marker path; cam3 must remain separate in interpretation. The laser quantities are derived from center/side channels and geometry-scaled differences; calibration constants and spatial equivalence should be treated as assumptions or historical script-derived quantities unless independently documented.

## What would be needed for a genuine accuracy/validation claim

- simultaneous camera and laser acquisition with a common hardware timebase or recorded synchronization pulse;
- the same physical point/quantity, or a documented geometric transfer function;
- camera and laser calibration uncertainty with propagation;
- waveform/window comparison in common units, not only condition-level RMS/frequency tables;
- predeclared matching rules and tolerances;
- blinded or hold-out conditions, including unfavorable 60, 80, and 320 RPM regimes;
- for modal identification: multiple spatially registered points, phase/mode-shape information, and a structural reference or model.

## Files

- `EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv`
- `EXPLORATORY_CAMERA_LASER_FREQUENCY_SUMMARY.csv`
- `EXPLORATORY_CAMERA_LASER_DOMINANT_SUMMARY.csv`
- `EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv`
- `EXPLORATORY_CAMERA_LASER_RMS_SUMMARY.csv`
- `EXPLORATORY_SOURCE_HASHES.json`
- `EXPLORATORY_RUNTIME.txt`
'''
(OUT/'EXPLORATORY_CAMERA_LASER_ACCURACY_MODAL_REPORT.md').write_text(report)
print(report)
