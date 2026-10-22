# ATTEMPTS_AND_DEAD_ENDS: Retracted, Abandoned, and Remedied Items

This document catalogues every dead end, superseded assumption, erroneous parameter, and retracted calculation identified during the Paper 2 research lineage. For each item, the original assumption, the reason for abandonment, the correcting file, and a verbatim quote (<= 15 words) are recorded.

---

## 1. Retraction of Photogrammetric Marker Separation (135.14 mm)

- **Initial Attempt / Erroneous Parameter:**  
  A camera-marker separation of 135.14 mm (calculated as 135.137294 mm) was derived photogrammetrically from a single calibration photograph in `evidence/MARKER_SEPARATION_PHOTOGRAMMETRY_2026-08-02.md`.
- **Why Abandoned / Retracted:**  
  The derivation was found to be unverified for the physical 2025 wind-tunnel setup. The true marker separation was never directly surveyed with calipers or a coordinate measuring machine. The ledger formally retracted this number on 2026-09-07.
- **Evidence / Source:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`  
  *Quote:* "135.14 mm (calculation 135.137294) ... RETRACTED / INVALID_FOR_2025"
- **Supervisor Estimate Contradiction:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/MARKER_SEPARATION_PHOTOGRAMMETRY_2026-08-02.md`  
  *Quote:* "supervisor reported a ~200 mm marker separation"
- **Current Scientific Status:**  
  The 2025 camera marker separation remains an unsurveyed physical quantity; qualitative proxy operators are used instead of unverified absolute metric torsion.

---

## 2. Coarse FFT Grid Resolution Artifact (~0.938 Hz Peak)

- **Initial Attempt / Erroneous Finding:**  
  Early spectral analyses using standard Welch PSD with `nperseg=64` (frequency bin width df ≈ 0.9375 Hz) reported dominant bending response peaks at 0.937–0.938 Hz for 60, 70, and 80 RPM.
- **Why Abandoned / Superseded:**  
  Fine-resolution LDS reanalysis (`nperseg=4096`, df ≈ 0.088 Hz) and third-camera native-timestamp FDD (df ≈ 0.067 Hz) demonstrated that the 0.938 Hz peak was entirely a grid-binning artifact. No physical modal peak exists at 0.938 Hz; the physical bending natural frequency of the bridge deck specimen is 1.4303 Hz.
- **Evidence / Source:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S06_3_MODAL_CONSENSUS_2026-08-13.md`  
  *Quote:* "These are FFT-bin estimates, not fine frequency measurements."  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md`  
  *Quote:* "reported location of 0.937–0.938 Hz is a bin center forced by the sampling grid"  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S11_1_LDV_NPERSEG4096_RESONANCE_CHECK_2026-08-30.md`  
  *Quote:* "instead found the dominant 0-3 Hz response at 1.406-1.494 Hz in every case"
- **Current Scientific Status:**  
  Spectra are reported at native resolution with the 1.4303 Hz facility modal benchmark clearly distinguished from grid-quantization bins.

---

## 3. Physical AprilTag Marker Size Confusion (80 mm vs 20 mm vs 35 mm)

- **Initial Attempt / Erroneous Draft Parameter:**  
  Early manuscript drafts (Section 2.2) erroneously described the AprilTag fiducial targets as 80 mm, an error inadvertently carried over from Paper 1 (which used 80 mm tags on a shear frame).
- **Why Abandoned / Corrected:**  
  Physical tag verification confirmed that the 2025 wind-tunnel campaign used 20 mm tags (AprilTag 36h11), whereas the 2024 campaign used 35 mm tags.
- **Evidence / Source:**  
  `04_code_software/github/shm-displacement-project/paper2/INVESTIGATION_REPORT_2026_06_10.md`  
  *Quote:* "Error in manuscript draft: Section 2.2 stated 'physical size: 80 mm'"  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/07_PROJECT_MEMORY/Decision_Log.md`  
  *Quote:* "the 2025 campaign's 20mm tag size"
- **Current Scientific Status:**  
  All 2025 pipeline configurations and manuscript texts are fixed to 20 mm (0.020 m).

---

## 4. Off-by-One Condition Alignment and Spurious Correlations (Legacy B0 Package)

