# PAPER2_COVERAGE: Research Evidence Map for Paper 2

This document maps fourteen core research questions to the primary files in the repository that directly address them. For each question, up to six directly addressing files are listed in order of relevance, accompanied by a one-sentence factual summary and a character-for-character quotation of at most 15 words. All 84 cited paths have been physically verified on disk (0 missing).

---

## 1. Per-camera frequency recovery (each camera alone vs the structure's natural frequencies)

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_3_MODAL_CONSENSUS_2026-08-13.md`**  
   Reports condition-level Frequency Domain Decomposition (FDD) dominant peaks across camera streams where single-camera and composite signals collapse to coarse FFT bin centers of 0.937–0.938 Hz at 60/70/80 RPM rather than resolving the true structural natural frequency.  
   *Quote:* "These are FFT-bin estimates, not fine frequency measurements."

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md`**  
   Evaluates an independent third camera instrument whose bending dominant frequency recovers 1.40–1.47 Hz at fine native resolution (~0.067 Hz) near the facility-confirmed natural bending frequency of 1.4303 Hz.  
   *Quote:* "dominant frequency lands at 1.40-1.47 Hz at fine (~0.067 Hz) native resolution"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`**  
   Synthesizes multi-instrument frequency recovery evidence establishing that the single-camera and composite 0.937–0.938 Hz peak is a grid resolution artifact while the physical specimen natural frequency is 1.4303 Hz (bending) and 3.1036 Hz (torsion).  
   *Quote:* "reported location of 0.937–0.938 Hz is a bin center forced by the sampling grid"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S11_1_LDV_NPERSEG4096_RESONANCE_CHECK_2026-08-30.md`**  
   Performs fine-resolution spectral reanalysis of the laser displacement sensor (LDS) record at 60/70/80 RPM, finding no feature at 0.937–0.938 Hz and recovering the dominant response at 1.406–1.494 Hz.  
   *Quote:* "instead found the dominant 0-3 Hz response at 1.406-1.494 Hz in every case"

5. **`00_inbox/Paper2_Review_2026-09-06/21_FULL_PER_CAMERA_FREQUENCY_SWEEP.csv`**  
   Compiles the Supplement S1 master sweep recording dominant frequency peaks and validation gates for all 60 admitted camera streams across all 21 wind-tunnel conditions.  
   *Quote:* "all predeclared numeric gates passed"

6. **`00_inbox/Paper2_Review_2026-09-06/25A_REFERENCE_BLIND_PEAKS_FROZEN.csv`**  
   Records the Supplement S2 table of 315 reference-blind frequency peaks extracted and frozen prior to external benchmark comparison to prevent confirmation bias.  
   *Quote:* "condition,rpm,camera,peak_rank,peak_frequency_hz,peak_power,normalized_peak_power,prominence,rayleigh_resolution_hz"

---

