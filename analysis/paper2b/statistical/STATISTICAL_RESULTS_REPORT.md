# Paper 2B Statistical Results Report

**Status:** exploratory, evidence-bounded, and separate from manuscript authority.

## Scope and denominators

The matched laser domain is exactly 20 RPM conditions. The canonical stream table (`results/s2c_stream_table_dev.csv`) contains 63 condition-camera streams (21 conditions x 3 cameras): 60 admissible, 2 rejected (cam1/cam2 at 320 RPM), and 1 diagnostic-only (cam3 at 320 RPM). The complete camera inventory contains 63 condition-camera streams, including three camera-only 0 RPM streams. Camera–laser correspondence analyses use 19 non-320 matched RPM conditions; 0 RPM streams are not treated as laser-matched observations. The spectral-shape input has 60 rows because it excludes the camera-only 0 RPM streams; it is a matched-analysis input, not the stream inventory (see `STREAM_INVENTORY_VALIDATION.csv`). Frequency correspondence therefore has 19 admissible conditions per camera and 114 condition-camera-target rows across three cameras, two targets, and 19 conditions. RMS response scaling uses the available pooled camera/laser table with 20 conditions; it is not camera-specific for cam1/cam2/cam3.

## Results

The CSV outputs are the numerical record. Full results precede sensitivity subsets in every table. `FREQUENCY_CORRESPONDENCE_RESULTS.csv` reports operational frequency correspondence, not modal-frequency accuracy. `RMS_SCALING_RESULTS.csv` reports cross-session response-trend association and descriptive regression. `REPEATABILITY_RESULTS.csv` is the strongest basis for a same-marker repeatability claim. `STATISTICAL_COMPARISONS.csv` keeps cam3 separate and contains the corrected forced-alignment diagnostics.

Pearson describes linear trend association; Spearman describes monotonic trend association; neither proves equality, calibration, causality, or accuracy. Regression is a cross-campaign response-scaling description, not calibration. RMS ratios are not expected to equal one without validated common-unit and spatial equivalence.

## Sensitivity and uncertainty

Condition-level percentile bootstrap intervals use 10,000 resamples and seed 0. Leave-one-condition-out results identify the effect of individual RPM conditions on Pearson and Spearman correlations. The 60, 70, 80, 300, and 320 RPM conditions are retained in the audit trail; excluding 60 and 80 RPM is a sensitivity analysis and cannot replace the full result.

## Forced-alignment warning

The forced-alignment result estimates lag from the first 60% and evaluates the fixed lag on the remaining 40% after interpolation to a common mathematical grid. It is mathematical forced alignment, not recovery of a physical shared clock. Conditional coherence and phase are diagnostics, not physical waveform validation. The obsolete `r_test = -0.118` result is not used.

## Claim boundary

Permitted language is: condition-level statistical characterization of camera spectral-feature repeatability, response-trend correspondence, observation-path dependence, and processing sensitivity. Prohibited language is camera accuracy, simultaneous validation, synchronized exposure, calibration, unique torsional/bending mode, or structural modal identification.

## Reproducibility

Run `python3 run_statistical_analysis.py` from this directory. Input hashes (including the canonical stream table `results/s2c_stream_table_dev.csv`) are recorded in `STATISTICAL_SOURCE_HASHES.sha256`; the 63/60/2/1 stream-inventory check is in `STREAM_INVENTORY_VALIDATION.csv`; runtime, package versions, bootstrap seed, domains, and admissibility counts are in `STATISTICAL_RUNTIME.txt`.
