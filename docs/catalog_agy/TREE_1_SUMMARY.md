# Tree 1 Summary: Structural Vision Research (Sensors-line evidence repository; S04..S12 reports, scripts, number ledgers)

## Overview and Scope
Tree 1 contains 468 total scanned files (264 catalogued, 204 identical duplicates).
Structural Vision Research (Sensors-line evidence repository; S04..S12 reports, scripts, number ledgers).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `evidence/FIG1_PIPELINE_SCHEMATIC_2026-08-26_figure.py`
- `evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13_figure.py`
- `evidence/S05_01_static_precision_2026-08-13.py`
- `evidence/S05_02_threshold_sensitivity_2026-08-13.py`
- `evidence/S06_2_time_series_spectra_2026-08-13.py`
- `evidence/S06_2_time_series_spectra_2026-08-13_figure.py`
- `evidence/S06_3_modal_consensus_2026-08-13.py`
- `evidence/S06_3_modal_consensus_2026-08-13_figure.py`

## Key Results and Stated Findings
- **`01_PROJECT_FOUNDATION/01_Project_Constitution.md`**: "3. For this campaign, dside=100 mm, db=200 mm, and dp=2.0."
- **`01_PROJECT_FOUNDATION/01_Project_Constitution.md`**: "raw-data precision as approximately 1.43 Hz and 3.11 Hz"
- **`02_KNOWLEDGE_BASE/literature/Hybrid Vision Vibration Monitoring Survey.md`**: "Consequently, fiducial tracking is inherently and fundamentally drift-free6."
- **`02_KNOWLEDGE_BASE/literature/Hybrid Vision Vibration Monitoring Survey.md`**: "> 1. Performance of Optical Structural Vibration Monitoring Systems in Experimental Modal Analysis \- ResearchGate, [https://www"
- **`02_KNOWLEDGE_BASE/literature/KLT_recovery_architecture_options_2026-08-26.md`**: "simulation RMSE 24.32 px fused vs"
- **`02_KNOWLEDGE_BASE/literature/KLT_recovery_architecture_options_2026-08-26.md`**: "Tested on a 167 m pedestrian bridge without"
- **`02_KNOWLEDGE_BASE/literature/SHM Sensor Validation Methodologies.md`**: ", 200–1000 Hz) and measure absolute inertial motion"
- **`02_KNOWLEDGE_BASE/literature/SHM Sensor Validation Methodologies.md`**: "Under optimal conditions with high-contrast speckle patterns, this noise floor can reach ![][image45] to ![][image46] pixels10."

## Planned or Missing Elements
- `02_KNOWLEDGE_BASE/literature/Hybrid Vision Vibration Monitoring Survey.md`: spatial smoothness
- `02_KNOWLEDGE_BASE/literature/Hybrid Vision Vibration Monitoring Survey.md`: of KLT is brightness constancy
- `02_KNOWLEDGE_BASE/literature/KLT_recovery_architecture_options_2026-08-26.md`: the current
- `02_KNOWLEDGE_BASE/literature/KLT_recovery_architecture_options_2026-08-26.md`: an initial
- `02_KNOWLEDGE_BASE/literature/KLT_recovery_architecture_options_2026-08-26.md`: above)

## Duplicate Files Across Trees
- `manuscript/final_candidates/synthesis/submission_package/Cover_Letter_MDPI_Sensors.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Cover_Letter_MDPI_Sensors.md`)
- `manuscript/final_candidates/synthesis/submission_package/Highlights.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Highlights.md`)
- `manuscript/final_candidates/synthesis/submission_package/Novelty_Contribution_Statement.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Novelty_Contribution_Statement.md`)
- `manuscript/final_candidates/synthesis/submission_package/Short_Cover_Summary.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Short_Cover_Summary.md`)
- `manuscript/final_candidates/synthesis/supplement/README_SUPPLEMENT_STATUS.md`: identical to Tree 1 (`manuscript/final_candidates/opus/supplement/README_SUPPLEMENT_STATUS.md`)
- `manuscript/final_candidates/synthesis/supplement/data/20_FULL_FREQUENCY_SWEEP_RUN_METADATA.json`: identical to Tree 1 (`manuscript/final_candidates/opus/supplement/data/20_FULL_FREQUENCY_SWEEP_RUN_METADATA.json`)
- `manuscript/final_candidates/synthesis/supplement/data/20_full_frequency_sweep.py`: identical to Tree 1 (`manuscript/final_candidates/opus/supplement/data/20_full_frequency_sweep.py`)
- `manuscript/final_candidates/synthesis/supplement/data/20b_write_sweep_outputs.py`: identical to Tree 1 (`manuscript/final_candidates/opus/supplement/data/20b_write_sweep_outputs.py`)
