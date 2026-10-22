# Exploratory Camera–Laser Accuracy and Modal-Interpretation Study

**STATUS: EXPLORATORY ONLY — NOT MANUSCRIPT-AUTHORIZED.**

This report is for experimental-design understanding. It does not promote any result to camera accuracy, simultaneous validation, or structural modal identification.

## Inputs and mapping

- Frozen camera peaks: `/mnt/space/adev/research/phd/phd-research-advisory/03_PACKAGES/chat/CLAUDE_SCIENTIFIC_AUDIT_v3/30_RESULTS/25A_REFERENCE_BLIND_PEAKS_FROZEN.csv`; 315 rows, five reference-blind peaks per stream.
- 2025 laser condition table: `/mnt/phd_data/phd_master/05_publications/p02_sensors_windtunnel/scripts/table_2025_ldv_primary.csv`; 20 conditions, 20–320 RPM.
- Historical dominant-frequency join table: `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/analysis_2026-10-15/laser2025_vs_camera_dominant.csv`.
- Raw-derived laser summary: `/mnt/phd_data/phd_master/04_code_software/bridgedeck-vision-pipeline/working_tree/results/laser_y2025_by_condition.csv`.
- Condition-level mapping: laser D01–D20 to camera e1_20rpm–e20_320rpm by RPM. The campaigns were not synchronized.

For every camera and each laser bending/torsional dominant frequency, the closest of the camera's five retained peaks was selected. This is a sensitivity-oriented nearest-peak comparison, not a pre-registered validation rule.

## Stream inventory scope

The full camera inventory is 63 condition-camera streams (21 conditions × 3 cameras; 60 admissible, 2 rejected, 1 diagnostic-only), including three camera-only 0 RPM streams. This study uses only the 60 streams with a matched laser condition (20–320 RPM); 0 RPM streams are not laser-matched observations. The 114 frequency-match rows are 19 non-320 conditions × 3 cameras × 2 targets. The canonical inventory is `results/s2c_stream_table_dev.csv`.

## Interpretation boundary

Frequency correspondence can be quantified directly. RMS amplitude ratios are only condition-level cross-session comparisons, not same-waveform accuracy. Modal identification cannot be established from dominant-frequency agreement alone; it requires mode-shape information, spatially registered observables, and a defined structural/modal reference.

Two frequency views are reported separately: `EXPLORATORY_CAMERA_LASER_DOMINANT_SUMMARY.csv` compares each camera's rank-1 peak with each laser dominant frequency; `EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv` selects the closest among five retained camera peaks. The latter is intentionally optimistic and must not be presented as an unbiased validation result.

The camera cam1/cam2 pair observes the same marker, while cam3 uses a different camera–marker path; cam3 must remain separate in interpretation. The laser quantities are derived from center/side channels and geometry-scaled differences; calibration constants and spatial equivalence should be treated as assumptions or historical script-derived quantities unless independently documented.

## What would be needed for a genuine accuracy/validation claim

- simultaneous camera and laser acquisition with a common hardware timebase or recorded synchronization pulse;
- the same physical point/quantity, or a documented geometric transfer function;
- camera and laser calibration uncertainty with propagation;
- waveform/window comparison in common units, not only condition-level RMS/frequency tables;
- predeclared matching rules and tolerances;
- blinded or hold-out conditions, including unfavorable 60, 80, and 320 RPM regimes;
- for modal identification: multiple spatially registered points, phase/mode-shape information, and a structural reference or model.

## Files

- `EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv`
- `EXPLORATORY_CAMERA_LASER_FREQUENCY_SUMMARY.csv`
- `EXPLORATORY_CAMERA_LASER_DOMINANT_SUMMARY.csv`
- `EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv`
- `EXPLORATORY_CAMERA_LASER_RMS_SUMMARY.csv`
- `EXPLORATORY_SOURCE_HASHES.json`
- `EXPLORATORY_RUNTIME.txt`
