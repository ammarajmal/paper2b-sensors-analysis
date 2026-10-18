import os

out_path = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/ANALYSIS_TIMELINE.md"

content = """# ANALYSIS_TIMELINE: Chronological History of Paper 2 Research Analyses

This timeline details the chronological evolution of analytical investigations across nine core experimental domains. Each entry lists the date, the primary source file, and the factual result stated in the file.

---

## 1. Acquisition

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2024-06-27** | `02_research_projects/p02_ros_multicamera_shm/p2_sen/P2 Sen - Results/Bridge_data/27June2024_sdcard/EVENT11.TXT` | Preliminary bridge deck telemetry logging recorded multi-channel acceleration and tilt sensor time series. |
| **2024-11-11** | `02_research_projects/P00_shm-displacement-project/context_data/TESolution/Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m` | Vendor laser displacement sensor acquisition performed across conditions D0 through D38 at 360 Hz. |
| **2025-04-13** | `03_datasets/ds004_windtunnel_cameras_2025/metadata.yaml` | Multi-camera wind-tunnel campaign executed across 21 conditions (e0_0rpm to e20_320rpm) using 3 synchronized Sony cameras. |
| **2026-08-08** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/02_BAG_TOPIC_MANIFEST.csv` | Full audit of ROS bag manifests confirming message counts, start timestamps, and topic schemas across all 21 test conditions. |

---

## 2. Timing and Synchronization

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2025-05-15** | `04_code_software/github/shm-displacement-project/scripts/static_camera_tests/static_cam2_test1_jitter_results.csv` | Static camera benchmark measuring inter-frame arrival intervals, confirming median frame rate near 59.96 Hz. |
| **2026-08-13** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_01_STATIC_PRECISION_2026-08-13.md` | Measured per-camera static sampling rates: cam1 = 59.965 Hz, cam2 = 59.936 Hz, cam3 = 60.008 Hz. |
| **2026-08-14** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md` | Measured per-condition camera sampling ranges between 59.94 Hz and 60.01 Hz under normal wind loading. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md` | Timing audit revealed effective frame rate drops to 30–50 Hz above 200 RPM, altering PSD peaks where jitter is severe. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md` | Defined timestamp-based nearest-neighbor resampling without gap interpolation to align camera observations. |

---

## 3. Detection and Admissibility Gating

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2026-06-10** | `04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md` | Corrected manuscript draft error that erroneously listed fiducial markers as 80 mm instead of the true 20 mm / 35 mm tags. |
| **2026-08-02** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md` | Formalized detection admissibility requirements for AprilTag 36h11 markers (nominal 20 mm side length). |
| **2026-08-13** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md` | Quantified quad segmentation failure at 320 RPM: cam1 failed 39.2% (717/1829) and cam2 failed 38.7% (707/1829). |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md` | Standardized 5-gate admissibility protocol: Tag ID 0, Hamming=0, Decision Margin >= 30, Completeness >= 0.80, and velocity gating. |

---

## 4. Camera Calibration and Intrinsics

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2024-10-30** | `03_datasets/ds004_windtunnel_cameras_2025/calibration/calib_data/cam1/calibcheckper.py` | OpenCV checkerboard calibration evaluating reprojection errors across individual calibration frames. |
| **2026-08-02** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/CAMERA_CALIBRATION_INVESTIGATION_2026-08-02.md` | Investigated multiple conflicting intrinsics: ChArUco (fx=56874), manual 720p scaling (fx=37916), wide-angle (fx=789.4), and production. |
| **2026-08-18** | `02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis/outputs/calibration/provisional_camera_info/cam1.yaml` | Documented dual provisional intrinsics profiles for wind tunnel experiments (fx=20327.9) versus static tests (fx=36498.25). |
| **2026-09-02** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md` | Finalized production camera intrinsics: cam1 (fx=20327.9, fy=20240.8), cam2 (fx=25749.5, fy=25819.0), cam3 (fx=25630.9, fy=25590.6). |

---

## 5. Pose Reconstruction and Spatial Operators

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2026-06-17** | `98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin/config/pipeline_config.yaml` | Configured rigid-body pose reconstruction pipeline with 0.020 m tag size. |
| **2026-08-02** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/SPATIAL_OPERATOR_SYNTHESIS_2026-08-02.md` | Synthesized spatial projection operators defining bending as mean vertical displacement and torsion proxy as differential displacement. |
| **2026-08-18** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP02B_INTRINSICS_DISCREPANCY_BENCHMARK_2026-08-18.md` | Benchmarked per-camera bending trajectory projection onto individual camera PCA axes, achieving Spearman rho = 0.794. |
| **2026-09-07** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md` | Formally retracted the 135.14 mm marker separation, establishing that metric torsion requires surveyed baseline geometry. |

---

## 6. Spectral and Modal Identification

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2026-06-10** | `04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md` | Established 6-source consensus natural frequencies at fh = 1.430 Hz (bending) and f_alpha = 3.103 Hz (torsion), ratio = 2.17. |
| **2026-08-13** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_3_MODAL_CONSENSUS_2026-08-13.md` | Demonstrated that single-camera and composite 0.937–0.938 Hz peaks at 60/70/80 RPM are coarse FFT bin-center artifacts. |
| **2026-08-30** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S11_1_LDV_NPERSEG4096_RESONANCE_CHECK_2026-08-30.md` | High-resolution LDS reanalysis (nperseg=4096) found no 0.938 Hz feature and recovered dominant response at 1.406–1.494 Hz. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md` | Third-camera timing-corrected FDD recovered dominant bending frequency at 1.40–1.47 Hz at fine 0.067 Hz resolution. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md` | Synthesized multi-instrument modal recovery confirming facility benchmarks of 1.4303 Hz (bending) and 3.1036 Hz (torsion). |

---

## 7. Laser Displacement Reference Analysis

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2024-11-11** | `02_research_projects/P00_shm-displacement-project/context_data/TESolution/Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m` | Established vendor Laser Displacement Sensor (LDS) parameters for Tunnel A: dside = 10 cm, db = 20 cm, dp = 2.0. |
| **2026-07-31** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md` | Locked laser spacing geometry in SI units: dside = 100 mm, db = 200 mm, dp = 2.0. |
| **2026-08-02** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/EIV_MATCHED_ROW_PROPOSAL_2026-08-02.md` | Mapped laser conditions D0 through D38 to nominal wind speeds, identifying D37 (300 RPM, 5.2810 m/s) and D38 (310 RPM, 5.4747 m/s). |
| **2026-08-14** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S07_2_LDV_TIME_AMPLITUDE_SPECTRAL_2026-08-14.py` | Documented laser record lengths: D0 = 10 s (3600 samples), D1-D38 = 30 s (10800 samples) at fs = 360 Hz. |

---

## 8. Camera-versus-Laser Statistical Comparison

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2026-06-10** | `04_code_software/github/shm-displacement-project/memory/claim_boundary.md` | Legacy B0 package achieved spuriously high correlations (r ~ 0.959) due to off-by-one condition alignment. |
| **2026-08-02** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/REMEDIATION_LOG_2026-08-02.md` | Remediated off-by-one mapping under decision REM-001 by implementing strict integer-RPM condition alignment. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md` | Excluded static e0_0rpm and dropout e20_320rpm, yielding 19 valid integer-matched comparison conditions. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md` | Final 19-condition association: bending Spearman rho = 0.691 (p = 0.0026), Pearson r = 0.616; excluding resonance rho = 0.926. |
| **2026-09-01** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md` | 37-condition third camera association across full sweep: Spearman rho = 0.882, Kendall tau = 0.709, Pearson r = 0.918. |

---

## 9. Uncertainty Budget and Precision Benchmarking

| Date | File | Summary of Stated Finding |
|---|---|---|
| **2026-08-13** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_01_STATIC_PRECISION_2026-08-13.md` | Measured raw pixel static noise floor: cam1 (0.027/0.084 px), cam2 (0.022/0.090 px), cam3 (0.027/0.047 px). |
| **2026-08-14** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md` | Constructed comprehensive uncertainty budget incorporating timing jitter, tag localization, intrinsics drift, and wind turbulence. |
| **2026-08-18** | `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md` | Established laser-benchmarked metric static noise floor: bending RMS = 0.1107 mm, torsion RMS = 0.1821 mm. |
"""

with open(out_path, "w") as f:
    f.write(content.strip() + "\n")

print(f"Wrote {out_path} ({len(content)} bytes)")
