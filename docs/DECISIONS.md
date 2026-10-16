# Decisions (append-only; newest last)
| Date | Decision | Source | Consequence |
|---|---|---|---|
| 2026-10-15 | Marker map: cam1/cam2 = offset marker (ID-0-1), cam3 = near-axis marker (ID-0-2) | owner, checked images | SVR "center/side" labels are reversed (NOTES F1) |
| 2026-10-15 | Apparatus facts and IL-300 follow the Measurement paper; T. Mehmood removed from both papers | owner | n/a for code |
| 2026-10-15 | Camera frame rate reported per camera (cam1/cam2 59.94 Hz, cam3 60.00 Hz) | owner + stage S1 | ledger keeps three rates |
| 2026-10-16 | Camera intrinsics = values stored in the bags' `camera_info` (identical to `omrpr_fin/config/pipeline_config.yaml`); never adjusted by laser agreement | owner | `refine_intrinsics_laser.py` not ported; intrinsics uncertainty goes in the budget as an unverified-calibration envelope |
| 2026-10-16 | Exact campaign dates are omitted from the papers | owner | the "11 months" wording is not needed; non-simultaneity is still stated |
| 2026-10-16 | Reuse of the older code approved after reading; new codebase `bridgedeck-vision-pipeline` in `/mnt/space/adev/projects/active/` | owner | this repo |
| 2026-10-16 | Laser inputs: 2024 raw and vendor-camera files read from the P00 TESolution tree, 2025 laser from P00 `Video Measurement/laser_displacement` | sha256 comparison of three copies (2024: identical in all 3; 2025: P00 == USB, github is a subset) | `config/paths.yaml` |
| 2026-10-16 | Intrinsics verified: K and all 14 distortion terms in the bags equal `omrpr_fin/config/pipeline_config.yaml` (sha256 prefix 2ce2d6b1ffeea7d1) for the e0 5-second bag; all-bag check recorded in RUNLOG | direct comparison | source file named in README |
| 2026-10-16 | Detector for production: official AprilRobotics v3.4.5 Python wrapper built by scripts/build_apriltag.sh (gate S2a passed); pupil-apriltags stays only as an optional cross-check | gate S2a | `import apriltag` in the project venv |
| 2026-10-16 | Static bags have their own intrinsics (NOTES F16); WTT intrinsics are the bag values | camera_info of all 62 bags | static data is not pooled with WTT data in millimetres |

## Open (owner)
- O1 primary laser session for Paper 2B (see project kit OPEN_DECISIONS D1)
- O2 outcome-independent rule for the "regime-interior" set (D2)
- O3 bending definition: heave/pitch coordinates vs band-limited bending (D3)
- O4 gate thresholds (Wilson 0.95, margin 30, velocity 27.75 px/frame): re-derive and pre-register in S2, or adopt the SVR candidates
- O5 official `apriltag` binding build vs `pupil-apriltags` as the production detector (decided by the S2 gate result)
