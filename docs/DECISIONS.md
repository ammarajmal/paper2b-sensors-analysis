# Decisions (append-only; newest last)
| Date | Decision | Source | Consequence |
|---|---|---|---|
| 2026-10-15 | Marker map: cam1/cam2 = offset marker (ID-0-1), cam3 = near-axis marker (ID-0-2) | owner, checked images | SVR "center/side" labels are reversed (NOTES F1) |
| 2026-10-15 | Apparatus facts and IL-300 follow the Measurement paper; T. Mehmood removed from both papers | owner | n/a for code |
| 2026-10-15 | Camera frame rate reported per camera (cam1/cam2 59.94 Hz, cam3 60.00 Hz) | owner + stage S1 | ledger keeps three rates |
| 2026-10-16 | Camera intrinsics = values stored in the bags' `camera_info` (identical to `omrpr_fin/config/pipeline_config.yaml`); never adjusted by laser agreement | owner | `refine_intrinsics_laser.py` not ported; intrinsics uncertainty goes in the budget as an unverified-calibration envelope |
| 2026-10-16 | Exact campaign dates are omitted from the papers | owner | the "11 months" wording is not needed; non-simultaneity is still stated |
| 2026-10-16 | Reuse of the older code approved after reading; new codebase `bridgedeck-vision-pipeline` in `/mnt/space/adev/projects/active/` | owner | this repo |

## Open (owner)
- O1 primary laser session for Paper 2B (see project kit OPEN_DECISIONS D1)
- O2 outcome-independent rule for the "regime-interior" set (D2)
- O3 bending definition: heave/pitch coordinates vs band-limited bending (D3)
- O4 gate thresholds (Wilson 0.95, margin 30, velocity 27.75 px/frame): re-derive and pre-register in S2, or adopt the SVR candidates
- O5 official `apriltag` binding build vs `pupil-apriltags` as the production detector (decided by the S2 gate result)
