# Tree 8 Summary: Wind Tunnel Bridge Deck (Experimental analysis scripts and wind tunnel documentation)

## Overview and Scope
Tree 8 contains 59 total scanned files (51 catalogued, 8 identical duplicates).
Wind Tunnel Bridge Deck (Experimental analysis scripts and wind tunnel documentation).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `experimental_analysis/scripts/analyze_experiments.py`
- `experimental_analysis/scripts/dynamic_test/PlanA/A1_run_all_sanity_checks.py`
- `experimental_analysis/scripts/dynamic_test/PlanA/A2_aggregate_sanity_reports.py`
- `experimental_analysis/scripts/dynamic_test/PlanA/A_sanity_check_bagfiles.py`
- `experimental_analysis/scripts/dynamic_test/PlanB/B1_run_all_detections.py`
- `experimental_analysis/scripts/dynamic_test/PlanB/B_detect_apriltag_validate.py`
- `experimental_analysis/scripts/dynamic_test/Recorder_WTT.py`
- `experimental_analysis/scripts/dynamic_test/STEP2_CHECT_WTTBAGS.py`

## Key Results and Stated Findings
- **`experimental_analysis/scripts/analyze_experiments.py`**: "axvline(TARGET_FPS, color="red", linestyle="--", label="Target 60 Hz")"
- **`experimental_analysis/scripts/analyze_experiments.py`**: "append(f"  FPS mean = {mean_fps:.4f}, std = {std_fps:.4f}\n")"
- **`experimental_analysis/scripts/dynamic_test/PlanA/A2_aggregate_sanity_reports.py`**: "Large jitter (>5 ms)"
- **`experimental_analysis/scripts/dynamic_test/PlanA/A_sanity_check_bagfiles.py`**: "TAG_SIZE_M = 0.02  # default 2cm"
- **`experimental_analysis/scripts/dynamic_test/STEP2_CHECT_WTTBAGS.py`**: "EXPECTED_DT = 1.0 / 60.0  # expected frame interval at 60 Hz"
- **`experimental_analysis/scripts/dynamic_test/STEP2_CHECT_WTTBAGS.py`**: "DROP_THRESH = 1.5 * EXPECTED_DT  # gap > 25 ms considered a drop"
- **`experimental_analysis/scripts/dynamic_test/debug_3_wtt.py`**: "UPSAMPLE_RESAMPLE = True      # Resample to 1kHz and back to 60Hz"
- **`experimental_analysis/scripts/dynamic_test/debug_3_wtt.py`**: "TARGET_FS = 60.0              # Target frequency after resampling"

## Planned or Missing Elements
- No explicit unresolved tasks or unverified assumptions flagged.

## Duplicate Files Across Trees
- `experimental_analysis/scripts/dynamic_test/multi_cam_extrinsics.yaml`: identical to Tree 6 (`scripts/dynamic_test/multi_cam_extrinsics.yaml`)
- `experimental_analysis/scripts/dynamic_test/rest/PlanB_detect_apriltag_validate.py`: identical to Tree 6 (`scripts/dynamic_test/rest/PlanB_detect_apriltag_validate.py`)
- `experimental_analysis/scripts/dynamic_test/rest/step3b_analytics.py`: identical to Tree 6 (`scripts/dynamic_test/rest/step3b_analytics.py`)
- `experimental_analysis/scripts/process_all.sh`: identical to Tree 6 (`scripts/process_all.sh`)
- `experimental_analysis/scripts/static_tests/bagfiles/cam2_working scripts/gen_.sh`: identical to Tree 6 (`scripts/static_tests/bagfiles/cam2_working scripts/gen_.sh`)
- `experimental_analysis/scripts/static_tests/bagfiles/gen_.sh`: identical to Tree 6 (`scripts/static_tests/bagfiles/gen_.sh`)
- `experimental_analysis/scripts/static_tests/bagfiles/run_all_steps.py`: identical to Tree 8 (`experimental_analysis/scripts/static_tests/bagfiles/cam2_working scripts/run_all_steps.py`)
- `experimental_analysis/scripts/tag_pixel_coverage.py`: identical to Tree 6 (`scripts/tag_pixel_coverage.py`)
