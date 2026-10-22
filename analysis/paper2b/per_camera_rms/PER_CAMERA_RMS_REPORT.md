# Per-camera RMS, Paper 2B (CONDITIONAL GO implementation)

Script: `run_per_camera_rms.py` (repo HEAD 8d03ba3, runtime in `PER_CAMERA_RMS_RUNTIME.txt`). Run from the repo root with `.venv/bin/python`.
Full results (section 2) are generated and reported before sensitivity results (section 4).

## 1. Provenance and stream accounting

- **63 detection streams** in `detections_ALL21.parquet`; **61 S4 pose streams** in `outputs/s4_pose_channels_by_frame.parquet`.
- **60 admitted streams** (e0–e19 × cam1/cam2/cam3); **2 rejected streams** (e20 cam1, e20 cam2: 60.8% / 61.3% tag detection, no values computed); **1 diagnostic-only stream** (e20_320rpm cam3).
- **Three camera-only 0 RPM streams** (e0_0rpm cam1/cam2/cam3). They are admitted and serve as the per-camera noise floor. There is no laser match at 0 RPM.
- **One diagnostic-only cam3 320 RPM stream.** Its values are in the tables, labelled `diagnostic_only`, and are excluded from the full results. They appear only in the named sensitivity "incl_e20_diagnostic".
- **Per-camera RMS values are reproducible from the frame-level Parquet source.** Source sha256 `9378c6ea…c612` matches the approved registry. The script recomputes all 61 streams × 2 channels from that file. Agreement with `results/s4_pose_by_stream.csv`, used as a check only and not as a value source, is max |diff| 4.4e-16.
- **The pooled RMS table was not the source of the per-camera values.** Neither `table_2025_ldv_primary.csv` nor `EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv` was read.
- Laser values come from `results/laser_y2025_by_condition.csv` and `results/laser_y2024_by_condition.csv` (`heave_mm_rms`). These two files are **not in the approved input registry**. They are hashed in `PER_CAMERA_RMS_SOURCE_HASHES.sha256` and need your confirmation as a laser source.
- Calibration: `config/intrinsics_bag.json` (sha256 `fe2553f1…4ba8`, K and D from the e0 bag `camera_info`) and tag side 20.0 mm.

## 2. Full results

**Definition.** Total mean-removed RMS, `np.nanstd` with ddof=0 about the stream mean. It is full-band to the camera Nyquist (~30 Hz), with no detrend and no noise correction. It is **not** a narrow-band line amplitude. Channels are `H1_y_mm` (mm) and `H2_roll_rad` (rad) throughout, with no mixing with the P1/P5 family. `n_total` is the number of admitted frames in the stream and `n_valid` the number of finite samples; they are equal here.

Table (rows `H1_y_mm_rms_total_meanremoved` and `H2_roll_rad_rms_total_meanremoved` in `PER_CAMERA_RMS_VALUES.csv`; mm values carry ±2.5% scale bounds in `rms_scale_lo/hi`, rad values none):

| rpm | H1_y cam1 (mm) | cam2 | cam3 | H2 cam1 (rad) | cam2 | cam3 |
|---|---|---|---|---|---|---|
| 0 (floor) | 0.00572 | 0.00617 | 0.00316 | 1.0e-4 | 1.0e-4 | 1.9e-4 |
| 20 | 0.00728 | 0.00801 | 0.00301 | 1.1e-4 | 1.0e-4 | 1.8e-4 |
| 40 | 0.01009 | 0.01054 | 0.00967 | 1.0e-4 | 1.1e-4 | 4.7e-4 |
| 50 | 0.02238 | 0.02263 | 0.02408 | 1.2e-4 | 1.6e-4 | 8.8e-4 |
| **60** | 0.08537 | 0.08521 | 0.08676 | 1.4e-4 | 2.9e-4 | 1.2e-3 |
| 70 | 3.092 | 3.101 | 3.097 | 4.0e-4 | 3.6e-4 | 6.5e-4 |
| **80** | 1.411 | 1.409 | 1.400 | 9.3e-4 | 9.4e-4 | 1.25e-3 |
| 90 | 1.638 | 1.641 | 0.1041 | 0.01291 | 0.01302 | 0.01285 |
| 100 | 0.2485 | 0.2482 | 0.1233 | 1.76e-3 | 1.75e-3 | 2.07e-3 |
| 110 | 0.1762 | 0.1757 | 0.1536 | 5.2e-4 | 5.4e-4 | 1.3e-3 |
| 120 | 0.2460 | 0.2455 | 0.1512 | 1.23e-3 | 1.25e-3 | 1.65e-3 |
| 140 | 1.432 | 1.431 | 0.1856 | 0.01059 | 0.01064 | 0.01072 |
| 160 | 2.387 | 2.384 | 0.2618 | 0.01835 | 0.01834 | 0.01841 |
| 180 | 2.804 | 2.797 | 0.3674 | 0.02222 | 0.02186 | 0.02219 |
| 200 | 2.895 | 2.904 | 0.3842 | 0.02352 | 0.02335 | 0.02376 |
| 220 | 2.113 | 2.116 | 0.5020 | 0.01744 | 0.01750 | 0.01774 |
| 240 | 0.7406 | 0.7405 | 0.6914 | 2.15e-3 | 2.16e-3 | 2.36e-3 |
| 260 | 0.8551 | 0.8552 | 0.8301 | 1.50e-3 | 1.54e-3 | 1.78e-3 |
| 280 | 1.110 | 1.110 | 1.074 | 1.93e-3 | 1.93e-3 | 2.08e-3 |
| 300 | 1.254 | 1.254 | 1.212 | 3.28e-3 | 3.32e-3 | 3.47e-3 |
| 320 | not computed | not computed | 2.183 (**diagnostic-only**) | not computed | not computed | 0.0967 (**diagnostic-only**) |

