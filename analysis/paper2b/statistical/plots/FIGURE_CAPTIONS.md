# Statistical plot captions

All plots use condition-level units drawn from the 60 camera-laser matched streams (the 63-stream inventory minus three camera-only 0 RPM streams; see `STREAM_INVENTORY_VALIDATION.csv`). Frequency and RMS comparisons are cross-session operational correspondence, not accuracy or simultaneous validation.

1. `01_frequency_by_rpm.png`: Camera frequency selected by the existing nearest-retained-peak rule against RPM for the laser bending target; 19 non-320 admissible conditions per camera.
2. `02_rms_by_rpm.png`: Pooled camera and laser bending RMS values in millimetres across all 20 matched RPM conditions.
3. `03_full_vs_sensitivity_regression.png`: Descriptive camera-on-laser regression for the full 20-condition set and predeclared sensitivity subset excluding 320, 60, and 80 RPM.
4. `04_cam1_cam2_frequency_difference.png`: Same-marker cam1 minus cam2 dominant-frequency differences for 19 non-320 conditions.
5. `05_cam1_cam2_rms_ratio.png`: Cam1/cam2 pixel-RMS ratio by RPM for 19 non-320 conditions.
6. `06_cam3_relative_response.png`: Cam3 RMS relative to the same-marker cam1/cam2 mean; observation-path dependence only.
7. `07_leave_one_out_range.png`: Correlations after removing each non-320 condition; no frame-level replication.
8. `08_forced_alignment_train_heldout.png`: Corrected mathematical forced-alignment training versus held-out correlation; not physical clock recovery.
9. `09_frequency_error_rayleigh.png`: Absolute frequency error in Rayleigh intervals; Rayleigh resolution is not estimator uncertainty.
10. `10_ratio_summary.png`: Condition-level camera/laser RMS ratios; the pooled source lacks camera-specific cam3 common-unit RMS.
