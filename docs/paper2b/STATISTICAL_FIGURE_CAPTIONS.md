# Proposed figure captions: statistical supporting layer (Paper 2B)

**Status:** guidance only. Source plots are in `analysis/paper2b/statistical/plots/` (10 PNGs) and
`analysis/paper2b/per_camera_rms/plots/` (4 PNGs). Which plots enter the manuscript versus the supplement
is an owner decision (OI-12). The statistical plots are PNG; the journal figures need >= 300 dpi, which
has not been checked (OI-12). Captions use only the denominators validated in the package.

Common sentence for every statistical figure: *The unit is the RPM condition. Camera-laser comparisons
are cross-session, non-simultaneous operational correspondence, not accuracy or simultaneous validation.*

1. **`01_frequency_by_rpm.png`.** Camera frequency selected by the nearest-retained-peak rule against RPM for
   the laser bending target, 19 non-320 conditions per camera. Cam1, cam2 and cam3 are shown separately.
   Operational correspondence only.
2. **`02_rms_by_rpm.png`.** Pooled camera and laser bending RMS in millimetres against RPM across all 20
   laser-matched conditions. The pooled camera source is not camera-specific.
3. **`03_full_vs_sensitivity_regression.png`.** Descriptive camera-on-laser regression for the full
   20-condition set and for the subset excluding 320, 60 and 80 RPM. The slope is a response-trend
   description, not a calibration.
4. **`04_cam1_cam2_frequency_difference.png`.** Cam1 minus cam2 dominant-frequency difference for 19
   non-320 conditions (same marker). Repeatability, not accuracy.
5. **`05_cam1_cam2_rms_ratio.png`.** Cam1/cam2 pixel-RMS ratio against RPM for 19 non-320 conditions
   (same marker).
6. **`06_cam3_relative_response.png`.** Cam3 RMS relative to the cam1/cam2 mean. Observation-path
   dependence only; marker location and camera channel are confounded.
7. **`07_leave_one_out_range.png`.** Correlation range after removing each non-320 condition in turn.
   There is no frame-level replication.
8. **`08_forced_alignment_train_heldout.png`.** Training against held-out correlation after fitting a lag on the first 60%
   of each record. Mathematical forced alignment; not recovery of a physical shared clock and not
   waveform validation.
9. **`09_frequency_error_rayleigh.png`.** Absolute frequency difference in units of the Rayleigh interval.
   Rayleigh resolution is a record property, not estimator uncertainty.
10. **`10_ratio_summary.png`.** Condition-level pooled camera/laser RMS ratios. The pooled source has no
    camera-specific cam3 common-unit RMS. Ratios are not expected to equal one.

Per-camera RMS plots (`per_camera_rms/plots/`):

11. **`rms_by_rpm_H1_y_mm.png`.** Per-camera H1,y RMS (mm). Cam1 and cam2 view the same side/off-center
    marker (handwritten label ID-0-1); their H1,y is its vertical metric motion and includes a lever-arm x
    roll term, so it is not direct heave. Cam3 views a distinct centre marker (handwritten label ID-0-2)
    and is the heave proxy, with data-derived, unsurveyed geometry. Both markers decode as AprilTag ID 0.
    The 0 RPM point is the camera-only noise floor.
12. **`rms_by_rpm_H2_roll_rad.png`.** Per-camera H2 roll RMS (rad); rad values carry no scale bound.
13. **`noise_floor_ratio_H1_y.png`.** H1,y RMS divided by the same camera's 0 RPM RMS. Points below 5x are flagged.
14. **`camera_path_ratios.png`.** Cam1/cam2 (same marker) and cam3/cam1, cam3/cam2 (observation path) RMS
    ratios, shown separately.

Do not reuse the captions in `FIGURE_CAPTIONS.md` verbatim without checking the 63/60 wording: its
statement that all plots draw on "60 camera-laser matched streams" is correct for the e1-e20 set but would
be read against the manuscript's different 60 admitted streams.
