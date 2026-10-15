# Tree 2 Summary: OMRPR Analysis (Clean-room offline pose reconstruction package with modular signals, calibration, and validation)

## Overview and Scope
Tree 2 contains 187 total scanned files (178 catalogued, 9 identical duplicates).
OMRPR Analysis (Clean-room offline pose reconstruction package with modular signals, calibration, and validation).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `scripts/00_preflight.sh`
- `scripts/01_bootstrap_or_update.sh`
- `scripts/02_upgrade_dependencies.sh`
- `scripts/03_install_official_apriltag.sh`
- `scripts/04_data_placement_assistant.sh`
- `scripts/05_classify_existing_bags.py`
- `scripts/06_project_readiness.sh`
- `scripts/07_backup_project.sh`

## Key Results and Stated Findings
- **`ai-context/01_CURRENT_STATE.md`**: "320 RPM is excluded from stable summaries and retained"
- **`ai-context/01_CURRENT_STATE.md`**: "S05--S08 (static precision and admissibility, response/structural-modal"
- **`ai-context/03_ROADMAP.md`**: "G3 | Precision and admissibility | static noise/PSD, per-camera/per-condition quality, no averaging through failed streams | NOT STARTED"
- **`ai-context/03_ROADMAP.md`**: "G4 | KLT independent branch | AprilTag-anchored bounded KLT, hidden-frame/synthetic tests, return-anchor drift gates | QUARANTINED"
- **`ai-context/06_TASK_QUEUE.md`**: "G6 (response and modal analysis): superseded by S06, complete (10/10)"
- **`configs/observation-control.yaml`**: "First-pass static admissibility gates derived from the measured 0 RPM"
- **`configs/observation-control.yaml`**: "60 RPM onset midpoint"
- **`docs/MASTER_EXECUTION_ROADMAP.md`**: "04 | Static precision | Timing, detection, RMS, PSD, and axis-specific noise documented"
- **`docs/MASTER_EXECUTION_ROADMAP.md`**: "10 | Frequency and uncertainty | Correct model frequencies and uncertainty components used"

## Planned or Missing Elements
- `ai-context/06_TASK_QUEUE.md`: Superseded by S06
- `outputs/reports/step_11_review.md`: | `a7b35d6ba17237182fcdc8a23cbb351cce97fd9ebbd85b24419b237c5a7da491` |
- `outputs/reports/task3_per_camera_frequency_recovery.md`: entirely (see
- `outputs/reports/task3b_cross_camera_phase_coherence.md`: underlying the manuscript's differential
- `outputs/reports/task3b_cross_camera_phase_coherence.md`: is **not** well-supported as a simple, RPM-invariant

## Duplicate Files Across Trees
- `docs/decisions/LEGACY_ANALYSIS_REPORT.md`: identical to Tree 1 (`evidence/mining_reports/LEGACY_ANALYSIS_REPORT_shm_pipeline_audit.md`)
- `outputs/image-audit-runs/20260801_022229/RUN_STATUS.txt`: identical to Tree 2 (`outputs/audit-runs/20260801_022002/RUN_STATUS.txt`)
- `outputs/reports/step02b_laser_corrected_intrinsics_discrepancy.md`: identical to Tree 1 (`evidence/OMRPR_STEP02B_INTRINSICS_DISCREPANCY_BENCHMARK_2026-08-18.md`)
- `outputs/reports/step_04_static_precision.md`: identical to Tree 1 (`evidence/OMRPR_STEP04_STATIC_PRECISION_2026-08-18.md`)
- `outputs/reports/step_05_review.md`: identical to Tree 1 (`evidence/OMRPR_STEP05_DETECTION_COVERAGE_2026-08-18.md`)
- `outputs/reports/step_09_review.md`: identical to Tree 1 (`evidence/OMRPR_STEP09_CONDITION_BENCHMARK_2026-08-18.md`)
- `outputs/reports/step_10_review.md`: identical to Tree 1 (`evidence/OMRPR_STEP10_FREQUENCY_REVIEW_2026-08-18.md`)
- `outputs/tables/step04_static_admissibility_thresholds.md`: identical to Tree 2 (`manuscript/tables/step04_static_admissibility_thresholds.md`)