## 2. Effect of timestamps or resampling on spectra

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md`**  
   Compares naive nominal-rate PSD against timestamp-resampled PSD for the third camera, demonstrating that dominant resonance peak estimates match at 60/70/80 RPM but diverge at low motion and degraded frame rates.  
   *Quote:* "the timestamp fix changes the answer exactly where jitter is worst"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`**  
   Demonstrates in Figure 4 that naive-nominal-rate versus timestamp-resampled Welch PSDs both peak at the facility-confirmed 1.4303 Hz bending line for 70 RPM.  
   *Quote:* "showing the accepted frequency estimate is not sensitive to the timing correction"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Specifies the timestamp-based resampling rule assigning cam1 and cam2 observations to nearest cam3 timestamps within 0.75x dt without interpolation across gaps exceeding 1.5x dt.  
   *Quote:* "assigned to the nearest cam3 timestamp only if within 0.75 times"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_TIME_SERIES_SPECTRA_2026-08-13.md`**  
   Evaluates the effect of timestamp-derived sampling rates (~60 Hz) on Welch PSD bin spacing (df ≈ 0.94 Hz for nperseg=64) and establishes that contiguous finite runs are analyzed without bridging gaps.  
   *Quote:* "coarse approximately 0.94 Hz bin spacing near the observed approximately 60 Hz"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S10_04_TWO_PERSONA_INTERNAL_REVIEW_2026-08-27.md`**  
   Explains that reported FDD peak frequencies are constrained by Welch grid bin centers and that small frequency spreads across conditions reflect per-camera frame-rate jitter.  
   *Quote:* "the sub-hertz spread across conditions reflects fps jitter, not independently resolved frequency content"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md`**  
   Quantifies camera frame-interval timing jitter at less than 2 ms RMS and confirms zero frame index gaps on the static segment.  
   *Quote:* "<2 ms RMS frame-interval jitter; 0% missing on the static segment"

---

## 3. AprilTag detection gates and thresholds (hamming, decision margin, completeness, velocity)

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_02_THRESHOLD_SENSITIVITY_2026-08-13.md`**  
   Derives and sensitivity-tests the candidate production gates: expected tag ID, Hamming = 0, decision margin >= 30, finite corners, one-sided 95% Wilson lower bound >= 0.95, and velocity cutoff 27.746787 px/frame.  
   *Quote:* "Candidate cutoff: midpoint of clean maximum and first failure: 27.746787209837"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_03_ADMISSIBILITY_MANIFEST_2026-08-13.md`**  
   Applies the observation and velocity gates across all 63 camera streams, classifying 60 streams as admissible, 2 streams as rejected (cam1 and cam2 at 320 RPM), and 1 stream as diagnostic-only (cam3 at 320 RPM).  
   *Quote:* "Every non-320RPM stream is admissible (60/60), matching accepted S04.04 Finding 5."

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Formalizes the five independent admissibility gates plus the 27.746787 px/frame velocity cutoff and 5x static compensation-validity multiplier.  
   *Quote:* "exact expected tag ID, Hamming distance equal to zero, decision margin of at least 30"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/scripts/generate_official_quality_scores.py`**  
   Implements the official quality score evaluation, Wilson 95% confidence interval computation, and gate threshold logic in code.  
   *Quote:* "exact tag ID match, hamming==0, margin>=30, finite corners, valid status"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`**  
   Records the locked candidate thresholds in Section F including Hamming = 0, margin >= 30, Wilson LB >= 0.95, and velocity cutoff 27.746787 px/frame.  
   *Quote:* "candidate velocity cutoff: 27.746787 px/frame; Wilson bound 0.95"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md`**  
   Demonstrates that the velocity gate flags the regime where AprilTag quad segmentation fails due to motion blur and quiet-zone erosion.  
   *Quote:* "No other condition approaches the failure-onset velocity range."

---

## 4. Static (no-wind) noise floor

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_01_STATIC_PRECISION_2026-08-13.md`**  
   Measures raw static pixel noise floor on the e0_0rpm condition across all three cameras (cam1 RMS 0.027/0.084 px, cam2 0.022/0.090 px, cam3 0.027/0.047 px).  
   *Quote:* "cam1 RMS 0.0268 / 0.0842 ... cam2 RMS 0.0215 / 0.0902"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md`**  
   Calculates provisional metric static noise floor on the fused e0_0rpm series as 0.1107 mm bending RMS and 0.1821 mm torsion RMS using laser-corrected intrinsics.  
   *Quote:* "bending RMS: 0.1107 mm ... torsion RMS: 0.1821 mm"

