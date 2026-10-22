# Estimand scope decision: reference frequencies, laser targets, pooled RMS, per-camera RMS

**Purpose:** separate four quantities that the integration text had treated as one "statistical layer", and
decide what each may do in the manuscript. Companion files: `DOMAIN_RECONCILIATION.csv`,
`LASER_SESSION_PROVENANCE_REVIEW.md`, `PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md`.
No manuscript, supplement or submission file was edited.

## 1. The four constructs

| Construct | What it is | Unit and domain | Source (exact) | Evidence status |
|---|---|---|---|---|
| **A. Fixed reference frequencies** | Two numbers, `f_v = 1.4303 Hz`, `f_t = 3.1036 Hz`, applied to every condition after the reference-blind freeze | Hz; all 60 admitted streams (DM01) | Manuscript tex lines 447-452 (Section 2.4 opening), Table `tab:tb4-posthoc-reference` lines 1094-1137; facility values per `08_PROVENANCE/12_TAG_ID_RECONCILIATION_REPORT.md` line 33 | Consistent with the y2024 session (LASER_SESSION_PROVENANCE_REVIEW.md section 3). Frozen and audited in the manuscript lineage. |
| **B. Per-condition laser targets** | For each RPM, the dominant bending and torsion frequency of the y2025 sweep file; the camera peak is the nearest of the stream's five retained peaks | Hz; 19 non-320 conditions (DM06) | `/mnt/phd_data/phd_master/05_publications/p02_audit_2026-10/analysis_2026-10-15/laser2025_vs_camera_dominant.csv` columns `laser_bend_dom_hz`, `laser_tors_dom_hz`; `scripts/exploratory_camera_laser_analysis.py` lines 24-31; `analysis/paper2b/statistical/FREQUENCY_CORRESPONDENCE_RESULTS.csv` | Exploratory ("EXPLORATORY ONLY NOT MANUSCRIPT-AUTHORIZED", `EXPLORATORY_CAMERA_LASER_ACCURACY_MODAL_REPORT.md`). Laser session recorded about ten days before the cameras. |
| **C. Pooled RMS** | Legacy published table: `cam_bend = ((y1+y2)/2 + y3)/2`, `cam_tors = y3 - (y1+y2)/2` on cam3 time stamps, against laser bending/torsion RMS | mm; 20 rows including 320 RPM (DM05) | `table_2025_ldv_primary.csv`; `PER_CAMERA_RMS_DEFINITION_LEDGER.csv` rows 11 and 12 | NOT-CURRENT-LINEAGE (ledger row 12: "produced by an earlier pipeline; cannot be inverted to per-camera values"); exploratory. |
| **D. Per-camera RMS** | RMS of H1,y (mm) and H2 roll (rad) per stream, from rectified tag corners, with a noise-floor ratio | mm and rad; 61 pose streams (DM07), comparisons on 19 conditions (DM08) | `analysis/paper2b/per_camera_rms/PER_CAMERA_RMS_VALUES.csv`, `PER_CAMERA_RMS_COMPARISON.csv`, `PER_CAMERA_RMS_DEFINITION_LEDGER.csv` rows 2-4, 14-21 | VERIFIED (20/20 validation checks, `PER_CAMERA_RMS_VALIDATION.md`; deterministic rerun). The ±2.5% mm scale bound is PROVISIONAL (ledger rows 13, 20). |

The statistical frequency, repeatability and cam3 observation-path results use construct B (frequency) and
pixel or relative RMS from the stream tables. The statistical `RMS_SCALING_RESULTS.csv` uses construct C.
The per-camera RMS package is construct D. Constructs B and C share the y2025 laser session.

## 2. Decisions

**ED-01. Construct A stays the only external reference in the main-text Methods lane.** The manuscript's
sentence that these are "the only external reference values used anywhere in this study" (tex lines 451-452)
remains true if constructs B to D stay out of the main text. The decision of which numbers A holds (2024
facility values or the A3 rebuilt 2025 values) is an owner decision (OD-1 in the updated open items). Do not
mix: if A3 is adopted, Table 4 and the 33/60 and 17/60 counts must be recomputed by script as one change.
*Status:* DECIDED conditional on OD-1.

