# Per-camera RMS: source-lineage design review (read-only)

Repo HEAD 8d03ba3; nothing outside this directory was modified. Checks were run with the repo `.venv` on existing outputs.

## Answers to the nine questions

1. **Does `results/s4_pose_by_stream.csv` already hold valid per-camera RMS?** Yes, in a defined sense. It has 61 rows (cam1 20, cam2 20, cam3 21), and `H1_y_mm_rms` and `H2_roll_rad_rms` are per-stream values. I recomputed them from `outputs/s4_pose_channels_by_frame.parquet`. The maximum difference is 4e-16, so they reproduce exactly. They are *total* RMS values (see 5). They are not detrended, not band-limited and not noise-corrected.
2. **Definitions.** `H1_y_mm` is the vertical displacement, in mm, of the centroid of the four undistorted corners. The corners are mapped through the inverse of the reference tag-plane homography, and the stream median is subtracted. The reference is the per-stream median corner set against a 20 mm square. `H2_roll_rad` is the unwrapped in-plane edge angle of the same rectified corners, minus its median. Source: `pose.py:175-190`; gate `S4b.md`.
3. **Calibration and tag geometry.**
   - Intrinsics K and the 14-term distortion D come from the `camera_info` of `e0_0rpm_run1.bag`. They are stored in `config/intrinsics_bag.json` and equal `omrpr_fin/config/pipeline_config.yaml` (sha256 2ce2d6b1ffeea7d1...). They were never tuned to the laser.
   - Tag family is tag36h11, id 0, detected by AprilRobotics v3.4.5.
   - The tag side is 20.0 mm, a constant in `pose.py:16`. Its support: ledger section J, GUI `tag_size` 0.02 m, and a ruler check giving 20.1–20.2 mm. The owner has not yet confirmed the ruler graduation, so the budget carries ±2.5% on every mm value.
   - There are no per-tag measured geometry files and no calibration covariance.
   - Hashes are in `PER_CAMERA_RMS_SOURCE_HASHES.sha256`.
4. **Admissibility.**
   - Frame level: `detected` and `decision_margin >= 30`. Frames are sorted by `frame_idx`, with no interpolation or gap filling. The margin cut removes zero frames in this dataset, and Hamming distance is 0 everywhere.
   - Stream level: 60 streams are admitted (e0–e19, three cameras each), plus e20 cam3 as diagnostic-only. e20 cam1 and cam2 are rejected (60.8% and 61.3% detected, speed above tag/10) and are absent from s4.
   - Frame counts: 115,276 total, 113,852 valid, 111,618 used in s4.
5. **What the RMS is.** It is `np.nanstd` (ddof=0) of the whole admitted series about its mean (`run_s4.py:16`). That is total RMS to the camera Nyquist of about 30 Hz, including noise and any low-frequency drift. It is not narrow-band. Linear detrending would change it by 0–2.4%. The narrow-band quantities in s4 and s6 are `*_Afh` and `*_Afa`, which are sinusoid amplitudes (A, not A/√2).
6. **Comparable with the laser?** Only partly.
   - Same statistical form: the laser uses mean-removed total std (ddof=1, 360 Hz, 20 s, to 180 Hz). The ddof difference is under 0.03%.
   - Not the same physical quantity for cam1 and cam2. Those are the *offset* marker, about 125 mm from the rotation axis, so their vertical displacement is approximately heave plus 125 mm × roll. The laser heave is the centre head. Only cam3, the near-axis marker (about 6 mm), approximates laser heave.
   - Camera roll is in-plane tag rotation, compared with laser pitch = (side − centre)/d. The laser pitch depends on d (13 cm or 10 cm), which was not measured here.
   - The record lengths (30.5 s vs 20 s) and noise bandwidths differ. The recordings are separate and not simultaneous.
7. **Does cam3 use a different marker path?** The code path is identical: the same detector, `stream_channels` and `rectified_channels`. The inputs differ.
   - cam3 views a different physical marker (ID-0-2, near the axis). Cam1 and cam2 view ID-0-1.
   - It has its own K and D (fx 25631, against 20328 for cam1 and 25750 for cam2).
   - It runs at 60.00 Hz (cam1 and cam2: 59.94 Hz) and has one duplicate frame per 16 s.
   - Its decision margin is higher (median 110, against 70).
   - It is the only e20 stream retained.
8. **Was the pooled RMS table built from per-camera values?** No.
   - `EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv` is copied from `table_2025_ldv_primary.csv` (dated 2026-10-09).
   - It holds pooled bend = ((y1+y2)/2+y3)/2 and torsion = y3 − (y1+y2)/2, built from P1 (not H1) on cam3 stamps.
   - It differs from the current `s6_matched_pairs` legacy RMS by up to 0.029 mm (bend) and 0.088 mm (torsion), so it comes from an earlier pipeline.
   - Per-camera values cannot be recovered from it: 2 combined series cannot be inverted to 3 per-camera RMS values without cross-covariances.
   - `s6_camera_by_condition.csv` has per-camera line amplitudes only, not RMS.
9. **Expected counts.**

| Item | Expected | Found |
|---|---|---|
| Conditions | 21 | 21 |
| Streams in detections | 63 | 63 |
| Streams in s4 | 61 | 61 |
| e0_0rpm | 3 (cam1, cam2, cam3) | 3 |
| e20_320rpm | 1 (cam3 only, diagnostic) | 1 |
| Admitted streams | 60 | 60 |
| Laser-matched conditions | 20 (20–320 RPM); 19 excluding 320 | 20 |

   - e0 H1_y_mm RMS is 0.0057 / 0.0062 / 0.0032 mm for cam1 / cam2 / cam3. This is the noise floor.
   - e20 cam3 has H1_y RMS 2.18 mm and H2 RMS 0.097 rad, with IPPE order b and 93% ambiguous frames (not used by H1/H2). It is governance-labelled diagnostic-only.

## Risks and cautions
- A different `ddof`, detrend or band choice changes the numbers. Any new RMS must state its choice.
- Noise floors differ between instruments. The camera floor is below the laser's, so rule (a) of the S6 gate (signal ≥ 5× floor for both) should gate the low-RPM conditions.
- 60 and 80 RPM are known regime-boundary disagreements and must be flagged, not dropped silently.
- The scale uncertainty applies to mm only, not to rad.
