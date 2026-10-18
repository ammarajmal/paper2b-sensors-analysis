# RUN_REPORT: Audit Verification Self-Check

### 1. Audit Summary Statistics
- **Total Audited Records Generated**: 729 records across Group G1 and Group G2
- **Total Batches Completed**: 10 batches (G1 parts 01–07, G2 parts 01–03)
- **Total Skipped Rows**: 480 rows recorded in `SKIPPED.csv`
- **Total Unreadable Files**: 0 files
- **Random Sampling Test Size**: 25 records (100% physically inspected against source disk)
- **Self-Check Result**: ALL 25 SAMPLES PASSED (100% VERIFIED)

### 2. Randomly Sampled Quote Verifications (25/25)

| # | Path | Quote (<= 15 words) | Word Count | Verbatim in File | Status |
|---|---|---|---|---|---|
| 1 | `Week_042_Contours_segmentation_and_image_measurement.md` | "title:: Week 042 — Contours, segmentation and image measurement" | 9 | True | **PASS** |
| 2 | `01_introduction.tex` | "constrained by three persistent limitations: software-timing variability across" | 8 | True | **PASS** |
| 3 | `README_SETUP.md` | "Stage S1 has passed. Next: S1b static census, S2a detector build" | 11 | True | **PASS** |
| 4 | `1Hz Sine_Exp1_30s_2025-03-22_03-33-50_analysis.txt` | "Experiment Duration: 30 seconds" | 4 | True | **PASS** |
| 5 | `07_conclusion.tex` | "\section{Conclusion}" | 1 | True | **PASS** |
| 6 | `01_introduction.tex` | "Contact-based sensing technologies --- including LVDTs, laser displacement sensors, and" | 10 | True | **PASS** |
| 7 | `48_TB3_cam1_cam2_agreement.tex` | "raw difference in hertz spans 1.6e-05--0.0024~Hz across the 20 admitted conditions" | 11 | True | **PASS** |
| 8 | `after_authors_and_LS.tex` | "Reference-Blind Per-Camera Spectral Analysis of a Wind-Tunnel Bridge-Deck Model" | 9 | True | **PASS** |
| 9 | `stabilized_sony_cam1.csv` | "time_s,tx_rel_m,ty_rel_m,tz_rel_m" | 1 | True | **PASS** |
| 10 | `omrpr-analysis-state.md` | "# omrpr-analysis — state as of 2026-07-22" | 7 | True | **PASS** |
| 11 | `INSTRUCTIONS_MEASUREMENT_project.txt` | "matching RPM is not simultaneous agreement, accuracy or proof of cause." | 11 | True | **PASS** |
| 12 | `static_cam2_test9_jitter_results.csv` | "ros_time_sec,tx_m,ty_m,tz_m" | 1 | True | **PASS** |
| 13 | `42_CLAIM_TO_SECTION_MATRIX.csv` | "CL01,"63 camera streams (21 conditions x 3 cameras) were processed" | 10 | True | **PASS** |
| 14 | `10_preregistration_laser2025.md` | "\|f_camera_dominant - f_laser_dominant\| <= 0.050 Hz" | 6 | True | **PASS** |
| 15 | `12_crossref_check.md` | "The other 24 Measurement entries match Crossref on title/year/pages." | 9 | True | **PASS** |
| 16 | `abstract.tex` | "the bending channel achieved $r = 0.9711$ (RMSE~$\approx 0.288$~mm," | 9 | True | **PASS** |
| 17 | `static_bag_acceptance_review.csv` | "LIKELY_USABLE_WITH_GAP_HANDLING" | 1 | True | **PASS** |
| 18 | `fig06_pipeline_architecture.tex` | "% System architecture diagram: layered view of the OMRPR reconstruction pipeline." | 11 | True | **PASS** |
| 19 | `sony_cam2.csv` | "stamp,img_path" | 1 | True | **PASS** |
| 20 | `untitled2.m` | "clear all" | 2 | True | **PASS** |
| 21 | `OPEN_DECISIONS.md` | "The 2025 laser agrees with the camera better (bending r 0.991 vs 0.971" | 13 | True | **PASS** |
| 22 | `bags_inventory.csv` | "drive_root,size_bytes,mtime,path" | 1 | True | **PASS** |
| 23 | `SYNTHESIS_master_evidence_table.csv` | "direct fiducial precedent" | 3 | True | **PASS** |
| 24 | `fable_variants_phase7_2026-07-07.md` | "# Phase 7 (follow-up) — Fable Bulk-Generation for Phase F, 2026-07-07" | 11 | True | **PASS** |
| 25 | `static_cam2_test1_timestamps.csv` | "frame_idx,ros_time_sec,dt_sec,fps_inst" | 1 | True | **PASS** |

### 3. Detailed Verification Ledger