- **Initial Attempt / Erroneous Alignment:**  
  The legacy B0 comparison scripts matched camera condition labels `e0` through `e20` to laser records `D1` through `D21`, resulting in an off-by-one condition index mismatch. Because both structural displacement and wind speed monotonically increase with fan RPM, the misaligned series produced spuriously high Pearson correlations (r ~ 0.959 for bending, r ~ 0.968 for torsion).
- **Why Abandoned / Remediated:**  
  Condition-by-condition audit proved that `D0` corresponded to 0 RPM static (10 s duration) and subsequent files corresponded to specific RPM setpoints. An off-by-one mapping corrupts the physical pairing.
- **Evidence / Source:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/REMEDIATION_LOG_2026-08-02.md`  
  *Quote:* "Off-by-one Step 10 D-file mapping, remediated_rebuilt"  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`  
  *Quote:* "19 exactly matched RPM labels"
- **Current Scientific Status:**  
  Strict integer-RPM matching yields 19 valid comparison conditions (excluding e0_0rpm and e20_320rpm), with true physical correlations of Spearman rho = 0.691 (bending) and 0.774 (torsion proxy).

---

## 5. Laser Spacing Geometry and Calibration Factor Discrepancies (Tunnel A vs Tunnel B)

- **Initial Attempt / Erroneous Parameters:**  
  Earlier codebase versions mixed parameters between two different wind tunnels: Tunnel B (dside = 130 mm, dp = 1.538) and Tunnel A (dside = 100 mm, db = 200 mm, dp = 2.0). Furthermore, raw laser voltages were intermittently confused between cm and mm units.
- **Why Abandoned / Resolved:**  
  Vendor acquisition script `BRID2D1_choi.m` and project constitutional documents verified the physical setup for Tunnel A.
- **Evidence / Source:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/01_PROJECT_FOUNDATION/01_Project_Constitution.md`  
  *Quote:* "dside = 100 mm, db = 200 mm, and dp = db/dside = 2.0"  
  `02_research_projects/P00_shm-displacement-project/context_data/TESolution/Video Measurement/RAW_Data/3D_video_system/2D_WTT/BRID2D1_choi.m`  
  *Quote:* "dside = 10; ... db = 20; ... dp = db/dside;"
- **Current Scientific Status:**  
  Tunnel A geometry is standardized across all analysis scripts.

---

## 6. Naive Nominal Frame Rate Assumption (60.0 fps) vs Inter-Frame Jitter

- **Initial Attempt / Erroneous Assumption:**  
  Initial frequency estimation assumed uniform sampling at exactly 60.0 Hz across all cameras and conditions.
- **Why Abandoned / Remediated:**  
  Timestamp analysis revealed that inter-frame intervals exhibited jitter and dropped significantly to 30–50 Hz at high RPM setpoints (>200 RPM) due to processing backpressure. Naive nominal Welch PSD produced distorted peak estimates under high jitter.
- **Evidence / Source:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S12_1_TESOLUTION_CAMERA_TIMING_FDD_2026-09-01.md`  
  *Quote:* "the timestamp fix changes the answer exactly where jitter is worst"  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md`  
  *Quote:* "Camera timestamps run at ~60 fps nominal"
- **Current Scientific Status:**  
  Analyses require timestamp-aware resampling or native non-uniform Lomb-Scargle spectral analysis.

---

## 7. The 320 RPM High-Speed Tracking Failure

- **Initial Attempt / Abandoned Data:**  
  Condition e20 (320 RPM) was initially intended as the peak wind-speed comparison point.
- **Why Abandoned / Excluded:**  
  Severe quad-segmentation dropouts occurred on cam1 (39.2% failure) and cam2 (38.7% failure) due to motion blur and corner threshold failures at high bridge-deck velocities.
- **Evidence / Source:**  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md`  
  *Quote:* "cam1 | 1829 | 717 | 39.2%"  
  `02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/02_methods.md`  
  *Quote:* "and the 320-RPM condition ... are excluded"
- **Current Scientific Status:**  
  320 RPM is documented as a boundary limitation of the optical tracking system and excluded from steady-state statistical comparison.
---
---

