# Tree 4 Summary: OMRPR Fin (Historical analysis source, configuration, and documentation)

## Overview and Scope
Tree 4 contains 64 total scanned files (34 catalogued, 30 identical duplicates).
OMRPR Fin (Historical analysis source, configuration, and documentation).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `src/utils/__init__.py`
- `src/utils/bag_io.py`
- `src/utils/transforms.py`
- `tests/__init__.py`
- `tests/test_transforms.py`

## Key Results and Stated Findings
- **`config/pipeline_config.yaml`**: "measurement_noise_std: 0.05  # mm — amplitude ratio >= 0.957 across all conditions"
- **`docs/DEEP_METHODS_REVIEW.md`**: "2. Four-component uncertainty chain including derived (not directly measured) noise floor with explicit independence assumption"
- **`docs/DEEP_METHODS_REVIEW.md`**: "~~Critical bug — intrinsics discrepancy~~ — RESOLVED (2026-06-20):"
- **`docs/OMRPR_SUPERVISOR_GUIDELINE.md`**: "NOTE:** f_h/f_α/damping values are UNVERIFIED pending a provenance check (Tunnel B Sept 2025 vs"
- **`docs/OMRPR_SUPERVISOR_GUIDELINE.md`**: "dside=130mm) and comparison numbers (r=0.845 etc"
- **`docs/PROJECT_CONTEXT.md`**: "2026-07-06 RESOLVED:** f_h/f_α/damping values below were UNVERIFIED pending a provenance check"
- **`docs/PROJECT_CONTEXT.md`**: "free-vibration measurement (f_h=1.4299 Hz/f_α=3.1098 Hz, within 0.2%/0.9%) and the already-documented"
- **`docs/RESULTS_LOG.md`**: "Discrepancy Cleanup — 2026-06-22"
- **`docs/RESULTS_LOG.md`**: "Bending MAE | 0.484 mm / 0.562 mm | **0.484 mm** | canonical (stable)"

## Planned or Missing Elements
- `docs/DEEP_METHODS_REVIEW.md`: ** The cameras share the same building and environment
- `docs/DEEP_METHODS_REVIEW.md`: (σ² adds, not 2σ²) is physically reasonable for separate-session recordings (hou
- `docs/DEEP_METHODS_REVIEW.md`: "We assume independent noise between cameras, which is physically plausible for
- `docs/OMRPR_SUPERVISOR_GUIDELINE.md`: ** f_h/f_α/damping values are UNVERIFIED pending a provenance check (Tunnel B Se
- `docs/OMRPR_SUPERVISOR_GUIDELINE.md`: the dp-sensitivity study above was run around the B0 dp=1
- `docs/OMRPR_SUPERVISOR_GUIDELINE.md`: ** Can a fully offline, deterministic, multi-camera

## Duplicate Files Across Trees
- `docs/_archive/CRITICAL_ANALYSIS_REVISED_20260622.md`: identical to Tree 4 (`docs/CRITICAL_ANALYSIS_REVISED_20260622.md`)
- `docs/_archive/DEEP_METHODS_REVIEW.md`: identical to Tree 4 (`docs/DEEP_METHODS_REVIEW.md`)
- `docs/current_ground_truth_audit_2026-06-23.md`: identical to Tree 4 (`docs/_archive/current_ground_truth_audit_2026-06-23.md`)
- `docs/walkthrough_log.md`: identical to Tree 4 (`docs/_archive/walkthrough_log.md`)
- `src/a1_bandlimited_recomparison.py`: identical to Tree 3 (`legacy_src/a1_bandlimited_recomparison.py`)
- `src/a5a6a7_sweep_ablation_crosstalk.py`: identical to Tree 3 (`legacy_src/a5a6a7_sweep_ablation_crosstalk.py`)
- `src/bending_channel_leakage_analysis.py`: identical to Tree 3 (`legacy_src/bending_channel_leakage_analysis.py`)
- `src/comparison_plot_options.py`: identical to Tree 3 (`legacy_src/comparison_plot_options.py`)