3. **`04_code_software/github/shm-displacement-project/memory/claim_boundary.md`**  
   Records legacy B0 package static noise floor estimates of ~0.017 mm bending RMS and ~0.033 mm torsion proxy RMS.  
   *Quote:* "bending_avg_y_mm RMS: ~0.017 mm ... torsion_diff_y_mm RMS: ~0.033 mm"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_time_series_spectra_2026-08-13_results/response_amplitude_summary.csv`**  
   Reports condition-level static baseline spatial operator RMS values for e0_0rpm as 0.0269 px for bending and 0.0425 px for torsion proxy.  
   *Quote:* "e0_0rpm,bending ... 0.026863334537540487 ... e0_0rpm,torsion_proxy ... 0.0425090213531087"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/mining_reports/LEGACY_ANALYSIS_REPORT_shm_pipeline_audit.md`**  
   Documents legacy near-floor threshold definitions of 0.035 mm for bending and 0.067 mm for torsion proxy.  
   *Quote:* "near-floor threshold: Bending: 0.035 mm, Torsion proxy: 0.067 mm"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md`**  
   Synthesizes static precision as Item 2 of the uncertainty budget, citing raw RMS of 0.02–0.03 px and raw drift <= 0.011 px per 1000 frames.  
   *Quote:* "Raw RMS 0.02-0.03px raw; drift <=0.011 px/1000fr raw"

---

## 5. Camera calibration and intrinsics: where the values come from, and any statement that they are verified or not

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/CAMERA_CALIBRATION_INVESTIGATION_2026-08-02.md`**  
   Traces active production calibration values to standard checkerboard ROS calibration and custom ChArUco package, finding four mutually inconsistent fx/fy determinations and identifying narrow-FOV planar-calibration degeneracy.  
   *Quote:* "mutually inconsistent (20k vs 57k) focal-length estimates at the same ~600mm-equivalent zoom"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md`**  
   Audits camera intrinsics in pipeline_config.yaml (fx=20327.9, 25749.5, 25630.9), confirming extrinsics.yaml is 0 bytes and noting a conflict between low reprojection error claims and documented planar degeneracy.  
   *Quote:* "Extrinsics: confirmed empty. config/extrinsics.yaml exists as a file but is 0 bytes."

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md`**  
   Mandates as a foundational constraint that no camera intrinsic calibration is verified and metric reconstructions remain unverified sensitivity envelopes.  
   *Quote:* "No available camera intrinsic calibration is verified."