## 8. Hardcoded "Expected Tag ID 1" Bug on Camera 3

- **Initial Attempt / Erroneous Implementation:**  
  Early detector post-processing scripts (`fresh_quality_scores/per_frame_detections.csv`) hardcoded `expected_tag_id = 1` for camera 3 under the assumption that Marker B carried encoded AprilTag ID 1.
- **Why Abandoned / Remediated:**  
  Both physical markers in the wind tunnel carry encoded AprilTag ID 0 (with human-readable handwritten labels "ID 0" and "ID 1"). The mismatch caused all 38,448 frames for cam3 to be silently marked as undetected until discovered on 2026-08-12.
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/12_TAG_ID_RECONCILIATION_REPORT.md`  
  *Quote:* "both physical WTT markers carry AprilTag ID 0"  
  *Quote:* "silently marking all 38,448 cam3 frames as `detected=False`"
- **Current Scientific Status:**  
  Detector expectations for all three cameras are locked to ID 0 (`EXPECTED_TAG = {"cam1": 0, "cam2": 0, "cam3": 0}`). Camera identity (cam1/cam2 vs cam3) distinguishes the physical locations.

---

## 9. Campaign Measurement Operator Inequivalence (2024 vs 2025)

- **Initial Attempt / Erroneous Assumption:**  
  Preliminary drafts assumed that torsional observables from the 2024 laser campaign and the 2025 camera campaign were directly equivalent spatial operators.
- **Why Abandoned / Clarified:**  
  While the mechanical structural system was identical between campaigns (`MECHANICAL_SYSTEM_EQUIVALENCE = TRUE`), the marker geometries differed: 2024 used symmetric 35 mm tags, whereas 2025 used center + off-center 20 mm tags. Consequently, the derived spatial observables are physically distinct operators (`MEASUREMENT_OPERATOR_EQUIVALENCE = FALSE`).
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md`  
  *Quote:* "mechanical_system_same_between_campaigns   = YES"  
  *Quote:* "measurement_operator_same_between_campaigns = NO"
- **Current Scientific Status:**  
  2024 symmetric torsional displacement and 2025 center-plus-side differential displacement are treated as distinct operators and never equated without explicit geometric transformation.

---

## 10. Superseded Pre-Pass-3 Claims in Submission Packages (Defect C-01)

- **Initial Attempt / Retracted Claims:**  
  Early submission packages asserted claims that were later retracted during manuscript audit: "for Vortex-Induced Vibration Characterization", "explicit five-gate admissibility manifest", "KLT-based diagnostic branch", and "condition-level join against a non-concurrent 2024 laser-vibrometer campaign".
- **Why Abandoned / Remediated:**  
  Adversarial audit `52_FINAL_MANUSCRIPT_AUDIT_REPORT.md` flagged these claims as Critical Defect C-01 because the final manuscript focuses strictly on reference-blind spectral identification and same-marker cross-view agreement.
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/53_FINAL_MANUSCRIPT_DEFECT_LEDGER.csv`  
  *Quote:* "carry the superseded pre-Pass-3 lineage and assert claims the current manuscript retracts"
- **Current Scientific Status:**  
  Submission package documents (cover letter, highlights, novelty statement) are aligned to the synthesized manuscript in `synthesis_v2/` with no mention of VIV, condition joins, or KLT branches.

---

## 11. Undisclosed Running Window Settings (Defect M-03)

- **Initial Attempt / Undisclosed Parameters:**  
  Early drafts presented short-time windowed frequency tracking (Figure 3 and Section 5.5) without disclosing window length, hop size, or window counts.
- **Why Abandoned / Remediated:**  
  Flagged as Major Defect M-03; reproducibility required full specification of the windowing parameters.
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/53_FINAL_MANUSCRIPT_DEFECT_LEDGER.csv`  
  *Quote:* "10 s windows, 5 s hop, 5 windows per ~30.5 s record"
- **Current Scientific Status:**  
  Methods explicitly document: 10 s window length, 5 s hop, 5 windows per ~30.5 s record, with a secondary 15 s / 7.5 s setting reported in Supplement S4 (`28_WINDOWED_FREQUENCY_EVOLUTION.csv`).
