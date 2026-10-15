# Tree 6 Summary: SHM Displacement Project - GitHub (Offline processing, frequency recovery, and LDV comparison pipelines)

## Overview and Scope
Tree 6 contains 202 total scanned files (194 catalogued, 8 identical duplicates).
SHM Displacement Project - GitHub (Offline processing, frequency recovery, and LDV comparison pipelines).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `offline_processing/__init__.py`
- `offline_processing/notebooks/demo_pipeline.ipynb`
- `offline_processing/scripts/__init__.py`
- `offline_processing/scripts/compare_ldv.py`
- `offline_processing/scripts/compute_metrics.py`
- `offline_processing/scripts/detect_apriltag.py`
- `offline_processing/scripts/export_from_rosbag.py`
- `offline_processing/scripts/fractional_delay.py`

## Key Results and Stated Findings
- **`docs/ANALYSIS_REPORT_TESOLUTION.md`**: "│       ├── D00–D20                                  ← Raw LDV (21 conditions, 7200 rows each = 20s)"
- **`docs/ANALYSIS_REPORT_TESOLUTION.md`**: "│   ├── D0–D38                               ← Raw LDV (39 conditions, 10800 rows=30s)"
- **`docs/INVESTIGATION_REPORT_2026_06_10.md`**: "Which tunnel — LDV reference? | **Tunnel B geometry** (dside=13cm) | Setup doc 센서간격=13cm, Pearson 0.936 vs 0.721"
- **`docs/INVESTIGATION_REPORT_2026_06_10.md`**: "Chord width? | **0.40 m** | Setup doc 교폭=0.4m"
- **`docs/OMRPR_SUPERVISOR_PROMPT.md`**: "RMSE displacement        | 0.14–0.40 mm (best cases)"
- **`docs/OMRPR_SUPERVISOR_PROMPT.md`**: "RMSE repeatability       | 0.096–0.261 mm (mean 0.181 ± 0.086 mm)"
- **`docs/OMRPR_SUPERVISOR_PROMPT_backup.md`**: "RMSE displacement | 0.14–0.40 mm (best cases)"
- **`docs/OMRPR_SUPERVISOR_PROMPT_backup.md`**: "RMSE repeatability | 0.096–0.261 mm (mean 0.181 ± 0.086 mm)"

## Planned or Missing Elements
- `docs/ANALYSIS_REPORT_TESOLUTION.md`: that the two LDV references come from different tunnels
- `docs/ANALYSIS_REPORT_TESOLUTION.md`: Natural frequencies differ between 2016 paper (1
- `docs/ANALYSIS_REPORT_TESOLUTION.md`: as extrapolated
- `docs/INVESTIGATION_REPORT_2026_06_10.md`: | Answer | Evidence |
- `docs/INVESTIGATION_REPORT_2026_06_10.md`: ** Torsion formulas differ
- `docs/INVESTIGATION_REPORT_2026_06_10.md`: ** Camera free-vibration characterization was at **48

## Duplicate Files Across Trees
- `docs/paper2_tesolution_style_torsion_plan_ubun20_Jun-11-121823-2026_Conflict.md`: identical to Tree 6 (`docs/paper2_tesolution_style_torsion_plan.md`)
- `docs/paper2_tesolution_style_torsion_plan_ubun24_Jun-11-144902-2026_Conflict.md`: identical to Tree 6 (`docs/paper2_tesolution_style_torsion_plan.md`)
- `memory/claim_boundary_ubun20_Jun-11-121824-2026_Conflict.md`: identical to Tree 6 (`memory/claim_boundary.md`)
- `memory/claim_boundary_ubun24_Jun-11-144904-2026_Conflict.md`: identical to Tree 6 (`memory/claim_boundary.md`)
- `memory/experimental_results_ubun24_Jun-11-144906-2026_Conflict.md`: identical to Tree 6 (`memory/experimental_results.md`)
- `paper2/manuscript/PAPER2_CRITICAL_REVIEW.md`: identical to Tree 5 (`docs/legacy_drafts/PAPER2_CRITICAL_REVIEW.md`)
- `scripts/static_tests/bagfiles/run_all_steps.py`: identical to Tree 6 (`scripts/static_tests/bagfiles/cam2_working scripts/run_all_steps.py`)
- `.pytest_cache/README.md`: identical to Tree 2 (`.pytest_cache/README.md`)
