# Paper 2B Statistical Analysis Plan

## Scope

This is a separate, evidence-first, condition-level statistical package. It does not edit the manuscript, supplement, frozen outputs, raw bags, canonical source files, or existing audit outputs.

## Units and domains

Matched RPM condition is the unit for camera–laser comparisons; condition-camera stream is the unit for camera spectral results; cam1/cam2 same-marker condition pair is the unit for repeatability. The laser domain contains 20 RPM conditions (20–320 RPM). Camera frequency summaries use 19 admissible non-320 conditions because cam1/cam2 at 320 RPM are rejected and cam3 is diagnostic-only. RMS pooled camera/laser values are available for all 20 conditions. The complete camera inventory is 63 streams (60 admissible, 2 rejected, 1 diagnostic-only), including three camera-only 0 RPM streams that have no matched laser condition and are excluded from every camera–laser comparison.

## Estimands

Frequency correspondence reports signed and absolute error, median, mean, IQR, RMSE, 90th percentile, 0.1 Hz and Rayleigh fractions. RMS scaling reports Pearson, Spearman, robust winsorized Pearson, RMSE in available mm units, ratios, descriptive regression, residuals, and full-before-sensitivity subsets. Repeatability reports paired frequency differences, pixel-RMS ratios, relative differences, bootstrap intervals, and a paired permutation test. Cam3 is retained as observation-path dependence.

## Resampling and tests

All bootstrap resampling is at the complete-condition level, with 10,000 percentile resamples and fixed seed 0. Leave-one-condition-out results are reported for each RMS correlation. No frame-level hypothesis tests are performed. statsmodels is installed in the project environment; no network access is used.

## Forced alignment

The corrected pre-existing forced-alignment outputs are reused: lag estimated on the first 60%, applied to the last 40%, with interpolation onto a common mathematical grid. Training/held-out correlation, standardized RMSE, and conditional coherence/phase are diagnostics only. This is mathematical forced alignment, not recovery of a physical shared clock. The obsolete `r_test = -0.118` value is excluded.

## Interpretation restrictions

These results are operational correspondence, response-trend association, same-marker repeatability, observation-path dependence, and processing sensitivity. They do not establish camera accuracy, calibration, causality, simultaneous validation, synchronization, a unique structural mode, or modal identification.