The cam3 320 RPM IPPE ambiguity applies to the pose-order channels. H1/H2 are computed from the rectified corners. The stream is still labelled diagnostic-only by governance, and the 2.18 mm / 0.097 rad values are not admitted results.

### Noise floor (e0_0rpm, per camera) and ratios
Floors are the e0 total RMS above: H1_y 0.0057 / 0.0062 / 0.0032 mm (cam1/cam2/cam3) and H2 1.0e-4 / 1.0e-4 / 1.9e-4 rad. Ratios for every condition are in `PER_CAMERA_RMS_VALUES.csv` (`*_noise_floor_ratio`). Ratios below 5× (the S6 rule (a) threshold, applied here on the camera side only) are flagged `below_5x_camera_floor`:

- H1_y: cam1 and cam2 at 20, 40 and 50 RPM; cam3 at 20 and 40 RPM.
- H2: cam1 at 20, 40, 50, 60, 70 and 110; cam2 at 20–70; cam3 at 20, 40, 50 and 70 RPM.
- The laser noise floor is not available in this analysis. The S6 both-sided gate is therefore **not** reproduced.

### Flags
- **60 and 80 RPM regime-boundary sensitivity** (`regime_boundary_60_80_sensitivity`). Retained in all full results and excluded only in named sensitivity rows.
- **320 RPM admissibility.** Only cam3 exists and it is `diagnostic_only`. e20 cam1/cam2 are rejected.

### Comparisons (full stage; admitted e1–e19, n = 19 conditions, one value per condition)
Per-condition rows are in `PER_CAMERA_RMS_COMPARISON.csv`.

**cam1/cam2 same-marker (ID-0-1).** H1_y RMS agrees: geometric-mean ratio cam1/cam2 = 0.992, Spearman 1.00. Lever-arm descriptive check: cam1/cam2 H1_y RMS divided by (125 mm × own roll RMS) is 0.97–1.13 at 90, 100 and 140–220 RPM, the strong-roll conditions. It is larger elsewhere (up to 4.6 at 240–280 RPM, and 61 at 70 RPM where heave dominates), so the vertical displacement there is not explained by the lever-arm term alone. At the strong-roll conditions the cam1/cam2 vertical displacement is essentially the lever-arm term. It is **not laser heave** and is not labelled as such. This is an RMS-magnitude comparison with no phase information.

**cam3 observation path.** cam3 views a different physical marker (ID-0-2, near axis), with its own K/D and 60.00 Hz rate (cam1/cam2: 59.94 Hz). cam3/cam1 H1_y geometric-mean ratio 0.458 and cam3/cam2 0.455 (Spearman 0.65). The gap is concentrated at the roll-dominated conditions (90 and 140–220 RPM), where cam3 H1_y is 4–16× smaller than cam1/cam2 (about 2× at 100 and 120 RPM) while the H2 roll RMS is within about 2% on all three cameras. cam3 and cam1/cam2 agree within 8% at 40–80 and 240–300 RPM. The paths are kept separate and never averaged or combined.

**cam3 vs laser heave (primary, laser y2025 session).** Geometric-mean ratio cam3/laser = **0.515**, Spearman **0.726** (n = 19). The ±2.5% camera scale gives ratio bounds ×0.975 to ×1.025 per condition (`ratio_scale_lo/hi`). The laser's own scale uncertainty is not propagated.

| rpm | cam3 H1_y (mm) | laser heave y2025 (mm) | ratio |
|---|---|---|---|
| 20 / 40 / 50 | 0.0030 / 0.0097 / 0.0241 | 0.137 / 0.138 / 0.139 | 0.02–0.17 |
| 60 | 0.087 | 1.761 | 0.049 |
| 70 | 3.097 | 2.923 | 1.06 |
| 80 | 1.400 | 0.235 | 5.96 |
| 90–220 | 0.10–0.50 | 0.19–0.59 | 0.51–0.85 |
| 240–300 | 0.69–1.21 | 0.78–1.13 | 0.81–1.17 |
| 320 (diagnostic) | 2.183 | 2.175 | 1.00 |