**ED-02. Construct B (per-condition laser targets) goes to the Supplement as exploratory, post-hoc,
cross-session correspondence, not to the main Results.** Reasons: (i) it is labelled not manuscript-authorized
at source; (ii) it needs a new reference lane (the y2025 sweep) that the Methods and Figure 1 do not describe;
(iii) the laser session is not the one described in the manuscript (LASER_SESSION_PROVENANCE_REVIEW.md R1, R2);
(iv) decision A1 drops 2024 and keeps y2025, which cannot be reconciled with the manuscript's 2024 lane without
the owner. If it is kept, the supplement text must call it "laser session B (2025, about ten days before the
camera recordings)" and the main text needs one pointer sentence only. The matching rule (nearest of five
retained peaks) is the same rule that Table 4 uses for construct A, so the two are comparable in method.
*Status:* DECIDED (Supplement only), pending OD-2 on whether to include B at all.

**ED-03. Construct C (pooled RMS) is withdrawn from the manuscript and the Supplement as a result.**
Reasons, each from the source rows above:
1. It combines the three cameras, which the manuscript forbids at every stage ("No analysis anywhere in this
   study performs cross-camera pixel averaging or cross-camera pixel subtraction", tex lines 316-320; Section 3.3
   "not a fused measurement", lines 700-703). Its torsion value is a cross-marker difference (cam3 minus the
   cam1/cam2 mean), i.e. the reconstruction of a torsion-like quantity that the manuscript says is never formed
   (tex line 320).
2. It includes the 320 RPM condition (row `rpm=320`, flag `DCG-excl`) although the manuscript excludes that
   condition because two of its three streams are rejected (tex lines 279-298). The `full_20` rows of
   `RMS_SCALING_RESULTS.csv` therefore cannot be called an admitted-set result.
3. The file is dated 2026-10-09, comes from an earlier pipeline, and "cannot be inverted to per-camera values"
   (ledger row 12). The per-camera package does not read it (`PER_CAMERA_RMS_VALIDATION.md`, verdict 3).
4. Pearson 0.9020313613196937 and the other `RMS_SCALING_RESULTS.csv` values are therefore descriptive
   properties of an exploratory, non-current table, not response-trend evidence for the cameras.
Consequence: the "pooled RMS response-trend" subsection, supplement item S15 and statistical figures 02, 03
and 10 in the earlier proposed text are withdrawn. The files stay in the repository as audit material.
*Status:* DECIDED.

**ED-04. Construct D (per-camera RMS) is a bounded Supplement analysis.** See
`PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md`. *Status:* DECIDED (Supplement only), pending OD-3 on the
Methods exception wording.

**ED-05. Terminology.** Use: "reference frequencies" only for A; "per-condition laser dominant frequency" for B;
"per-camera RMS" for D. Never write "pooled" without the definition in row C. "LDS" (not "LDV") stays the
instrument abbreviation, as the manuscript defines (tex lines 203-207); the repository files `table_2025_ldv_*`
and dataset `ds003_windtunnel_ldv_2024` carry the legacy label.

## 3. What each construct may support

| Claim | A | B | C | D |
|---|---|---|---|---|
| Operational frequency correspondence (post-hoc) | yes (existing Table 4) | Supplement, exploratory | no | no |
| Response-trend correspondence | no | no | withdrawn | Supplement, bounded |
| Accuracy, calibration, simultaneous validation, ground truth | no | no | no | no |
| Cam1/cam2 repeatability | no | no | no | yes (same marker; RMS magnitude only) |
| Cam3 observation-path dependence | no | no | no | yes (confounded; not mode) |

## 4. Evidence still missing

- The facility derivation of 1.4303 Hz and 3.1036 Hz (only the quoted page is cited).
- The tie between the y2025 laser files and the 2025-10-01 camera session (no test log; LASER_SESSION_PROVENANCE_REVIEW.md E14).
- The definition of the cam3 "relative RMS" unit in `STATISTICAL_COMPARISONS.csv` (observation_path_dependence): the
  column is a ratio, so units cancel, but the source stream table (pixel or mm) is not stated in the file. Check
  `analysis/paper2b/statistical/run_statistical_analysis.py` before quoting it.
