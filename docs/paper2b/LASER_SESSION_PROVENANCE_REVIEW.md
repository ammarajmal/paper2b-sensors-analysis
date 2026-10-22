# Laser session provenance review: `laser_y2024` and `laser_y2025`

**Scope:** which acquisition each label refers to, and how each relates to the 2025 camera bags.
**Method:** campaign identity is not inferred from file or folder names (the audit package states this
rule in `08_PROVENANCE/14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md`, "file-provenance rule"). Dates
come from internal metadata where it exists (ROS bag index, xlsx core properties, raw record lengths)
and from filesystem modification times only as supporting evidence. Raw data were read, never modified.

## 1. Evidence

| # | Observation | Source (exact) | Evidence status |
|---|---|---|---|
| E1 | The 2025 camera bags were recorded on **2025-10-01**. Main bags: e0_0rpm 08:15:13Z to 08:15:43Z; e1_20rpm 08:18:04Z; e20_320rpm 09:13:45Z to 09:14:16Z. 5-second bags: 07:29:06Z (e0) to 07:54:08Z (e20). | Chunk-info records at the end of `/mnt/phd_data/phd_master/03_datasets/ds004_windtunnel_cameras_2025/raw/wtt-main/e{0,1,20}_*/*.bag` and `raw/wtt-5sec/e{0,20}_*/*.bag` (read-only parse of the bag index). | VERIFIED as the ROS recording host clock. Whether that clock was set correctly is not independently verified; the file modification times (2025-10-01 17:18 local for e1) agree with it. This is record time, not exposure time (project rule). |
| E2 | `ds004` `metadata.yaml` says `dates: "2024-11 to 2025-01"`. | `ds004_windtunnel_cameras_2025/metadata.yaml` | CONTRADICTED by E1. Treat as an unverified descriptive field. |
| E3 | The **y2025 laser sweep** (files `D00`..`D20`, 7,200 rows x 3 columns, 20 s at an assumed 360 Hz) was written on **2025-09-21**, 11:40 to 12:32 local time. | `.../TESolution/Video Measurement/laser_displacement/등류/영각00/D00..D20` (file times); sample counts in `docs/gates/S5a.md` (Inputs and RESULT 1) | Dates: SUPPORTING (file system). Sample counts: VERIFIED by the S5a integrity gate. |
| E4 | The y2025 free-vibration records `Bd1` (72,000 rows) and `Td1` were written 2025-09-21 11:04 and 11:09. | `.../laser_displacement/자유진동/Bd1`, `Td1`; row count of `Bd1` read here (72000) | SUPPORTING. |
| E5 | The y2025 setup workbook `설계속도 및 모형Setup_영상계측.xlsx` was last modified **2025-09-21T02:37:48Z** (internal core property); the vendor script `BRID2D1.m` is dated 2025-09-21 (`docs/DECISIONS.md`, owner decisions 2026-10-17, row d). | `.../laser_displacement/모형_setup/설계속도 및 모형Setup_영상계측.xlsx`, `docProps/core.xml` | VERIFIED (internal metadata) for the workbook; the sweep files themselves have no internal timestamp. |
| E6 | The **y2024 laser sweep** (`D0` bias; `D1`..`D38`, 10,800 rows = 30 s) was written **2024-10-22**; the vendor script `BRID2D1_choi.m` on 2024-11-12. | `.../RAW_Data/laser_displacement/2D_WTT/` (39 files dated 2024-10-22, 2 dated 2024-11-12); `docs/gates/S5a.md` Inputs | SUPPORTING (file system). |
| E7 | The y2024 free-vibration records `Bd1` and `Td1` each contain **36,000 rows (100 s at 360 Hz)** and were written 2024-10-17. | `.../RAW_Data/laser_displacement/free_vibration/Bd1`, `Td1` (row counts read here) | VERIFIED (row count); date SUPPORTING. |
| E8 | `Free Vibration Comparison.xlsx` was created 2024-11-07 and modified 2024-11-08 (internal core properties). The `ds003` dataset metadata states `dates: "2024-10 to 2024-11"`. | `.../Video Measurement/Free Vibration Comparison.xlsx`, `docProps/core.xml`; `03_datasets/ds003_windtunnel_ldv_2024/metadata.yaml` | VERIFIED (workbook); `metadata.yaml` descriptive. |
| E9 | The facility natural frequencies **1.4303 Hz** (vertical) and **3.1036 Hz** (torsion) appear on page 3 of a facility photograph/document in the 2024 TESolution material. | `08_PROVENANCE/12_TAG_ID_RECONCILIATION_REPORT.md` line 33; `14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md` line 112 | VERIFIED as quoted in the audit package. The document page itself was not opened here. |
| E10 | Reprocessing from raw (free-decay damped-sinusoid fit, 95% block bootstrap): y2024 bending 1.4298795 Hz [1.4298263, 1.4299322], torsion 3.1034333 Hz [3.1024334, 3.1044247]; y2025 bending 1.4317569 Hz [1.4315950, 1.4319288], torsion 3.0981814 Hz [3.0968951, 3.0993092]. | `results/reference_frequencies_free_vibration.json` fields `f_fit_hz`, `f_fit_lo`, `f_fit_hi` by `session` and `mode`; `docs/gates/S5a.md` RESULT 4 | VERIFIED (reproducible code, tests/test_laser.py). |
| E11 | The y2024 and y2025 sweeps use different RPM lists: y2024 10..310 in steps of 10 (38 conditions); y2025 20, 40, 50, 60, 70, 80, 90, 100, 110, 120, 140..320 (20 conditions), the same list as camera conditions e1..e20. | `docs/gates/S5a.md` Inputs and RESULT 1; `results/laser_y2025_by_condition.csv` column `rpm`; camera conditions in `results/s2c_stream_table_dev.csv` | VERIFIED. The match of the test matrix is design evidence, not proof of simultaneity. |
| E12 | Owner confirmation that the mechanical structural system is the same in 2024 and 2025; marker geometry and measurement operator differ. | `08_PROVENANCE/14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md` ("owner explicitly confirmed", 2026-09-07) | OWNER-CONFIRMED. |
| E13 | Owner decisions: 2026-10-16 "Exact campaign dates omitted from papers"; 2026-10-18 A1 "Laser 2024 DROPPED from papers ... Only camera vs laser 2025"; A3 "Reference frequencies in papers = rebuilt values 1.4318 Hz (bending) 3.0982 Hz (torsion)". | `docs/DECISIONS.md`, owner decision tables dated 2026-10-16 and 2026-10-18 | OWNER DECISIONS (recorded). |
| E14 | No facility acquisition log, test log or timestamped record linking the y2025 laser files to the 2025-10-01 camera session was found. The only tie is the identical RPM test matrix (E11) and a co-mounting photograph (page 2 of the setup document, `12_TAG_ID_RECONCILIATION_REPORT.md` lines 28-31) whose campaign is not labelled. | Searches of `docs/`, the audit package `08_PROVENANCE/`, and the `logs/` folder of `ds004` (contains only `tesolution-2024-tunnel-a/`) | ABSENT. Recorded as an evidence gap, not as a negative finding. |

