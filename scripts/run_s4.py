import numpy as np, pandas as pd, json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bridgedeck import pose, paths
O=Path(paths.load()["outputs"]); R=paths.REPO/"results"; FH,FA=1.4318,3.0982
det=pd.read_parquet(O/"s2_detect/wtt_main/detections_ALL21.parquet")
CH=["H1_y_mm","H1_x_mm","H2_roll_rad","P0_y_px","P1_y_mm","P2_y_mm","P3_y_mm","P4_y_mm","P6_y_mm","P1_x_mm","P3_x_mm","P3_z_mm","P3_rx_rad","P3_ry_rad","P3_rz_rad","P5_roll_rad"]
def one(key):
    cond,cam=key
    g=det[(det.condition==cond)&(det.camera==cam)&det.detected&(det.decision_margin>=30)].sort_values("frame_idx")
    ch=pose.stream_channels(g,cam); ch.insert(0,"camera",cam); ch.insert(0,"condition",cond)
    row=dict(condition=cond,camera=cam,n=len(ch),mm_per_px=ch.attrs["mm_per_px"],side_px=ch.attrs["side_px"],z_med_mm=ch.attrs["z_med_mm"],order=ch.attrs["order"],
             amb_share=float((ch.P3_amb_ratio<2).mean()))
    t=ch.t_s.to_numpy()
    for c in CH:
        y=ch[c].to_numpy(); row[f"{c}_rms"]=float(np.nanstd(y)); row[f"{c}_pk"]=float(np.nanmax(np.abs(y-np.nanmedian(y))))
        row[f"{c}_Afh"],row[f"{c}_ffh"]=pose.line_amplitude(t,y,FH); row[f"{c}_Afa"],row[f"{c}_ffa"]=pose.line_amplitude(t,y,FA)
    return ch,row
if __name__=="__main__":
    keys=[(c,k) for c in sorted(det.condition.unique()) for k in ("cam1","cam2","cam3") if not (c.startswith("e20") and k!="cam3")]
    with ProcessPoolExecutor(12) as ex: res=list(ex.map(one,keys))
    pd.concat([r[0] for r in res],ignore_index=True).to_parquet(O/"s4_pose_channels_by_frame.parquet",index=False)
    d=pd.DataFrame([r[1] for r in res]); d.to_csv(R/"s4_pose_by_stream.csv",index=False)
    print("streams",len(d),"frames",int(d.n.sum()))