4. **`02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis/outputs/calibration/provisional_camera_info/cam1.yaml`**  
   Designates camera info profiles (wtt_experiment fx=20327.9, static_test fx=36498.25) explicitly with status PROVISIONAL_UNVERIFIED.  
   *Quote:* "status: PROVISIONAL_UNVERIFIED"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Formulates manuscript methodology under the constraint that camera calibration status is unverified and image-plane pixel quantities are analyzed directly.  
   *Quote:* "no available camera intrinsic calibration is verified"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP02B_INTRINSICS_DISCREPANCY_BENCHMARK_2026-08-18.md`**  
   Documents that provisional intrinsics with bad focal lengths inflate apparent depth/Z noise in solvePnP.  
   *Quote:* "plausibly a symptom of the still-provisional intrinsics' bad focal length"

---

## 6. Laser file-to-RPM mapping (list every mapping stated, with the file that states it) and laser units (cm vs mm)

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md`**  
   Defines the corrected 19-condition mapping (D2->20 RPM, D4->40, D6->50, D8->60, D10->70, D12->80, D14->90, D16->100, D18->110, D19->120, D21->140, D23->160, D25->180, D27->200, D29->220, D31->240, D33->260, D35->280, D37->300 RPM) and notes laser spacing parameters dside=100 mm, db=200 mm.  
   *Quote:* "Laser condition mapping: D2 (20 RPM), D4 (40 RPM)"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/EIV_MATCHED_ROW_PROPOSAL_2026-08-02.md`**  
   Tabulates the complete delivered D0–D38 sequence with commanded RPM and measured wind speed, mapping D2 through D37 to exact camera conditions and listing D38 as 310 RPM.  
   *Quote:* "D2 | 20 | 0.1348 ... D38 | 310 | 5.4747"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Documents laser calibration with pvolt = 2.7 cm/V, conversion from centimetres to millimetres, and rejection of the legacy D(n) -> D(n+1) offset convention.  
   *Quote:* "Calibration applies (data - bias) * pvolt with pvolt = 2.7 cm/V per channel"

4. **`04_code_software/github/shm-displacement-project/memory/claim_boundary.md`**  
   Records the legacy off-by-one mapping convention where D02 was mapped to 40 RPM, D03 to 50 RPM, up through D19 to 240 RPM, producing artificial correlations ~0.96.  
   *Quote:* "D02 was mapped to 40 RPM instead of 20 RPM"

5. **`02_research_projects/P00_shm-displacement-project/context_data/TESolution/Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m`**  
   Provides the vendor MATLAB script demonstrating raw laser sensitivity in cm/V (pvolt = 2.7) and geometry parameters dside = 10 cm, db = 20 cm.  
   *Quote:* "pvolt = 2.7; % cm/V ... dside = 10; % cm"

6. **`04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md`**  
   Documents two distinct tunnel geometries and laser mappings: Tunnel A (D0–D38, dside=100 mm, dp=2.0) versus Tunnel B (D00–D20, dside=130 mm, dp=1.538).  
   *Quote:* "dside | 10 cm = 100 mm ... dside | 13 cm = 130 mm"

---

## 7. Camera-versus-laser comparison statistics

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`**  
   Reports Table 2 association statistics on 19 conditions: bending Spearman ρ=0.691 (p=0.0026), excl. resonance=0.926, Pearson r=0.616; torsion-proxy Spearman ρ=0.774 (p=0.0006), excl. resonance=0.909, Pearson r=0.258 (n.s.).  
   *Quote:* "Bending | 0.691 (p = 0.0026) | 0.926 | 0.616 | 0.705"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S08_2_CONDITION_COMPARISON_2026-08-14.md`**  
   Computes paired permutation rank and linear association statistics and BCa bootstrap confidence intervals on the 19 matched conditions with resonance-excluded subsets.  
   *Quote:* "Spearman ρ and Pearson r use a paired permutation test"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_2_TESOLUTION_LDV_RANK_ASSOCIATION_2026-09-01.md`**  
   Reports rank and linear association for the third camera versus laser across 37 D-number-matched conditions: bending Spearman ρ = 0.882, Kendall τ = 0.709, Pearson r = 0.918.  
   *Quote:* "Across the full set, Spearman ρ is 0.882 ... Pearson r is 0.918"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md`**  
   Documents Phase 5 preliminary validation numbers: bending Pearson r = 0.6272, Spearman ρ = 0.6912; torsion-proxy Pearson r = 0.3001, Spearman ρ = 0.7737.  
   *Quote:* "bending Pearson r is 0.6272 and Spearman rho is 0.6912"

5. **`04_code_software/github/shm-displacement-project/memory/claim_boundary.md`**  
   Records legacy B0 package validation statistics using off-by-one mapping: bending Pearson r ~0.959, torsion proxy Pearson r ~0.968.  
   *Quote:* "Bending ... Pearson r | ~0.959 ... Torsion proxy ... Pearson r | ~0.968"

6. **`04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md`**  
   Reports preliminary comparison correlations for Tunnel B (Pearson r = 0.936, 11 conditions) and Tunnel A (Pearson r = 0.721, 15 conditions).  
   *Quote:* "Tunnel B LDV Pearson = 0.936 (11 conditions) vs Tunnel A LDV Pearson = 0.721"

---

## 8. Uncertainty budget

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md`**  
   Synthesizes a seven-item uncertainty budget distinguishing quantified components (timing, static noise, detection confidence, sensitivity envelopes, spectral CIs) from structurally unquantifiable campaign confounding.  
   *Quote:* "No single combined 'total uncertainty' figure is computed or implied here."

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`**  
   Presents Table 3 rolling up all seven quantified and unquantified uncertainty items across Sections 3.1–3.7 without pooling into a combined error bar.  
   *Quote:* "Table 3 synthesizes every quantified and unquantified uncertainty component"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Predeclares the seven-item uncertainty budget framework reporting each component on its own scale and domain.  
   *Quote:* "A seven-item uncertainty budget separately quantifies, without combining"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_1_ROBUSTNESS_MATRIX_2026-08-14.md`**  
   Evaluates calibration-family sensitivity (0.85x–1.03x) and axis/operator sensitivity (1.26x–55.5x) envelopes feeding Item 4 of the budget.  
   *Quote:* "These two envelopes are not additive and not a combined uncertainty figure"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_TIME_SERIES_SPECTRA_2026-08-13.md`**  
   Quantifies within-record spectral uncertainty via chi-square PSD intervals and Student-t RMS intervals, explicitly bounding their scope.  
   *Quote:* "this is conditional, within-record spectral uncertainty; it does not include localization"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`**  
   Records locked uncertainty metrics including frame jitter (<2 ms), static RMS (0.02–0.03 px), and operator substitution sensitivity.  
   *Quote:* "RMS 0.02-0.03px raw; drift <=0.011 px/1000fr raw"

---