## 2. Resolution

**R1. `laser_y2024` is the October 2024 laser session.** The raw files are dated 2024-10-22 (sweep) and
2024-10-17 (free vibration), the free-vibration records have exactly 36,000 rows (E7), and the facility
workbook was written in November 2024 (E8). That matches the manuscript's description of the laser
free-vibration record (360 Hz, 100 s, 36,000 samples) and its "approximately eleven months" separation from
the camera bags (2024-10 to 2025-10-01, E1). The manuscript's 2024 laser reference lane is therefore the
y2024 session. Evidence status: file-system dates plus verified record lengths; no facility log.

**R2. `laser_y2025` is a laser session of mid-to-late September 2025, about ten days before the cameras.**
Its files are dated 2025-09-19 to 2025-09-22 (sweep 2025-09-21) and the setup workbook's internal
timestamp is 2025-09-21 (E3-E5). The camera bags were recorded on 2025-10-01 (E1). The two acquisitions are
**not simultaneous and not on the same day**. The y2025 session is therefore **not** "the 2024 campaign" and
**not** a same-session companion of the cameras. Whether it belongs to the same test series as the cameras
(same RPM matrix, E11) is plausible but is not documented (E14).

**R3. Campaign wording that the evidence supports.** "A laser displacement session recorded on the
facility's tunnel about ten days before the camera recordings" for y2025, and "a laser session recorded in
October 2024, about eleven months before the camera recordings" for y2024. The wording "same campaign" or
"concurrent" is not supported for either. Owner decision 2026-10-16 says exact campaign dates are omitted from
the papers. The review therefore recommends the neutral labels *laser session A (2024)* and *laser session B
(2025, shortly before the camera recordings)* in text, with the dates held in the provenance record.

