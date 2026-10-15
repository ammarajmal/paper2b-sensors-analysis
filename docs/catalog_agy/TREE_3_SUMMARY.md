# Tree 3 Summary: OMRPR Offline Pose Reconstruction (Legacy source, recovery experiments, and documentation)

## Overview and Scope
Tree 3 contains 398 total scanned files (395 catalogued, 3 identical duplicates).
OMRPR Offline Pose Reconstruction (Legacy source, recovery experiments, and documentation).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `docs/omrpr_ubuntu24_bootstrap.sh`
- `legacy_src/a1_bandlimited_recomparison.py`
- `legacy_src/a5a6a7_sweep_ablation_crosstalk.py`
- `legacy_src/bending_channel_leakage_analysis.py`
- `legacy_src/comparison_plot_options.py`
- `legacy_src/comparison_plots.py`
- `legacy_src/comparison_plots_v2.py`
- `legacy_src/e20_diagnostic.py`

## Key Results and Stated Findings
- **`docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`**: "pvolt | 2.7 cm/V | BRID2D1_choi"
- **`docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`**: "dside | 13.0 cm (130 mm) | 설계속도 및 모형Setup_영상계측"
- **`docs/OMRPR_SUPERVISOR_GUIDELINE.md`**: "LDV dside | 10 cm (100 mm) | **130 mm** | `설계속도 및 모형Setup_영상계측"
- **`docs/OMRPR_SUPERVISOR_GUIDELINE.md`**: "LDV db | 20 cm (200 mm) | **200 mm** | Same document"
- **`docs/OMRPR_Ubuntu24_AI_Research_Ecosystem_Guide (1).md`**: "C1: Torsion geometry confirmed — db=200mm, dside=100mm, dp=2.0, citing Lee2016."
- **`docs/OMRPR_Ubuntu24_AI_Research_Ecosystem_Guide (1).md`**: "C2: Max pairwise timing drift = 46.4ms (cam2–cam3)"
- **`docs/gemini_Revised OMRPR Project Publication Readiness Analysis.md`**: "Assessment of 60 Hz Software Synchronization and the 20.0 ms Drift Limitation"
- **`docs/gemini_Revised OMRPR Project Publication Readiness Analysis.md`**: "The OMRPR documentation indicates a maximum software synchronization drift of 20.0 ms"

## Planned or Missing Elements
- `docs/OMRPR_MASTER_AUDIT_SENSORS.md`: Claude position
- `docs/OMRPR_MASTER_AUDIT_SENSORS.md`: Available alternatives:
- `docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`: ** Can a fully offline, deterministic, multi-camera
- `docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`: timestamps
- `docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`: Sparse CSV — frames with no detection produce no row

## Duplicate Files Across Trees
- `docs/OMRPR_SUPERVISOR_GUIDELINE (2).md`: identical to Tree 3 (`docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`)
- `docs/OMRPR_SUPERVISOR_GUIDELINE (3).md`: identical to Tree 3 (`docs/OMRPR_SUPERVISOR_GUIDELINE (1).md`)
- `docs/OMRPR_Ubuntu24_AI_Research_Ecosystem_Guide.md`: identical to Tree 3 (`docs/OMRPR_Ubuntu24_AI_Research_Ecosystem_Guide (1).md`)