## 9. Definitions of bending, torsion, heave, pitch (list every distinct definition and its file)

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/SPATIAL_OPERATOR_SYNTHESIS_2026-08-02.md`**  
   Tabulates explicit mathematical formulas for camera bending `b_cam = (yA + yB)/2` where `yA = (y1 + y2)/2` and `yB = y3`, camera torsion proxy `t_cam = yB - yA`, laser bending `b_LDS = (c + s)/2`, and laser torsion proxy `t_LDS = (s - c) * dp` with `dp = 2.0`.  
   *Quote:* "b_cam=(yA+yB)/2 = (((y1+y2)/2)+y3)/2 ... t_cam=yB-yA = y3-(y1+y2)/2"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Defines pixel-domain bending as the equal-weight cross-marker mean of Marker A and Marker B, and torsion_proxy as Marker B minus Marker A, requiring all three cameras to be simultaneously admissible.  
   *Quote:* "cross-marker mean (bending ... ) and a torsion-sensitive differential proxy (torsion_proxy ... )"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md`**  
   Defines millimetre-domain bending as `(center + side)/2` and torsion proxy as `(side - center) * 2.0` with `dp = db/dside = 200/100 = 2.0`.  
   *Quote:* "Bending is defined as (center + side)/2 and torsion proxy as (side - center)"

4. **`02_research_projects/P00_shm-displacement-project/context_data/TESolution/Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m`**  
   Implements vendor laser processing formulas: mean of channels 1 and 2 for bending (`disp_mean = (data(:,1) + data(:,2))/2`), and differential scaled by dp for torsion (`disp_diff = (data(:,2) - data(:,1)) * dp`).  
   *Quote:* "disp_mean = (data(:,1) + data(:,2))/2; % bending"

5. **`04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md`**  
   Documents Tunnel B alternative torsion definition dividing by 2: `(side - center)/2 * pvolt * dp` with `dp = 1.538`.  
   *Quote:* "Torsion formula | (side − center)/2 × pvolt × dp"

6. **`98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin/docs/OMRPR_SUPERVISOR_GUIDELINE.md`**  
   Refers to heave (`f_h`) and pitch/torsional (`f_α`) natural vibration frequencies and damping ratios.  
   *Quote:* "f_h/f_α/damping values are UNVERIFIED pending a provenance check"

---

## 10. Background or camera-motion compensation

1. **`02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis/src/omrpr_analysis/background_compensation.py`**  
   Implements stationary-background camera-motion compensation using OpenCV ECC image alignment (affine motion, 20 px dilated marker mask) to compute compensated centroids.  
   *Quote:* "camera motion is estimated directly from each frame's static background via ECC"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_01_STATIC_PRECISION_2026-08-13.md`**  
   Finds that ECC compensation improves cam2 RMS but causes severe monotonic drift on cam3 (0.328/0.349 px compensated vs 0.027/0.047 px raw), demonstrating compensation is not universally beneficial.  
   *Quote:* "cam3 shows a real regression ... roughly 7-12x worse on both axes"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_03_ADMISSIBILITY_MANIFEST_2026-08-13.md`**  
   Establishes a 5x static compensation-regression check and assigns per-camera defaults: cam1 raw, cam2 compensated, cam3 raw fallback.  
   *Quote:* "cam1 = raw, cam2 = compensated, cam3 = raw fallback"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Details the selection of raw versus compensated tracks per camera stream based on zero-motion baseline drift.  
   *Quote:* "primary pixel-domain measure (raw or compensated) is selected individually per camera"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_1_AXIS_OPERATOR_SENSITIVITY_2026-08-14.md`**  
   Evaluates how the cam1=raw versus cam2=compensated split drives a large q1/q2 RMS divergence (1.26x to 55.5x).  
   *Quote:* "dominated by the cam1=raw vs. cam2= compensated processing-branch split"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`**  
   Reports that between-camera divergence is attributable in part to the processing branch difference rather than raw camera noise.  
   *Quote:* "cam1's frozen default track is raw and cam2's is ECC-motion-compensated"

---

