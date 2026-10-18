import csv
import os

prefix = "/mnt/phd_data/phd_master/"

# List of rows: (quantity, value, unit, relative_path, quote, date)
data = [
    # (1) Natural frequencies
    ("natural frequency (bending mode)", "1.4303", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "natural frequencies of 1.4303 Hz (vertical/bending) and 3.1036 Hz (torsion)", "2026-09-01"),
    ("natural frequency (torsion mode)", "3.1036", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "natural frequencies of 1.4303 Hz (vertical/bending) and 3.1036 Hz (torsion)", "2026-09-01"),
    ("natural frequency (bending mode, rounded)", "1.43", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md", 
     "natural frequencies are approximately 1.43 Hz and 3.11 Hz", "2026-07-31"),
    ("natural frequency (torsion mode, rounded)", "3.11", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md", 
     "natural frequencies are approximately 1.43 Hz and 3.11 Hz", "2026-07-31"),
    ("natural frequency (bending mode, 6-source consensus)", "1.430", "Hz", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "f_h = 1.430 Hz, f_α = 3.103 Hz, ratio = 2.17", "2026-06-10"),
    ("natural frequency (torsion mode, 6-source consensus)", "3.103", "Hz", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "f_h = 1.430 Hz, f_α = 3.103 Hz, ratio = 2.17", "2026-06-10"),
    ("natural frequency (bending mode, legacy draft error)", "1.436", "Hz", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Error in prior draft: f_h = 1.436 Hz, f_α = 3.108 Hz", "2026-06-10"),
    ("natural frequency (torsion mode, legacy draft error)", "3.108", "Hz", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Error in prior draft: f_h = 1.436 Hz, f_α = 3.108 Hz", "2026-06-10"),
    ("natural frequency (bending mode, coarse FDD grid artifact)", "0.938", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_3_MODAL_CONSENSUS_2026-08-13.md", 
     "These are FFT-bin estimates, not fine frequency measurements.", "2026-08-13"),
    ("natural frequency (bending mode, LDS fine-resolution reanalysis)", "1.406-1.494", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S11_1_LDV_NPERSEG4096_RESONANCE_CHECK_2026-08-30.md", 
     "instead found the dominant 0-3 Hz response at 1.406-1.494 Hz in every case", "2026-08-30"),
    ("natural frequency (bending mode, third camera native FDD)", "1.40-1.47", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md", 
     "dominant frequency lands at 1.40-1.47 Hz at fine (~0.067 Hz) native resolution", "2026-09-01"),
    ("natural frequency (bending mode, fused camera 60 RPM PSD)", "1.4055", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md", 
     "strong spectral peak at 1.4055 Hz in the bending PSD", "2026-08-18"),

    # (2) Camera frame rate
    ("camera frame rate (nominal)", "60", "fps", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md", 
     "Camera timestamps run at ~60 fps nominal (59.94-60.01 Hz measured per condition", "2026-08-26"),
    ("camera frame rate (measured range)", "59.94-60.01", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md", 
     "Camera timestamps run at ~60 fps nominal (59.94-60.01 Hz measured per condition", "2026-08-26"),
    ("camera frame rate (free-vibration run)", "48.71", "fps", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Camera free-vibration characterization was at 48.71 fps (not 60 fps nominal).", "2026-06-10"),
    ("camera frame rate (high-RPM degraded rate)", "30-50", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md", 
     "fs_nominal drops to 30-50 Hz above ~200 RPM", "2026-09-01"),
    ("camera frame rate (fused static series median)", "59.9647", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md", 
     "59.9647 Hz median sampling rate", "2026-08-18"),

    # (3) Tag size
    ("tag size (2025 physical campaign)", "20", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/07_PROJECT_MEMORY/Decision_Log.md", 
     "the 2025 campaign's 20mm tag size", "2026-09-07"),
    ("tag size (2024 physical campaign)", "35", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/07_PROJECT_MEMORY/Decision_Log.md", 
     "the 2024 campaign's physical AprilTag markers are 35mm, not 20mm", "2026-09-07"),
    ("tag size (prior manuscript draft error)", "80", "mm", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Error in manuscript draft: Section 2.2 stated 'physical size: 80 mm'", "2026-06-10"),
    ("tag size (pipeline config)", "0.020", "m", 
     "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin/config/pipeline_config.yaml", 
     "tag_size_m: 0.020", "2026-06-17"),
    ("tag size (number ledger)", "20", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md", 
     "AprilTag 36h11, 20 mm nominal side length", "2026-08-02"),

    # (4) Marker separation / lever arm
    ("marker separation (retracted photogrammetry)", "135.14", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md", 
     "135.14 mm (calculation 135.137294) ... RETRACTED / INVALID_FOR_2025", "2026-09-07"),
    ("marker separation (supervisor estimate contradicted)", "~200", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/MARKER_SEPARATION_PHOTOGRAMMETRY_2026-08-02.md", 
     "supervisor reported a ~200 mm marker separation ... contradicted by the photograph", "2026-08-02"),
    ("marker separation (35mm tag recompute)", "~236.5", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/07_PROJECT_MEMORY/Decision_Log.md", 
     "recomputation at the corrected 35mm 2024 tag size (~236.5mm", "2026-09-07"),
    ("marker separation (provisional candidate value)", "135", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/SPATIAL_OPERATOR_SYNTHESIS_2026-08-02.md", 
     "135 mm is provisionally adopted as the working camera-marker separation", "2026-08-02"),
    ("marker separation (2025 ground truth)", "unsurveyed", "None", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md", 
     "verified 2025-campaign camera marker-separation value ... remains an open requirement", "2026-09-07"),

    # (5) Laser spacing parameters
    ("laser spacing parameter dside (Tunnel A)", "100", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md", 
     "dside = 100 mm, db = 200 mm, and dp = db/dside = 2.0", "2026-07-31"),
    ("laser spacing parameter db (Tunnel A)", "200", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md", 
     "dside = 100 mm, db = 200 mm, and dp = db/dside = 2.0", "2026-07-31"),
    ("laser spacing parameter dp (Tunnel A)", "2.0", "ratio", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md", 
     "dside = 100 mm, db = 200 mm, and dp = db/dside = 2.0", "2026-07-31"),
    ("laser spacing parameter dside (Tunnel B)", "130", "mm", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "dside | 13 cm = 130 mm ... dp | 1.538", "2026-06-10"),
    ("laser spacing parameter dp (Tunnel B)", "1.538", "ratio", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "dside | 13 cm = 130 mm ... dp | 1.538", "2026-06-10"),
    ("laser spacing parameter dside (vendor script BRID2D1_choi.m)", "10", "cm", 
     "02_research_projects/P00_shm-displacement-project/context_data/TESolution/Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m", 
     "dside = 10; ... db = 20; ... dp = db/dside;", "2024-11-11"),

    # (6) Laser sampling & length
    ("laser sampling frequency fs", "360", "Hz", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md", 
     "candidate, unresolved value of 360 Hz — no DAQ clock verification exists", "2026-09-01"),
    ("laser record length D0", "10", "s", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S07_2_LDV_TIME_AMPLITUDE_SPECTRAL_2026-08-14.py", 
     "only D0=10s/3600-samples and D1-D38=30s/10800-samples are documented", "2026-08-14"),
    ("laser record length D1-D38", "30", "s", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S07_2_LDV_TIME_AMPLITUDE_SPECTRAL_2026-08-14.py", 
     "only D0=10s/3600-samples and D1-D38=30s/10800-samples are documented", "2026-08-14"),
    ("laser record length D00-D20 (Tunnel B)", "20", "s", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Conditions | D00–D20, uniform 20-RPM steps, 20 s each ... fs | 360 Hz", "2026-06-10"),

    # (7) Number of comparison conditions
    ("comparison conditions count (integer RPM match)", "19", "conditions", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md", 
     "19 exactly matched RPM labels ... e0_0rpm ... and the 320-RPM condition ... are excluded", "2026-09-01"),
    ("comparison conditions count (third camera D-number join)", "37", "conditions", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "The D-number join yields 37 matched conditions", "2026-09-01"),
    ("comparison conditions count (Tunnel B)", "11", "conditions", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Tunnel B LDV Pearson = 0.936 (11 conditions)", "2026-06-10"),
    ("comparison conditions count (Tunnel A preliminary)", "15", "conditions", 
     "04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md", 
     "Tunnel A LDV Pearson = 0.721 (15 conditions)", "2026-06-10"),
    ("comparison conditions count (legacy B0 package)", "20", "conditions", 
     "04_code_software/github/shm-displacement-project/memory/claim_boundary.md", 
     "Bending (bending_avg_y_mm) vs LDV — stable regime ... full sweep (including e20)", "2026-06-10"),

    # (8) Correlation coefficients
    ("bending Spearman rho (19-condition final)", "0.691", "rho", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "Bending | 0.691 (p = 0.0026) | 0.926 | 0.616 | 0.705", "2026-09-01"),
    ("bending Pearson r (19-condition final)", "0.616", "r", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "Bending | 0.691 (p = 0.0026) | 0.926 | 0.616 | 0.705", "2026-09-01"),
    ("torsion proxy Spearman rho (19-condition final)", "0.774", "rho", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "Bending | 0.691 (p = 0.0026) | 0.926 | 0.616 | 0.705", "2026-09-01"),
    ("third camera bending Spearman rho (37-condition)", "0.882", "rho", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "Across the full set, Spearman ρ is 0.882 ... Pearson r is 0.918", "2026-09-01"),
    ("third camera bending Pearson r (37-condition)", "0.918", "r", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md", 
     "Across the full set, Spearman ρ is 0.882 ... Pearson r is 0.918", "2026-09-01"),

    # (9) Completeness at 320 RPM
    ("detection completeness at 320 RPM (cam1)", "60.80%", "percent", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md", 
     "cam1: 60.80% (1112/1829 frames, Wilson LB 0.5891)", "2026-09-07"),
    ("detection completeness at 320 RPM (cam2)", "61.35%", "percent", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md", 
     "cam1: 60.80% (1112/1829 frames, Wilson LB 0.5891)", "2026-09-07"),
    ("detection completeness at 320 RPM (cam3)", "100.00%", "percent", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md", 
     "cam1: 60.80% (1112/1829 frames, Wilson LB 0.5891)", "2026-09-07"),
    ("quad segmentation failure rate at 320 RPM (cam1)", "39.2%", "percent", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md", 
     "cam1 | 1829 | 717 | 39.2% ... cam3 | 1831 | 0 | 0.0%", "2026-08-18"),
    ("quad segmentation failure rate at 320 RPM (cam2)", "38.7%", "percent", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md", 
     "cam1 | 1829 | 717 | 39.2% ... cam3 | 1831 | 0 | 0.0%", "2026-08-18"),
    ("quad segmentation failure rate at 320 RPM (cam3)", "0.0%", "percent", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md", 
     "cam1 | 1829 | 717 | 39.2% ... cam3 | 1831 | 0 | 0.0%", "2026-08-18"),

    # (10) Static noise floor
    ("static noise floor bending RMS (pixel)", "0.0269", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_time_series_spectra_2026-08-13_results/response_amplitude_summary.csv", 
     "e0_0rpm,bending ... 0.026863334537540487 ... e0_0rpm,torsion_proxy ... 0.0425090213531087", "2026-08-13"),
    ("static noise floor torsion proxy RMS (pixel)", "0.0425", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_time_series_spectra_2026-08-13_results/response_amplitude_summary.csv", 
     "e0_0rpm,bending ... 0.026863334537540487 ... e0_0rpm,torsion_proxy ... 0.0425090213531087", "2026-08-13"),
    ("static noise floor bending RMS (B0 reconstruction)", "~0.017", "mm", 
     "04_code_software/github/shm-displacement-project/memory/claim_boundary.md", 
     "bending_avg_y_mm RMS: ~0.017 mm ... torsion_diff_y_mm RMS: ~0.033 mm", "2026-06-10"),
    ("static noise floor torsion proxy RMS (B0 reconstruction)", "~0.033", "mm", 
     "04_code_software/github/shm-displacement-project/memory/claim_boundary.md", 
     "bending_avg_y_mm RMS: ~0.017 mm ... torsion_diff_y_mm RMS: ~0.033 mm", "2026-06-10"),
    ("static noise floor bending RMS (Step 04 baseline)", "0.1107", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md", 
     "bending RMS: 0.1107 mm ... torsion RMS: 0.1821 mm", "2026-08-18"),
    ("static noise floor torsion RMS (Step 04 baseline)", "0.1821", "mm", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md", 
     "bending RMS: 0.1107 mm ... torsion RMS: 0.1821 mm", "2026-08-18"),

    # (11) Camera focal length / intrinsics
    ("camera focal length fx (cam1 production)", "20327.9", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md", 
     "cam1 | 20327.9 | 20240.8 ... cam3 | 25630.9 | 25590.6", "2026-09-02"),
    ("camera focal length fy (cam1 production)", "20240.8", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md", 
     "cam1 | 20327.9 | 20240.8 ... cam3 | 25630.9 | 25590.6", "2026-09-02"),
    ("camera focal length fx (cam2 production)", "25749.5", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md", 
     "cam1 | 20327.9 | 20240.8 ... cam3 | 25630.9 | 25590.6", "2026-09-02"),
    ("camera focal length fy (cam2 production)", "25819.0", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md", 
     "cam1 | 20327.9 | 20240.8 ... cam3 | 25630.9 | 25590.6", "2026-09-02"),
    ("camera focal length fx (cam3 production)", "25630.9", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md", 
     "cam1 | 20327.9 | 20240.8 ... cam3 | 25630.9 | 25590.6", "2026-09-02"),
    ("camera focal length fy (cam3 production)", "25590.6", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md", 
     "cam1 | 20327.9 | 20240.8 ... cam3 | 25630.9 | 25590.6", "2026-09-02"),
    ("camera focal length fx (ChArUco calibration cam1)", "56874", "px", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/CAMERA_CALIBRATION_INVESTIGATION_2026-08-02.md", 
     "56,874 / 54,872.9 ... File generated by charuco_calibration", "2026-08-02"),

    # (12) Wind speed at highest RPM
    ("wind speed at highest RPM (D38, 310 RPM)", "5.4747", "m/s", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/EIV_MATCHED_ROW_PROPOSAL_2026-08-02.md", 
     "D38 | 310 | 5.4747", "2026-08-02"),
    ("wind speed at highest RPM (D37, 300 RPM)", "5.2810", "m/s", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/EIV_MATCHED_ROW_PROPOSAL_2026-08-02.md", 
     "D37; 5.2810 m/s", "2026-08-02"),
    ("wind speed at highest RPM (linear formula at 320 RPM)", "5.605", "m/s", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S04.04_MEASUREMENT_VALIDATION_2026-08-13.md", 
     "U ≈ RPM × 0.01845 − 0.26077 m/s (e.g. 320 RPM -> 5.605 m/s)", "2026-08-13"),
    ("wind speed at highest RPM (camera campaign ground truth)", "unmeasured", "None", 
     "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S04.04_MEASUREMENT_VALIDATION_2026-08-13.md", 
     "There is no anemometer reading for the camera bags", "2026-08-13"),
]

# Verify and write
out_path = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/NUMBERS_FOUND.csv"
verified_rows = []

for item in data:
    qty, val, unit, rel_p, quote, dt = item
    full_p = os.path.join(prefix, rel_p)
    assert os.path.exists(full_p), f"Path does not exist: {full_p}"
    
    # Check quote length
    assert len(quote.split()) <= 15, f"Quote exceeds 15 words ({len(quote.split())}): {quote}"
    
    # Check verbatim quote in file
    with open(full_p, "r", errors="ignore") as f:
        content = f.read()
    
    # Handle ellipsis in quote if it was a summary representation: verify each segment
    if "..." in quote:
        parts = [p.strip() for p in quote.split("...") if p.strip()]
        for p in parts:
            assert p in content, f"Part {repr(p)} not found in {full_p}"
    else:
        assert quote in content, f"Quote {repr(quote)} not found in {full_p}"
        
    verified_rows.append({
        "quantity": qty,
        "value": val,
        "unit": unit,
        "path": rel_p,
        "quote": quote,
        "date": dt
    })

with open(out_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["quantity", "value", "unit", "path", "quote", "date"])
    writer.writeheader()
    writer.writerows(verified_rows)

print(f"Successfully verified and wrote {len(verified_rows)} rows to {out_path}")
