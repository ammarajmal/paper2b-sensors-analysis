# Corrected Discussion/Limitations Guidance

**Status: drafting guidance only. No manuscript file was modified.**

## Required corrections to the proposed blueprint

1. Describe the laser comparison as a **separate 2025 laser campaign** unless a specific source record establishes another year. Do not call it 2024 LDV validation.
2. Use **20 matched RPM conditions** (20--320 RPM) for the camera--laser condition join. The camera dataset also contains 0 RPM, which has no matching laser row in the comparison table. The complete camera inventory contains 63 condition-camera streams (60 admissible, 2 rejected, 1 diagnostic-only), including three camera-only 0 RPM streams; these are not laser-matched observations.
3. The approximately 0.034 Hz value is the median absolute rank-1 bending-frequency difference for cam1/cam2 over the 19 non-320-RPM matched conditions. It is approximately the Rayleigh scale, not strictly within it: the Rayleigh interval is about 0.0327--0.0328 Hz.
4. The bending RMS correlation `r = 0.990` is a sensitivity result for the 17-condition subset excluding 320, 60, and 80 RPM. Report the full 19-condition result (`r = 0.815`) beside it. Do not describe the exclusions as independently established non-resonant conditions.
5. The previous forced-alignment value `r_train = 0.503` and `r_test = -0.118` must not be used as the final aggregate result. The lag-indexing implementation was corrected. For cam1 bending over 19 matched conditions, the corrected medians are approximately `r_train = 0.597`, `r_test = 0.109`, and held-out standardized RMSE `= 1.063`. Across the 57 admissible matched non-320-RPM camera streams (19 conditions × 3 cameras), the corrected bending medians are `0.503` and `0.118`; torsion medians are `0.143` and `0.083`.
6. Do not call the RMS comparison “accuracy,” “validation,” or “energy validation.” Use **cross-campaign RMS response scaling** or **condition-level response correspondence**.
7. Do not call the cam1/cam2/cam3 phase table a mode shape. It is an apparent camera-response phase pattern. Cam1/cam2 observe the same marker; cam3 changes marker location and optical path.

## Safe Discussion wording

“The camera and laser records were acquired in separate campaigns and therefore do not share a verified physical timebase. We nevertheless conducted a forced-alignment stress test as a diagnostic of the limits of post-hoc temporal fitting. For each matched condition, a relative lag was selected by cross-correlation over the first 60% of the available overlap and then applied unchanged to the remaining 40%. The corrected cam1 bending results showed a median training correlation of approximately 0.60 and a median held-out correlation of approximately 0.11 across 19 non-320-RPM conditions; the corresponding held-out standardized waveform RMSE was approximately 1.06. The weak and condition-dependent transfer of the fitted lag indicates that numerical lag optimization can produce apparent alignment without establishing a shared physical timebase. Accordingly, the cross-campaign comparison is restricted to condition-level frequency correspondence and RMS response scaling. Waveform RMSE, cross-correlation, phase coherence, and absolute displacement accuracy are not treated as validated quantities without simultaneous acquisition, hardware timing, common units, and spatial registration.”

## Safe placement

- Main text: frequency correspondence and full-versus-sensitivity-subset RMS scaling, with exact denominators.
- Supplement: forced-alignment plots, lag table, train/held-out results, and apparent phase table.
- Limitations: explicitly state that forced alignment is a stress test, not a synchronization method.

## Source outputs

- `forced_alignment/FORCED_ALIGNMENT_WAVEFORM_RESULTS.csv`
- `forced_alignment/FORCED_ALIGNMENT_SUMMARY.csv`
- `forced_alignment/APPARENT_CAMERA_PHASE_MODE_SHAPE.csv`
- `forced_alignment/clean_plots/`
