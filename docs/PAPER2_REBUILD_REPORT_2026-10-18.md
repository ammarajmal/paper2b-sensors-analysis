# Paper 2 rebuild: full progress report (2026-10-15 to 2026-10-18)
Written for the author (Ammar). Everything here is recorded in the repository `bridgedeck-vision-pipeline` (code, gate files in `docs/gates/`, results in `results/`, decisions in `docs/DECISIONS.md`). Mirror: `/mnt/phd_data/phd_master/04_code_software/bridgedeck-vision-pipeline/`. Numbers below are copied from the gate files or result tables; where a statement is my interpretation it says so.

## 1. What was done and why
Goal: make every number in Paper 2A (Sensors, spectral) and Paper 2B (Measurement, camera versus laser) reproducible from the raw rosbags and laser files, in a gated code base, while reviewing the manuscripts. Method: **gate first** (the pass criteria are written and committed before a stage runs), so a failed gate is a finding, not something to hide.
Scope decision of 2026-10-18 (yours): the papers use **camera versus the 2025 laser only**. The 2024 laser is out of the papers; its results stay in the repository as internal audit material. Rebuilt values replace earlier printed values. No laser-to-laser and no printed-versus-rebuilt comparison goes into the papers.

## 2. Pipeline and results by stage
| Stage | What | Result (from the gate file) |
|---|---|---|
| S1 | Frame-timing census, 42 wind-tunnel bags, 126 streams | Matches the earlier extraction (0 mismatches). Median rates 59.941 (cam1), 59.940 (cam2), 60.000 Hz (cam3). Duplicate frames only in cam3 (40 over 21 bags). Largest gaps 24.7 / 26.0 / 31.7 ms |
| S1b | 20 static bags | Recompute identical to the committed table. Under definitions fixed afterwards: 4 clean, 7 below 55 Hz, 12 with missing sequence numbers (plan said 5 / 7 / 8; the earlier definitions were never recorded) |
| S2a | Official AprilTag v3.4.5 built (owner decision O5) | Settings: tag36h11, threads 1, maxhamming 0, decimate 1, blur 0, refine_edges True |
| S2 | Detection in all 115,276 frames | Same detected flag as the frozen detections in 100% of frames; corner differences about 5e-7 px |
| S2c | Four candidate rules for admitting a stream (O4) | R1 physics (tag side/10 = 29.07 px/frame) agrees with the ledger on 62 of 63 streams; R3 logistic 5% point 31.6 px/frame; R4 (margin outlier) does not work (Spearman 0.008). Evidence rests on one failing condition (320 RPM), so no data-derived threshold has a trustworthy interval |
| S2b | Does the reference code's background (ECC) compensation help? | **No.** It lowers static RMS on all three cameras but removes 96-99% of the 90 RPM line (cam1 99.5%, cam2 96.9%, cam3 96.2%) and changes the 200 RPM amplitude by -46% / -13% / +17%. The "background" moves with the model. Not adopted |
| S3 | Per-camera spectra on native timestamps | Published peaks reproduced exactly in 60 of 60 streams; generalised Lomb-Scargle agrees in 61 of 61; 23 of 60 dominant peaks within one resolution bin of f_h or f_alpha (about 0.8 expected by chance) |
| S3b | Timebase shifts on refined frequencies | Interpolation to uniform 60 or 59.94 Hz moves peaks by at most 0.05 Rayleigh intervals; ignoring timestamps up to 1.48. The published table values do not reproduce (about half as large), cause not found |
| S4 / S4b | Pose and rectification | PnP rotation channels are unreliable (IPPE two-solution ambiguity: median ambiguous share 0.88 cam1, 0.24 cam2, 0.57 cam3). In-plane heave and in-plane roll (pitch) are used. Estimator variants agree to 0.1% |
| S5a | Laser reprocessing | Units are cm (x10 for mm). 2025 vendor torsion column is exactly half the correct value (the script overwrites the bending channel first): never use it. Free-decay frequencies 2025: 1.4318 Hz bending, 3.0982 Hz torsion (paper's 3.0827 does not reproduce) |
| S6 | Camera versus laser, all 19 conditions (20-300 RPM) | 2025 laser: heave log-correlation 0.844, typical ratio error E = 0.445, median ratio 0.82; pitch log-correlation 0.942, E = 0.387, median ratio 1.14. The pre-written test for dropping the other laser was not met (moot now) |
| S6b | Exploratory tag-size and spacing variants | Tag size and head spacing cannot explain the disagreement (E changes by at most 0.02). Variants are fitted to the laser and prove nothing |
| S7 | GUM uncertainty budget (relative standard uncertainty, rule-a conditions) | Heave: camera 0.14, laser 0.18, combined 0.24. Pitch: camera 0.23, laser 0.10, combined 0.28-0.30. Largest terms: within-record stationarity, head spacing (0.087 on pitch), tag scale (0.014) |
| S7b | Monte Carlo and consistency tests | Random noise is tiny (0.01-1% in amplitude; laser pitch 9% from the spacing). Intrinsics: zero distortion or fx, fy +/-5% change amplitude by at most 0.03%. Birge ratios 5-32 (an adequate budget gives about 1): the budget explains the disagreement poorly. cam1 versus cam2 on the same marker: median difference 0.35% (heave). Passing-Bablok slope 0.96-1.0 |
| S8 / S8b | Number ledger and manuscript number check | Ledger 5,031 rows, each with source file, recipe, script, commit and hash; independent stdlib recompute: 0 differences. 605 table cells compared with the printed ones: about 60% equal or within 3 last-digit units (195 of 322 Measurement, 177 of 283 Sensors), the rest differ (mostly 2-7%). Printed intervals use an unstated bootstrap |
| S9 | Outlier analysis (camera-internal flags only, the laser was not used to find them) | No camera defect in the interior regime. Fix candidates (Huber, frame rejection, windowed median, fusion): none improves camera-internal repeatability; robust fits remove real motion. **No fix adopted** (a windowed median helped agreement with one laser, but it was chosen by its outcome against the reference and worsened camera repeatability) |
| S10 | Session-difference evidence | Onset RPM identical in all instruments, so an RPM shift cannot align them. The 2025 wind column (about half the other session's) cannot be reconciled and could not be verified (owner could not find the calibration) |
| S11 / S11b | Raw spectra of 9 conditions (20, 40, 60, 80, 110, 140, 260, 280, 300 RPM), camera versus 2025 laser | **No instrument fault.** 60 and 80 RPM: different lock-in states in the two sessions (laser heave lock-in at 60, camera heave lock-in at 80). 20 and 40 RPM: laser at its floor. 110 RPM and 140 heave: small line next to a larger line. 260-300 RPM: broadband and non-stationary, both instruments see the same lines. 140 RPM pitch agrees within 0.7% |

## 3. Main findings (for the story)
1. The pipeline is reproducible end to end from the raw data, with a number ledger. Published peak frequencies are reproduced exactly; several printed magnitudes shift by 2-7% under the rebuild.
2. The camera is internally consistent: three cameras agree to under 1% on the same quantity; random noise, intrinsics and tag scale are negligible next to the camera-laser differences.
3. Camera-laser agreement is strong where a narrow-band lock-in dominates the variance (140 RPM pitch within 0.7%) and weak where the response is small, broadband, or in a different regime in the two sessions. The disagreements are properties of the conditions, not camera defects.
4. The uncertainty budget leaves a large unexplained component (Birge 5-32). It points to a session effect (non-simultaneous recordings, unverified wind), not to the camera.
5. The reference code's background compensation removes real motion. Do not use it.
6. Unsynchronised, host-timestamped cameras can be analysed per camera on native timestamps; timestamp treatment matters little (<= 0.05 interval) except when timestamps are ignored.

## 4. Decisions register (see docs/DECISIONS.md for the full text)
O1 2025 laser only (2024 dropped 2026-10-18). O2 regime rule: all four candidate rules kept, rule a (both instruments above 5x their own floor) adopted for the closeness decision as an amendment, stated as such. O3 bending/torsion definitions: recommendation heave/pitch line amplitudes primary, legacy proxy as sensitivity (your choice pending). O4 threshold: R1 physics primary (pending). O5 latest AprilTag. D6 reference frequencies 1.4318 / 3.0982 Hz. T tag 20 mm (assumption, +/-2.5%). d head spacing 13 cm (+/-15%). N rebuilt numbers throughout. W proceed at equal RPM without the 2025 wind calibration. A1, B1-B3, C1-C2 scope and order of work.

## 5. Mistakes and corrections made on the way (so you can trust the record)
- I first checked the static census against the committed file itself (proves nothing); redone against a fresh recompute.
- A wrong camera-name selector silently produced zeros in the ledger; the builder now fails on any empty selection.
- Background jobs died several times (two caused by `pkill -f` matching my own shell; the S2b parallel runs oversubscribed the CPU, load 278). S2b was finished by a sequential run. For S2b I did not repeat the full run, so the "two identical runs" check was not done.
- I wrote the 13 cm / workbook details into the decision file before reading them; they turned out right, but the order was wrong. Fixed and noted.
- The stage plan numbers 5/7/8 for the static bags were not reproduced: the original definitions are unknown.

## 6. Still open
Owner: O3 and O4 final choice; kit decisions D4 (keep and flag), D5 (timing study as dissertation chapter, recommended), D7, D8 (AI-use statement, check journal wording); ruler graduation, tag size and head spacing remain assumptions (cannot be confirmed). Analysis: Monte Carlo covers in-plane estimators only; variance-share criterion for reporting a ratio as agreement is proposed, not written; marker-to-side-sensor comparison would need its own gate. Literature: leads are excerpt-level and unverified; novelty not established. Backup: `phd_data` is a single copy until the NAS exists.

## 7. Where things are
Code `src/bridgedeck/`, runners `scripts/run_*.py`, gates `docs/gates/S*.md`, results `results/`, ledger `results/ledger.csv` (recipe per row), claims map `results/claims_map.csv`, table map `results/table_map.csv`, figures `results/figures/`. Reproduce a stage: `uv run python scripts/run_sX.py` (inputs in `config/paths.yaml`; bags are large and the full detection took hours). Verify: `uv run python scripts/check_number_ledger.py` and `scripts/check_tables.py`.
