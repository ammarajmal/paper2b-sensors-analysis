# Go / No-go: per-camera common-unit RMS

## Decision: CONDITIONAL GO

Per-camera RMS in common units is available for H1_y_mm (mm) and H2_roll_rad (rad). The values already exist in `results/s4_pose_by_stream.csv` and reproduce from the per-frame parquet to 1e-16. The conditions below are required before they are used as laser-comparable.

## Conditions
1. Label the quantity "total mean-removed RMS, ddof=0, full band to about 30 Hz, no detrend". Do not call it narrow-band or equivalent to the line amplitudes.
2. Use H1_y_mm and H2_roll_rad as the primary channels. Note that P1/P5 feed the pooled legacy table. Choose and state which family is used; do not mix them.
3. Report 60 admitted streams (e0–e19 × 3 cameras). Report e20 cam3 separately as diagnostic-only. e20 cam1 and cam2 have no values.
4. Do not equate cam1/cam2 H1_y with laser heave. They carry a lever-arm contribution of about 125 mm × roll. Use cam3 for heave comparison, or state the lever-arm term.
5. The RMS stays comparable to the laser only when the signal is above both noise floors. Apply the S6 rule (a) gate or an equivalent, and flag 60 and 80 RPM as regime-boundary conditions.
6. Carry ±2.5% on mm values for tag size until the owner confirms the ruler graduation. Do not apply it to rad.
7. Do not derive per-camera values from the pooled table. If detrended or band-limited RMS is wanted for like-for-like with the laser, it must be recomputed from `outputs/s4_pose_channels_by_frame.parquet` as a new, labelled analysis. This is a decision for the owner.

## Why not full GO
The laser RMS is a different physical quantity for cam1 and cam2, and the two instruments have different bandwidth, duration and session. These limits come from the data, not from errors in the code.

## Why not NO-GO
Definitions are explicit, inputs are canonical and hashed, the existing values reproduce exactly, and the counts match the ledger.