## 11. The 320 RPM dropout

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md`**  
   Identifies the root cause of the 320 RPM dropout as AprilTag quad-finding segmentation failure caused by high frame-to-frame velocity eroding the outer quiet-zone component.  
   *Quote:* "the quad-finding stage fails outright, not the decode stage"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_03_ADMISSIBILITY_MANIFEST_2026-08-13.md`**  
   Formally rejects 320 RPM cam1 and cam2 streams under governance override, Wilson gate failure, and velocity exceedance, retaining cam3 as diagnostic-only.  
   *Quote:* "320RPM remains cam3-only diagnostic ... composite_use_permitted is false"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`**  
   Records 320 RPM detection completeness as 60.80% (cam1), 61.35% (cam2), and 100.00% (cam3) with Wilson lower bounds.  
   *Quote:* "cam1: 60.80% ... cam2: 61.35% ... cam3: 100.00%"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Restricts the 320 RPM condition from composite estimation, retaining only cam3 single-view output labeled as diagnostic quantity d_320,B(t).  
   *Quote:* "retaining cam3 output as diagnostic-only, never composite-eligible"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13_figure.py`**  
   Renders Figure 2 displaying AprilTag detector debug output showing connected-component segmentation collapse on failed 320 RPM frames.  
   *Quote:* "composites six already-generated PNG files into one labeled gallery"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`**  
   Explains that 320 RPM image-plane velocity jumps ~13x above the 240–300 RPM plateau, triggering the quad segmentation failure mechanism.  
   *Quote:* "jumping ~13x at 320 RPM relative to the 240-300 RPM plateau"

---

## 12. The ~9 Hz line: hypotheses and test results

*Note on ground truth:* No scanned file identifies the ~9 Hz line as an "electrical/mechanical facility artifact." That attribution in older documents was unsupported. The primary evidence proposing hypotheses or reporting test results is:

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S05_01_STATIC_PRECISION_2026-08-13.md`**  
   Observes a resolvable y-axis peak at 9.1–9.6 Hz on cam1 and cam2 on the static segment (28–68x noise floor, amplitude ~0.01–0.02 px), stating as a hypothesis: "Cause not investigated (candidate: rig/building vibration or camera-mount resonance); flagged for completeness, not claimed."  
   *Quote:* "Cause not investigated (candidate: rig/building vibration or camera-mount resonance)"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S10_04_TWO_PERSONA_INTERNAL_REVIEW_2026-08-27.md`**  
   Proposes as a technical hypothesis that the reported 9.37 Hz peak is the 10th raw bin center of the Welch estimator grid (df ≈ fps/64 ≈ 0.94 Hz).  
   *Quote:* "clustered dominant FDD frequencies ... are, by construction, near-exact integer multiples of the Welch grid"

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_3_MODAL_CONSENSUS_2026-08-13.md`**  
   Records FDD test results showing the dominant peak at e0_0rpm is 9.370 Hz (coarse-in-phase, bootstrap stability 0.998) and at e1_20rpm is 9.373 Hz (coarse-mixed-phase, bootstrap stability 0.774).  
   *Quote:* "e0_0rpm | no | 9.370 | 9.370–9.370 | 0.998 | coarse-in-phase"

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md`**  
   Reports static fused series Welch PSD test results showing a bending dominant non-DC peak at 9.3695 Hz and a torsion dominant non-DC peak at 9.1352 Hz.  
   *Quote:* "bending PSD dominant non-DC peak at 9.3695 Hz"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_time_series_spectra_2026-08-13_results/response_amplitude_summary.csv`**  
   Documents test results where dominant nonzero frequency for e0_0rpm across qA, qB, bending, and torsion proxy is 9.370 Hz.  
   *Quote:* "dominant_nonzero_frequency_hz ... 9.369678772031438"

6. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md`**  
   Finds in test results that at low motion (dn=3, 30 RPM), the third camera naive peak of 1.40 Hz shifts to 8.74 Hz after timestamp resampling.  
   *Quote:* "lowest-motion condition (dn=3, 30 RPM: naive 1.40 Hz vs. fixed 8.74 Hz)"

---

## 13. Marker identity and layout: which camera sees which marker; tag sizes (20 mm vs 35 mm); marker separation values and any retraction

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/07_PROJECT_MEMORY/Decision_Log.md`**  
   Documents that in 2025 cam1/cam2 see center marker ID-0-1 and cam3 sees off-center marker ID-0-2 (20 mm tags), while in 2024 two symmetric markers were used (35 mm tags), retracting the 135.14 mm separation as invalid for 2025.  
   *Quote:* "the 2024 campaign's physical AprilTag markers are 35mm, not 20mm"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`**  
   Records in Section J the formal retraction of the 135.14 mm camera marker separation and 133.84–136.46 mm range as RETRACTED / INVALID_FOR_2025.  
   *Quote:* "135.14 mm (calculation 135.137294) ... RETRACTED / INVALID_FOR_2025"

3. **`00_inbox/Paper2_Review_2026-09-06/12_TAG_ID_RECONCILIATION_REPORT.md`**  
   Reconciles camera-to-marker mapping, establishing Marker A (center, cam1/cam2) and Marker B (side, cam3) both decode as AprilTag ID 0, and that camera stream identity is the sole physical marker discriminator.  
   *Quote:* "Both physical markers decode as AprilTag ID 0."

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`**  
   Defines the two-marker physical layout where Marker A is redundantly viewed by cam1 and cam2, and Marker B is viewed by cam3 alone.  
   *Quote:* "Marker A, observed redundantly by cam1 and cam2, and Marker B, observed by cam3 alone"

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/TASK2_DATASET_METADATA_AUDIT_2026-09-02.md`**  
   Audits the tag configuration confirming 20 mm nominal tag size (tag_size_m: 0.020) and two physically separate tags sharing the same AprilTag ID.  
   *Quote:* "Two physically separate printed tags share this same ID"

6. **`00_inbox/Paper2_Review_2026-09-06/14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md`**  
   Reconciles campaign geometries, confirming 2024 (symmetric 35 mm tags) and 2025 (center + off-center 20 mm tags) are different spatial measurement operators and invalidating the 135.14 mm separation.  
   *Quote:* "marker_geometry_same_between_campaigns     = NO"

---

## 14. Scripts that produce manuscript figures or tables (path, what it plots, input file)

1. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FIG1_PIPELINE_SCHEMATIC_2026-08-26_figure.py`**  
   *Plots:* Figure 1 pipeline schematic diagram illustrating the two parallel non-concurrent analytical lanes (camera and LDS), admissibility gates, spatial operators, and uncertainty budget.  
   *Input file:* Hardcoded schematic layout / pipeline structure (no data input file).  
   *Quote:* "Render Fig 1 (manuscript pipeline schematic)"

2. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13_figure.py`**  
   *Plots:* Figure 2 quad-segmentation failure gallery showing paired detected versus failed internal debug images for cam1 and cam2 at 320 RPM.  
   *Input files:* Six debug PNG files in `evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13_images/`.  
   *Quote:* "Render Fig 2 (manuscript) from the accepted quad-segmentation-failure debug images."

3. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_2_time_series_spectra_2026-08-13_figure.py`**  
   *Plots:* Figure 3 time-series displacement segments, Welch power spectral densities (PSD), and response amplitude summaries with 95% intervals across conditions.  
   *Input file:* `evidence/S06_2_time_series_spectra_2026-08-13_results/response_amplitude_summary.csv`.  
   *Quote:* "Render Fig 3 (manuscript) from the S06.02 spectral checkpoint results."

4. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01_figure.py`**  
   *Plots:* Figure 4 third-camera inter-frame interval jitter for 70 RPM and naive-nominal-rate versus timestamp-resampled Welch PSD with facility natural frequency marked.  
   *Input file:* `RAW_Data/3D_video_system/2D_WTT/D10.csv`.  
   *Quote:* "Render Fig 4 (manuscript) from the S12.1 timing-correction checkpoint."

5. **`02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/final_candidates/synthesis_v2/supplement/data/build_table_s1.py`**  
   *Plots/Builds:* Publication Table S1 by joining frozen reference-blind peaks (`S1A`), post-hoc comparison (`S1B`), and per-camera sweep (`Table S2`).  
   *Input files:* `S1A_reference_blind_peaks_frozen.csv`, `S1B_posthoc_reference_comparison.csv`, `Table_S2_per_camera_frequency_sweep.csv`.  
   *Quote:* "Build publication Table S1 by joining frozen tables; no spectra are computed."

6. **`00_inbox/Paper2_Review_2026-09-06/20_full_frequency_sweep.py`**  
   *Plots/Builds:* Full multi-camera Welch PSD and dominant spectral peaks across all 21 wind-tunnel conditions, producing `21_FULL_PER_CAMERA_FREQUENCY_SWEEP.csv`.  
   *Input files:* Multi-camera displacement time series across all 21 test conditions.  
   *Quote:* "DESCRIPTIVE_MATCH_RAYLEIGH_BINS = 1.0"