The laser y2024 session is reported separately: geometric-mean ratio 0.773, Spearman 0.675. cam1 and cam2 versus laser are also computed, each separately and flagged as offset-marker vertical, not heave. cam1 geometric-mean ratio vs laser y2025 is 1.12 and cam2 1.13.

**Differences that must travel with any camera–laser statement.**
- Bandwidth: camera Nyquist ≈ 30 Hz (59.94–60.01 Hz sampling); laser 360 Hz sampling, 180 Hz band.
- Record length: camera 30.46–30.55 s; laser 20 s (y2025) or 30 s (y2024).
- Campaign/session: the camera dataset (ds004_windtunnel_cameras_2025) and the laser sessions are separate, non-simultaneous recordings. I did not verify which laser session shares a campaign with the cameras. The y2025 session was chosen as primary on dataset naming only, and both sessions are reported.
- ddof: laser uses ddof=1, camera ddof=0 (<0.03% effect).
- At 20–50 RPM the laser sits at its own floor, ≈0.137 mm (y2025) or ≈0.032 mm (y2024), above the camera values. Ratios there compare camera noise to laser noise and are not heave information.

## 3. What is not claimed
No calibration, accuracy, synchronization or validation claim is made by these numbers. The ±2.5% scale is provisional (ruler graduation unconfirmed). It is applied only to mm values, and not to rad values or to same-stream noise-floor ratios, where it cancels. Band-limited like-for-like RMS was not computed (not part of this approval). No roll-versus-laser-pitch comparison is made, because laser pitch depends on an unmeasured lever distance d.

## 4. Sensitivity results (generated after section 2)

Unit of analysis is the condition for all of these. Bootstrap resamples conditions (10,000 draws, seed 20261022, percentile 95% interval). Leave-one-condition-out (LOCO) gives the range over all single-condition deletions.

**Linearly detrended RMS** (`*_rms_linear_detrended`, named separately). Ratio to total RMS is 0.976–1.000 over all 61 streams × 2 channels. cam3/laser y2025 is unchanged (geometric-mean ratio 0.515, Spearman 0.726).

**cam3 vs laser heave y2025:**

| variant | n | geomean ratio | Spearman |
|---|---|---|---|
| full (e1–e19) | 19 | 0.515 | 0.726 |
| bootstrap | 19 | 0.519 [0.283, 0.874] | 0.748 [0.271, 0.995] |
| LOCO range | 18 | 0.450–0.614 | 0.678–0.895 |
| **excluding 60 and 80 RPM** | 17 | 0.512 | **0.985** |
| bootstrap, excl. 60/80 | 17 | 0.524 [0.296, 0.789] | 0.985 [0.901, 1.000] |
| LOCO range, excl. 60/80 | 16 | 0.486–0.624 | 0.982–0.994 |
| incl. e20 diagnostic | 20 | 0.533 | 0.765 |
| camera ≥5× own floor | 17 | 0.697 | 0.618 |

y2024 laser: full 0.773 / 0.675; excluding 60 and 80 RPM 0.788 / 0.995; bootstrap 0.780 [0.470, 1.236] and Spearman [0.186, 1.000].

**Reading.** The rank agreement between cam3 and the laser is driven almost entirely by the two regime-boundary conditions: it moves from 0.73 to 0.985 when 60 and 80 RPM are removed, in both laser sessions. The magnitude ratio is stable near 0.5 (y2025) and 0.8 (y2024) under every deletion, and the ±2.5% scale does not account for it. The wide bootstrap Spearman interval shows how much this statistic depends on those two points. Under the camera-floor gate Spearman is lower (0.62) while the ratio is higher (0.70), because the gate drops only the lowest-RPM points and keeps 60 and 80.

## 5. Files
`PER_CAMERA_RMS_VALUES.csv` (488 rows: 8 quantities × 61 streams; extra columns `scale_rel_unc`, `rms_scale_lo/hi`, `flags` follow the required ones), `PER_CAMERA_RMS_COMPARISON.csv` (condition rows and summary rows, full stage first), `PER_CAMERA_RMS_DEFINITION_LEDGER.csv` (approved ledger plus new terms), `PER_CAMERA_RMS_SOURCE_HASHES.sha256`, `PER_CAMERA_RMS_RUNTIME.txt`, `plots/` (RMS vs rpm for H1_y and H2, noise-floor ratio, cam3 vs laser, camera-path ratios).
Nothing outside `analysis/paper2b/per_camera_rms/` was written. Manuscript files and existing statistical outputs were not touched.