**R4. The statistical layer uses only y2025.** Its inputs are `table_2025_ldv_primary.csv`,
`laser2025_vs_camera_dominant.csv` and `laser_y2025_by_condition.csv` (`EXPLORATORY_SOURCE_HASHES.json`;
`scripts/exploratory_camera_laser_analysis.py` lines 11-13). The per-camera RMS package computes both sessions,
with y2025 as the primary (`PER_CAMERA_RMS_REPORT.md`, "Campaign/session" paragraph).

**R5. The earlier statement "chosen as primary on dataset naming only" is now superseded.** It is replaced by
the owner decision A1 (2026-10-18) together with E3-E5, which are independent of the file names.

## 3. The two fixed reference frequencies

- The manuscript's `f_v = 1.4303 Hz` and `f_t = 3.1036 Hz` are consistent with the **y2024** session. Their
  differences from the raw-reprocessed y2024 fits are 0.00042 Hz (bending; just outside the y2024 fit interval
  [1.4298263, 1.4299322]) and 0.00017 Hz (torsion; inside [3.1024334, 3.1044247]). Both are far below the
  0.033 Hz record resolution used in the manuscript. The differences from the y2025 fits are 0.0015 Hz
  (bending) and 0.0054 Hz (torsion), both outside the y2025 fit intervals. The values therefore match the 2024
  session better than the 2025 session. The review did not find the facility's own derivation, so `f_v` and `f_t`
  stay "facility-reported values, consistent with raw reprocessing of the 2024 session" (E9, E10).
- Decision A3 (2026-10-18) names **1.4318 Hz and 3.0982 Hz** (y2025) as the reference values "in papers". The
  Paper 2B manuscript (September 2026 lineage) has not been updated to this and its frozen post-hoc comparison
  (Table 4, 33/60 and 17/60) uses the 2024 values. A3 and A1 as written conflict with the current manuscript.
  **This is an owner decision that the evidence cannot make.** See `UPDATED_MANUSCRIPT_INTEGRATION_OPEN_ITEMS.md`,
  OD-1.

## 4. Consequences for the integration text

1. The statistical frequency and RMS results are comparisons with the **y2025 laser session** and must say so
   in the Methods wording, not "the 2024 laser campaign".
2. The previously proposed text that says "report both sessions" is withdrawn for the main text. Under A1 only
   y2025 is used; y2024 results stay internal.
3. The statement "the only external reference values used anywhere in this study" cannot stand if per-condition
   y2025 laser targets are introduced. See `ESTIMAND_SCOPE_DECISION.md`.

## 5. Residual uncertainty

File-system and index dates could be wrong if clocks were mis-set or files were re-saved; the internal
workbook properties (E5, E8) and the bag index (E1) are the strongest items. No document states the
acquisition days directly. If the facility can supply its test log, E14 would close.
