# Tree 11 Summary: Paper 2 Acquisition Methods Research (Acquisition timing, jitter analysis, and sampling evaluation reports)

## Overview and Scope
Tree 11 contains 42 total scanned files (41 catalogued, 1 identical duplicates).
Paper 2 Acquisition Methods Research (Acquisition timing, jitter analysis, and sampling evaluation reports).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `references/tesol_ws_6349a2d_compare_displacements.py`
- `scripts/desktop_package/g3_redo.py`
- `scripts/desktop_package/g3_static_luminance.py`
- `scripts/desktop_package/g4_g3_wtt.py`
- `scripts/desktop_package/run_all.sh`
- `scripts/desktop_package/stationary_check.py`
- `scripts/g2_analyze.py`
- `scripts/g2_extract.py`

## Key Results and Stated Findings
- **`00_START_HERE/MASTER_PROGRESS_REPORT.md`**: "It is far too small to matter for 9 Hz (amplitude effect <0.1%)"
- **`00_START_HERE/MASTER_PROGRESS_REPORT.md`**: "4. **Two audit statements need caution:** (a) "the 9.28 Hz peak indicates camera mount self-vibration" (MINIMAL_PROTOTYPE_GO_NO_GO"
- **`references/Vision_SHM_Literature_Critical_Audit_2026-10-12.md`**: "4. **Mains aliasing:** A 50-Hz intensity modulation sampled at 60 Hz aliases to 10 Hz"
- **`references/Vision_SHM_Literature_Critical_Audit_2026-10-12.md`**: "100 Hz to 20 Hz"
- **`references/tesol_ws_6349a2d_compare_displacements.py`**: "std(reference) > 0 and np"
- **`references/tesol_ws_6349a2d_compare_displacements.py`**: "std(test) > 0:"
- **`reports/current/HISTORICAL_RESAMPLING_RECONCILIATION.md`**: "resample` to 60 Hz"
- **`reports/current/HISTORICAL_RESAMPLING_RECONCILIATION.md`**: "interp` to a 1 ms grid, then `scipy"

## Planned or Missing Elements
- `00_START_HERE/MASTER_PROGRESS_REPORT.md`: from 2025-09-23 lists NV12 and YUYV at 1920×1080, 59
- `00_START_HERE/MASTER_PROGRESS_REPORT.md`: (`measurement_timing_limitations
- `00_START_HERE/MASTER_PROGRESS_REPORT.md`: A3 that record time was set from header time conflicts with the campaign bags (a
- `references/Vision_SHM_Literature_Critical_Audit_2026-10-12.md`: ### Q1
- `reports/current/HISTORICAL_RESAMPLING_RECONCILIATION.md`: for the researcher

## Duplicate Files Across Trees
- `scratch/compare_displacements_6349a2d.py`: identical to Tree 11 (`references/tesol_ws_6349a2d_compare_displacements.py`)
