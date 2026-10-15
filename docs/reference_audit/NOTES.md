# Reference-code audit notes (2026-10-16)

Purpose: record what the older code and reports did, so the new pipeline reuses what is sound and avoids repeating known problems.
Nothing in the reference trees was modified or run. Evidence levels: **READ** (I read the text), **SKIMMED** (headings, docstrings, head of file),
**INVENTORIED** (automated extraction only: `inv_*.csv`), **NOT LOOKED AT**. Scientific numbers quoted here are what the cited document states; I did not recompute them.

## 0. Coverage
| Tree | Files / lines (inventory) | Level |
|---|---|---|
| `structural_vision_research` (SVR) evidence reports S04.04, S05.01-03, S06.2, S06.3 (6a), S07.2 (1-3), S09.1 (3-4), S09.2 (item 7), S12.1 | 101 code files, 19k lines | READ in part (sections named); S06.1, S08.x, S10, S11, FINAL_NUMBER_LEDGER (68 kB) NOT READ |
| `omrpr_analysis` (clean-room package) | 169 files incl. 76 duplicated under `.claude/worktrees` | SKIMMED: `background_compensation.py` head, `per_camera_frequency_recovery.py` head and its report, `refine_intrinsics_laser.py` head. Other modules INVENTORIED |
| `omrpr_fin/src` steps 00-12 | 29 files, 9.6k lines | Read by an earlier session (see `REDESIGN_2026-10-15.md`); INVENTORIED here |
| `shm-displacement-project/scripts` (static, dynamic, paper2, hybrid) | 109 files, 48k lines | INVENTORIED; hybrid plan README and Step 09 plan SKIMMED |
| `P00/docs` laser unit/mapping audit | 1 file | READ |
| `shm-displacement-project/offline_processing`, `p03_windtunnel_bridgedeck`, vendor `tesol_ws`, vendor MATLAB | 18 / 69 / 81 / 72 files | INVENTORIED only |

## 1. What was already done, by lineage
**A. Clean-room line (SVR + `omrpr_analysis`, Jul-Sep 2026, study OMRPR-NS-001).** Most careful lineage; every checkpoint has a markdown report, a script and a "status: candidate / owner approval" label.
- Official AprilRobotics v3.4.5 detections for all 63 camera streams (115,276 rows; frozen CSV SHA-256 `e7be189e…4024a9`). Detector settings: tag36h11, `threads=1, maxhamming=0, decimate=1.0, blur=0.0, refine_edges=True`.
- Observation gates: expected tag ID, Hamming 0, decision margin >= 30, finite in-image corners, one-sided 95% Wilson lower bound on completeness >= 0.95; candidate velocity gate 27.75 px/frame (midpoint between the clean maximum 21.27 px/frame at e14 cam1 and the first failure burst 34.23 px/frame at e20 cam1). Result: 60 streams admissible, 2 rejected (e20 cam1/cam2), 1 diagnostic-only (e20 cam3). All thresholds are labelled candidate, unsigned.
- S04.04 validation: static invariance at e0 (RMS 0.021-0.027 px in x, 0.047-0.090 px in y; tag side length stable to 0.03 px); synthetic translation test (672 trials, recovery RMS 0.0015 px); detector determinism (300/300 bit-identical). Known-perturbation truth does not exist for this free-response facility.
- Task 3 (`per_camera_frequency_recovery.py`, 2026-09-02): each camera alone, PCA of raw pixel centroid, Welch over the full record (0.033 Hz resolution), Lomb-Scargle for the gapped e20 streams. Over 19 conditions x 3 cameras: median error to the facility frequencies 1.59% (bending) and 1.59% (torsion band). **This is the same idea as Paper 2A.** Files `task3b_cross_camera_phase_coherence.csv` and `task4_gap_bridging_benchmark.csv` exist but their reports were not found.
- S06.2 spectra: strict timestamp matching, no interpolation, segment 64 samples = 0.94 Hz bins. S06.3 found a 0.937 Hz "mode" that was the first non-DC bin of that grid (resolution artifact), corrected on 2026-09-01.
- S07.2 laser lane rebuilt from raw D-files: bias run D0, calibration `(data - bias) * 2.7`, centimetre-to-millimetre factor 10, torsion = (ch1 - ch0) * 2.0.
- S09.1: cam1 and cam2 are not interchangeable: cam1-only changes bending RMS by 1.30x-1.95x, cam2-only by 0.13x-0.95x relative to the equal-weight operator. cam1's default is the raw track, cam2's the background-compensated one.
- S09.2 uncertainty budget: timing and missingness, static noise, detection variability and spectral CI are quantified; calibration/operator envelope (0.85-1.03x for calibration, 1.26x-55.5x for axis/operator) and the between-campaign confounding are NOT combinable into one number.
- S12.1: a third instrument was found, the vendor's own 3-camera fiducial tracker for the 2024 session (`D0.csv`-`D37.csv`, Unix-epoch timestamps, irregular dt, CV 0.16-0.9). Its dominant bending peak at 60/70/80 RPM is 1.40-1.47 Hz at 0.067 Hz resolution.
- Intrinsics: SVR says no camera calibration is verified. `refine_intrinsics_laser.py` fits fx, fy, cx, cy against laser agreement (a "provisional" step 02b).

