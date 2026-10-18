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

## Owner decisions of 2026-10-16 (second batch)
| ID | Decision (owner's words, condensed) | How it is carried out |
|---|---|---|
| O1 | 2025 laser is expected to become the ONLY reference (closer in time, matched the camera better). Keep both lasers for now, reprocess BOTH from raw, re-test; only after the results confirm that 2025 still matches closer, discard 2024 from comparisons and the paper. | Stage S5/S6 run both sessions with identical code. Confirmation test and its criterion are written before the run (docs/gates/S6.md). 2024 is dropped only after that test. |
| O2 | Define the regime rule from physics or the noise floor, apply it to both lasers, show all 19 conditions first. Drop 2024 at the end if 2025 is good enough. | Rule written and committed before any comparison (docs/gates/S6.md). All 19 first. |
| O3 | Try both definitions of bending (band-limited and heave/pitch) and search for other alternatives; derive results; choose which numbers go in the paper at the end. | S4/S6 compute every candidate; selection after results, recorded in DECISIONS.md. |
| O4 | The circularity of the gate thresholds is valid. Find a reasonable solution from the literature, test 3 to 4 candidate rules (outliers, other statistics), set them aside, derive results, select after analysis. | docs/gates/S2c.md: candidate rules fixed first, evaluated on out-of-sample data (the 5-second repeat bags). |
| O5 | Use the latest official AprilTag release; suggest anything better, otherwise use it. | Latest tag checked (see below). v3.4.5 stays the reference for reproducing the frozen detections; a newer release is tested as a sensitivity run. |
| D6 | Do not use three values per mode. Reproduce the natural frequencies from raw data once, use that one value everywhere. | S5 free-vibration analysis from the raw 2025 records, with an uncertainty interval; the single value is then used in both papers. |

## Open-issue checks of 2026-10-17 (docs/OPEN_ISSUES_2026-10-17.md)
- Tag size: ruler graduations support 20 mm to about 1% (ticks assumed 5 mm; owner to confirm the ruler). Budget carries 2.5% until confirmed.
- Camera scale: +/-2.5% changes the primary heave error E by at most 0.003; the laser cannot determine the tag size (opposite optimum scales for the two sessions).
- Laser spacing d: full difference over d is supported by the camera angle (ratio about 1.1-1.2, not 0.5-0.6); implied d is 10-16% below the vendor values (13 cm, 10 cm); carried as an input with +/-15%, not tuned.

## Owner decisions of 2026-10-17 (fixed before S7)
| ID | Decision | Provenance / reason |
|---|---|---|
| T | Tag size fixed at 20 mm | ruler check 20.1-20.2 mm (docs/OPEN_ISSUES_2026-10-17.md); acquisition GUI 0.02 m. Budget carries 2.5% (bound) until the ruler graduation (5 mm ticks) is confirmed |
| d | Laser head spacing primary = 13 cm (2025) and 10 cm (2024), +/-15% (bound) in the budget; 12 cm and 8 cm only as sensitivity | 13 cm (2025): verified 2026-10-17 in vendor workbook 설계속도 및 모형Setup_영상계측.xlsx, sheet '모형 Setup! (2)', cell B29 '센서간격' = 13cm, and in vendor script laser_displacement/등류/영각00/BRID2D1.m (modified 2025-09-21), line 19 `dside=13 % cm`. 10 cm (2024): vendor script RAW_Data/laser_displacement/2D_WTT/BRID2D1_choi.m (modified 2024-11-12), line 17 `dside = 10; % side sensor 거리 [cm]`; no spreadsheet entry. In both scripts d is the side-sensor-to-centre-sensor distance (pitch = (side - centre)/d). Whether the workbook's '센서간격' means the same distance is an inference from the equal value, not stated. Camera-implied values 11.7 and 8.4 cm are a consistency check, not a calibration |
| R | Regime rule a (both instruments >= 5x their own zero-wind amplitude) is adopted as the basis for the 2025-versus-2024 decision, as an AMENDMENT to the primary (rule d) fixed on 2026-10-17 | reason (physical, not outcome): a ratio is only meaningful where both instruments clearly see the motion. The amendment is made after seeing S6 results and must be stated as such in the paper; rule d (all 19) remains reported |
| other | all four regime rules, all metrics, both pairing arms stay recorded; S6b variants stay exploratory | owner 2026-10-17 |

## Owner decision of 2026-10-17 (after S8)
| ID | Decision | Reason |
|---|---|---|
| N | The manuscripts carry the REBUILT numbers throughout (ledger values, not the earlier published or audit values) once each number is in the ledger with provenance | single reproducible source; owner decision 2026-10-17. Numbers without a ledger row stay "as previously computed" until they have one. Consequence: abstract values such as mean ratio 1.217 and RMSE 0.288 change in the revision |

## Owner decision of 2026-10-18
| ID | Decision | Reason |
|---|---|---|
| W | The 2025 wind-speed calibration / anemometer record cannot be found; proceed without it. All camera-laser comparisons are at equal fan RPM. The 2025 workbook wind column (about half the 2024 column at every RPM) is treated as unverified and is not used as a comparison axis; S6 arm B is reported for 2024 only or flagged. Wind speeds printed in the papers are the Measurement-paper RPM-derived values and must be stated as an assumption for the 2025 session | S10: both lasers and the camera lock in at the same RPM, which contradicts a factor-two flow difference, so the 2025 wind column is probably a recording issue; not resolvable from data |

## Still open
- Final selection among candidates for O3 and O4, and whether 2024 is dropped (O1), after the analyses above.
- Kit D4, D5, D7, D8 (see the kit OPEN_DECISIONS.md).
