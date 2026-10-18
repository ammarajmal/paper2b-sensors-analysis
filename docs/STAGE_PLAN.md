# Stage plan (revised 2026-10-16 after the reference-code audit)
Rule: before each stage runs, its gate file `docs/gates/Sx.md` is written and committed (criteria, inputs, tolerances). A failed gate is a finding.
Consumers: **2A** = Sensors paper, **2B** = Measurement paper, **D** = dissertation.

| Stage | Work | Gate (written before running) | Feeds | Status |
|---|---|---|---|---|
| S1 | Frame-timing census of the 42 wind-tunnel bags (header vs record stamps, duplicates, gaps) | 126 streams equal the earlier extraction | 2A 2B D(timing chapter) | **done, 0 mismatches** |
| S1b | Same for the 20 static bags (they have different intrinsics, NOTES F16) | reproduce: 5 clean bags, 7 below 55 Hz, 8 with dropped frames | D | **DONE 2026-10-18 (recompute identical; counts 4 clean / 7 low / 12 dropped vs plan 5/7/8, see docs/gates/S1b.md)** |
| S2a | Build official AprilRobotics v3.4.5 binding (commit prefix 94be783) in a separate prefix; record library hash | `import apriltag` works; detector settings tag36h11, threads 1, maxhamming 0, decimate 1, blur 0, refine_edges True | all | **done, gate passed 2026-10-16** |
| S2 | Detect tags in all 115,276 WTT frames | vs frozen `per_frame_detections.csv`: same detected flag in >= 99.9% of frames; corner differences median <= 0.01 px, 99th percentile <= 0.1 px; every frame outside explained. Cross-check pupil-apriltags on e0/e7/e14 | all | **done, gate passed (100% flags, corners to 7e-7 px)** |
| S2b | Test the background-compensation hypothesis (NOTES F2): raw vs ECC-compensated amplitude at e7 and e14, plus a no-compensation baseline | decision rule fixed first: compensation is kept only if it lowers static (e0) RMS on all three cameras and leaves e7/e14 amplitude within 2% | 2B | **DONE 2026-10-18: compensation NOT kept (removes 96-99% of the 90 RPM line; docs/gates/S2b.md)** |
| S3 | **DONE 2026-10-17 (gate passed).** Spectral estimators: native-timestamp Lomb-Scargle (generalized), Baluev FAP, bootstrap frequency interval, full-record Welch cross-check; native vs interpolated vs nominal-60 timebase | dominant peaks match the frozen Sensors table within 0.5 Rayleigh bin; Task 3 median recovery error reproduces 1.59% | 2A D | todo |
| S4 | **DONE 2026-10-17 (gate passed; PnP angles flagged unreliable).** Pose: PnP (IPPE) with bag intrinsics; scale-factor in-plane estimator; IPPE two-solution ambiguity flag; heave/pitch from the owner marker map | e0 static RMS within 2x of S05.01 values; synthetic translation test RMS < 0.01 px; estimator spread reported | 2B D | todo |
| S5 | Laser: parse 2024 and 2025 raw D-files; unit test (native cm -> mm); test both D-file mappings (NOTES F3); regress against facility sheets; vendor 2024 camera check (F7) | mapping chosen by pre-listed physical tests (monotone RMS with wind speed, lock-in near 1.43/3.10 Hz); reproduces Table S2 for the chosen mapping; the 2025 torsion halving documented | 2B | todo |
| S6 | **RUN 2026-10-17; primary closeness test not met (see gate).** | Camera-vs-laser comparison: all 19 conditions first, then any subset by an outcome-independent rule (O2); both laser sessions; Deming/EIV; leave-one-out; effective n | rule file committed before the comparison | 2B | blocked on O1-O3 |
| S7 | Uncertainty: GUM table + Monte Carlo through S4 (static noise, intrinsics envelope, scale, timing, laser) | each component has a source and a number or is listed as unquantified | 2B D | **GUM budget DONE 2026-10-17 (docs/gates/S7.md); Monte Carlo through S4 and the intrinsics envelope NOT done** |
| S8 | `results/ledger.csv`, one script per figure/table, number-check against manuscripts | `check_number_ledger.py` passes on both manuscripts | 2A 2B D | **DONE 2026-10-17 (machinery gate passed; 15 of 22 curated claims differ, see S8.md)** |

## Compute and storage
- Decode cost: S2 reads 18.8 GB of JPEG frames from the bags (no PNG export; frames are decoded in memory). Output: detections table only.
- Nothing large is written next to the raw data. `outputs/` is on the SSD and not in git; `results/` holds small CSV/JSON that are committed.
- After every stage: commit, then `git bundle` to `/mnt/phd_data/phd_master/04_code_software/bridgedeck-vision-pipeline/` and copy `results/` and a manifest.