**B. Measurement-paper line (`omrpr_fin`, Jun-Jul 2026).** Steps 00-12, config intrinsics identical to the bags' `camera_info` (cam1 fx 20327.9, cam2 25749.5, cam3 25630.9), "locked" numbers, Option B (2024 laser primary, dp = 2.0). Known gaps recorded earlier: step 05 gap guard never implemented, no `step02b` file, stale comparison figures.

**C. Hybrid-framework line (`shm-displacement-project/scripts/paper2`, Apr-Jun 2026).** About 40 audit scripts and phases 01-09 (replay export, B0 baseline, Marker A reliability, AprilTag quality score, synthetic corruption benchmark, B1 RTS, B2 KLT fallback with retune, ROI optical flow). Plan says B0 is the publication baseline and B1-B4 claims are not validated. Phases 10-18 have plans but no scripts. Outputs: `data/results/paper2` (hybrid_framework 11 GB in P00; more in the newer `github` copy).

**D. Early lineage (Plans A/B/C, static tests, Sep-Oct 2025).** `ds005` static scripts, `phaseB_detection` (6.1 GB per-condition detections, May 2026), `time_analysis_results`.

## 2. Findings that change the new pipeline
| # | Finding | Evidence | Consequence |
|---|---|---|---|
| F1 | Marker labels are reversed in SVR: cam1/cam2 = "documented_center_marker", cam3 = "documented_side_marker". The owner confirmed the opposite on 2026-10-15 (cam1/cam2 = offset marker ID-0-1, cam3 = near-axis marker ID-0-2). | S05.01 table header; S06.1 operator names | Do not port S06.1 operator definitions or the Marker A/B names. Re-derive from the owner map. |
| F2 | The "stationary background" compensation (ECC affine, marker region masked by 20 px) may not have a stationary background to use. A stationary-feature check on e7 found every trackable feature in cam1/cam2 moves with the tag (corr > 0.99), and all features sit on the deck/clamp. | `background_compensation.py` docstring vs the `STATIONARY_FEATURE_CHECK_RESULTS.md` of 2026-10-13 | Hypothesis (untested): compensation either does nothing or removes real model motion. S2b must compare raw vs compensated amplitude at e7/e14 before any port. S05.01 already found compensation raises cam1 static RMS and cam3 drift (0.62/-0.66 px per 1000 frames). |
| F3 | Two incompatible 2024 laser file mappings exist: `actual Dn -> workbook D(n+1)` (P00 audit; 18 workbook rows excluded) vs direct `Dn -> Dn` (SVR rebuild). | `P00/docs/paper2_ldv_unit_and_mapping_audit.md`; S07.2 section 1 | The laser stage must test both against physical evidence (monotone RMS with wind speed, lock-in frequencies, pre-specified camera-frequency matching) and record the winner. |
| F4 | Laser units: raw values are centimetres; legacy columns labelled `_mm` may be unconverted. | P00 unit audit; S07.2 section 3 (x10, with a regression on D38: torsion RMS 17.08 mm +/- 0.05) | Add a unit test and name columns `*_native_cm`/`*_mm` explicitly. Check what Table S2 of the Measurement paper used. |
| F5 | Spectral resolution was a processing choice: 64-sample Welch gave 0.94 Hz bins and a spurious "mode". | S06.3 6a/7; Task 3 report | Use full-record estimators (about 0.033 Hz). Never report peak frequencies from short segments. |
| F6 | `refine_intrinsics_laser.py` tunes intrinsics to laser agreement. | script docstring | **Not ported.** Owner rule 2026-10-16: intrinsics come from the bags' `camera_info` and are never adjusted by laser agreement. |
| F7 | A vendor 3-camera system recorded in the **same 2024 session** as the 2024 laser (`RAW_Data/3D_video_system/2D_WTT/D*.csv`, 43 files). Nobody has joined it to the laser at sample level; the vendor script only computes mean/RMS/peak. | S12.1 | Candidate new analysis: vendor camera vs laser within one session separates "session" from "camera type" effects. Needs the time-column provenance checked first (Unix epoch, irregular). |
| F8 | `github/shm-displacement-project` is not a copy of `P00_shm-displacement-project`. A size-only comparison listed 79,201 files present only in `github` (78,944 under `data/results/paper2`) and 9 files with different sizes (CLAUDE.md, README.md, project_manager.md, memory notes). The reverse direction (files only in P00) was not checked. | rsync dry-run 2026-10-16 | `github` is the newer, larger one. Treat P00 as an older snapshot. Do not delete either. |
| F9 | The SVR rule "never validate against laser / no causal inference" was written for an 11-month gap. The 2025 laser session is about one month from the camera session. | CLAUDE.md of SVR; laser Sept 2025 and camera Oct 2025 per the earlier 2025-laser analysis (not re-checked here) | Keep the non-simultaneity rule, update the gap in the notes. |
| F10 | The detector binding differs: SVR/omrpr_analysis use the official `apriltag` module (v3.4.5, commit prefix 94be783). The new repo currently ships `pupil-apriltags` (bundled C library, version not verified). | `03_install_official_apriltag.sh`; pyproject | S2 gate decides. Plan: build the official v3.4.5 binding for the gate; keep pupil as a second implementation to cross-check (the SVR notes that both gave the same 61% detection at e20). |
| F11 | Facility anonymisation rule: no manuscript text, caption or ledger label may name the facility. Folder names in this repo's config do. | S04.04 note; `paper2_facility_anonymization_note.md` | Ledger and figure labels use `laser_2024`/`laser_2025`. `config/paths.yaml` is never uploaded. |
| F12 | Acquisition and number-ledger tooling worth keeping: `check_number_ledger.py` (pre-commit gate blocking manuscript numbers not in the ledger), `build_dataset_identity_manifest.py` (hashes the bags). | inventory | Port in stage S3/S7. |

## 3. Reuse verdict
| Item | Verdict |
|---|---|
| Frozen detections CSV | Gate target for stage S2 |
| Gates (Hamming, margin, Wilson, velocity) | Reuse the definitions; re-derive thresholds from the new data and pre-register; the old ones are unsigned candidates |
| Static invariance, synthetic-shift and determinism tests | Port as unit tests of the detector stage |
| Task 3 per-camera frequency recovery | Port as the baseline for Paper 2A; extend with false-alarm probability and the native-vs-resampled comparison |
| Timestamp matching rule (nearest, one-to-one, tolerance 0.75 dt, gap 1.5 dt, no interpolation) | Reuse for any cross-camera pairing |
| S09.2 budget structure (items 1-7) | Reuse as the skeleton of the uncertainty stage |
| Background compensation | Do not port until F2 is tested |
| Intrinsics refinement | Do not port (F6) |
| Marker operators (bending/torsion proxy) | Do not port (F1, F3 of S09.1); replace by heave/pitch from the owner marker map |
| Hybrid B1-B4 (RTS, KLT, ROI flow) | Out of scope for the papers; keep as dissertation outlook |
| `omrpr_fin` steps | Numeric cross-check only |
