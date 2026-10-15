# Tree 10 Summary: Vendor Data and MATLAB Analysis (Vendor documentation, geometry specifications, and laser benchmark routines)

## Overview and Scope
Tree 10 contains 28 total scanned files (27 catalogued, 1 identical duplicates).
Vendor Data and MATLAB Analysis (Vendor documentation, geometry specifications, and laser benchmark routines).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m`
- `Video Measurement/RAW_Data/3D_video_system/free_vibration/fqB.m`
- `Video Measurement/RAW_Data/3D_video_system/free_vibration/fqT.m`
- `Video Measurement/RAW_Data/laser_displacement/2D_WTT/BRID2D1_choi.m`
- `Video Measurement/RAW_Data/laser_displacement/free_vibration/fqB.m`
- `Video Measurement/RAW_Data/laser_displacement/free_vibration/fqT.m`
- `Video Measurement/laser_displacement/등류/영각00/BRID2D1.m`
- `Video Measurement/laser_displacement/등류/영각00/brid2d_sub1.m`

## Key Results and Stated Findings
- **`Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m`**: "rms_dat = [ std(dat2(:,1))*scale, std(dat2(:,2))*scale*dp]"
- **`Video Measurement/RAW_Data/3D_video_system/free_vibration/fqB.m`**: "%title('Time History of band pass 8.0~8.2Hz')"
- **`Video Measurement/RAW_Data/3D_video_system/free_vibration/fqB.m`**: "text(2.5,-1,['Negative Damping ratio : ',result_Ndamp,])"
- **`Video Measurement/RAW_Data/3D_video_system/free_vibration/fqT.m`**: "%title('Time History of band pass 8.0~8.2Hz')"
- **`Video Measurement/RAW_Data/3D_video_system/free_vibration/fqT.m`**: "text(2.5,-1,['Negative Damping ratio : ',result_Ndamp,])"
- **`Video Measurement/RAW_Data/laser_displacement/2D_WTT/BRID2D1_choi.m`**: "rms_dat = [ std(dat2(:,1))*scale, std(dat2(:,2))*scale*dp]"
- **`Video Measurement/RAW_Data/laser_displacement/free_vibration/fqB.m`**: "%title('Time History of band pass 8.0~8.2Hz')"
- **`Video Measurement/RAW_Data/laser_displacement/free_vibration/fqB.m`**: "text(2.5,-1,['Negative Damping ratio : ',result_Ndamp,])"

## Planned or Missing Elements
- `TESolution_2025_datasets.md`: ** Wind speeds are approximate, estimated from pitot formula
- `TESolution_2025_datasets.md`: april_marker
- `TESolution_LDV_geometry_and_results.md`: on D38:** Not in original Excel but raw file exists
- `TESolution_LDV_geometry_and_results.md`: "torsion_diff_y_mm is differential vertical displacement at 200 mm from centerli
- `TESolution_LDV_geometry_and_results.md`: ** Bending VIV peak at D05 = 2

## Duplicate Files Across Trees
- `Video Measurement/laser_displacement/자유진동/fq.m`: identical to Tree 10 (`Video Measurement/laser_displacement/모형_setup/fq.m`)