#### Sample 1: `/mnt/career-legacy/relive/Engineering_Mastery_Plan/weeks/Year_1/Q4/Week_042_Contours_segmentation_and_image_measurement.md`
- **Verbatim Quote**: `title:: Week 042 — Contours, segmentation and image measurement`
- **Word Count**: 9 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 2: `/mnt/phd_data/phd_master/05_publications/p02_sensors_windtunnel/manuscript/sections/01_introduction.tex`
- **Verbatim Quote**: `constrained by three persistent limitations: software-timing variability across`
- **Word Count**: 8 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 3: `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/project_kit_v2_2026-10-15/README_SETUP.md`
- **Verbatim Quote**: `Stage S1 has passed. Next: S1b static census, S2a detector build`
- **Word Count**: 11 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 4: `/mnt/phd_data/phd_master/00_inbox/TESolution/TSYCH/1Hz Sine_Exp1_30s_2025-03-22_03-33-50_analysis.txt`
- **Verbatim Quote**: `Experiment Duration: 30 seconds`
- **Word Count**: 4 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 5: `/mnt/phd_data/phd_master/98_legacy_imports/career_paper2_NEW_unmatched_worktree/PhD_previous_data/paper2_NEW/prev_work/Phd_data_dump/work/omrpr-paper2-manuscript/manuscript/sections/07_conclusion.tex`
- **Verbatim Quote**: `\section{Conclusion}`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 6: `/mnt/phd-legacy/fin_phd/omrpr_manuscript/manuscript/sections/01_introduction.tex`
- **Verbatim Quote**: `Contact-based sensing technologies --- including LVDTs, laser displacement sensors, and`
- **Word Count**: 10 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 7: `/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/48_TB3_cam1_cam2_agreement.tex`
- **Verbatim Quote**: `raw difference in hertz spans 1.6e-05--0.0024~Hz across the 20 admitted conditions`
- **Word Count**: 11 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 8: `/mnt/phd_data/phd_master/05_publications/p02_sensors_mdpi_revision_2026-10/revision_tools/after_authors_and_LS.tex`
- **Verbatim Quote**: `Reference-Blind Per-Camera Spectral Analysis of a Wind-Tunnel Bridge-Deck Model`
- **Word Count**: 9 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 9: `/mnt/phd_data/phd_master/98_legacy_imports/source_old_phd_master_cur/p2/shm-displacement-project-github/stabilized_sony_cam1.csv`
- **Verbatim Quote**: `time_s,tx_rel_m,ty_rel_m,tz_rel_m`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 10: `/mnt/space/data on Computer/~~ DATA TO MOVE/~ SETUPS/ai-state/omrpr-analysis-state.md`
- **Verbatim Quote**: `# omrpr-analysis — state as of 2026-07-22`
- **Word Count**: 7 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 11: `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/project_kit_v2_2026-10-15/INSTRUCTIONS_MEASUREMENT_project.txt`
- **Verbatim Quote**: `matching RPM is not simultaneous agreement, accuracy or proof of cause.`
- **Word Count**: 11 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 12: `/mnt/archive/00_inbox/adev/datasets/omrpr/raw/camera/rosbag/static_bags/cam2/old/static_cam2_test9_jitter_results.csv`
- **Verbatim Quote**: `ros_time_sec,tx_m,ty_m,tz_m`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 13: `/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/42_CLAIM_TO_SECTION_MATRIX.csv`
- **Verbatim Quote**: `CL01,"63 camera streams (21 conditions x 3 cameras) were processed`
- **Word Count**: 10 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 14: `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/project_kit_v2_2026-10-15/upload_sensors/10_preregistration_laser2025.md`
- **Verbatim Quote**: `|f_camera_dominant - f_laser_dominant| <= 0.050 Hz`
- **Word Count**: 6 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 15: `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/project_kit_v2_2026-10-15/upload_sensors/12_crossref_check.md`
- **Verbatim Quote**: `The other 24 Measurement entries match Crossref on title/year/pages.`
- **Word Count**: 9 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 16: `/mnt/phd_data/phd_master/05_publications/p02_measurement_revision_2026-10/manuscript/abstract.tex`
- **Verbatim Quote**: `the bending channel achieved $r = 0.9711$ (RMSE~$\approx 0.288$~mm,`
- **Word Count**: 9 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 17: `/mnt/phd_data/phd_master/02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis/outputs/diagnostics/static_bag_acceptance_review.csv`
- **Verbatim Quote**: `LIKELY_USABLE_WITH_GAP_HANDLING`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 18: `/mnt/phd-legacy/dissertation/figures/paper2/fig06_pipeline_architecture.tex`
- **Verbatim Quote**: `% System architecture diagram: layered view of the OMRPR reconstruction pipeline.`
- **Word Count**: 11 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 19: `/mnt/phd_data/phd_master/03_datasets/ds004_windtunnel_cameras_2025/processed/export/e12_160rpm_run1/sony_cam2/sony_cam2.csv`
- **Verbatim Quote**: `stamp,img_path`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 20: `/mnt/phd_data/phd_master/09_courses_training/c02_fall_2022/3. Sensors/MATLAB/untitled2.m`
- **Verbatim Quote**: `clear all`
- **Word Count**: 2 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 21: `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/project_kit_v2_2026-10-15/OPEN_DECISIONS.md`
- **Verbatim Quote**: `The 2025 laser agrees with the camera better (bending r 0.991 vs 0.971`
- **Word Count**: 13 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 22: `/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/bags_inventory.csv`
- **Verbatim Quote**: `drive_root,size_bytes,mtime,path`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 23: `/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research/02_KNOWLEDGE_BASE/literature/SYNTHESIS_master_evidence_table.csv`
- **Verbatim Quote**: `direct fiducial precedent`
- **Word Count**: 3 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 24: `/mnt/phd-legacy/fin_phd/omrpr_outputs_review/fable_variants_phase7_2026-07-07.md`
- **Verbatim Quote**: `# Phase 7 (follow-up) — Fable Bulk-Generation for Phase F, 2026-07-07`
- **Word Count**: 11 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

#### Sample 25: `/mnt/archive/00_inbox/adev/datasets/omrpr/raw/camera/rosbag/static_bags/cam2/old/static_cam2_test1_timestamps.csv`
- **Verbatim Quote**: `frame_idx,ros_time_sec,dt_sec,fps_inst`
- **Word Count**: 1 words (Max allowed: 15)
- **Physical Verification**: Located character-for-character in source file: `True`
- **Result**: `PASS`

