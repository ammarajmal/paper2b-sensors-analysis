# Decision: where does metric per-camera RMS belong in the Paper 2B manuscript?

**Decision: Option B, Supplement only.** The main manuscript keeps its image-plane spectral identity. The
per-camera metric RMS (H1,y in mm, H2 roll in rad) is a bounded supporting analysis delivered as supplement
items, with a one-sentence scope exception. No manuscript, supplement or submission file was edited.

## 1. Options considered

| Option | What it means | Verdict |
|---|---|---|
| A. Exclude entirely | Keep the package in the repository only | Rejected as the default: the package is validated and answers the reviewer question "what do the cameras report in amplitude?" without any claim of accuracy. Remains the fallback if the owner will not accept the Methods exception below. |
| **B. Supplement only** | Per-camera RMS tables, noise-floor ratios and the cam1/cam2 and cam3 ratios as supplement items; one scope sentence | **Chosen.** |
| C. Secondary Results subsection plus Methods expansion | Pose estimation, intrinsics, tag size and scale uncertainty described in Methods; RMS in Results | Rejected: it would contradict seven existing statements (section 3) and require unverified inputs to be declared (section 4). |

## 2. Reasons for B, each with its source

1. **The package is reproducible and bounded.** 20/20 validation checks pass; source Parquet hash
   `9378c6ea75ec1793ecd1cd183362b795cbe55c75ac57ebcac6a60f291ba3c612`; RMS parity with the earlier stream table within 4.441e-16;
   10,000 bootstrap resamples, seed 0; deterministic rerun (`PER_CAMERA_RMS_VALIDATION.md` section 1, verdicts
   1-7; `PER_CAMERA_RMS_RUNTIME.txt`). Evidence status: VERIFIED.
2. **It rests on inputs the manuscript says it does not use.** H1,y and H2 come from rectifying the four tag
   corners through a per-stream tag-plane homography with the bag `camera_info` intrinsics and a 20 mm tag
   side (`PER_CAMERA_RMS_DEFINITION_LEDGER.csv` rows 2, 3, 13). The scale `mm_per_px` carries a PROVISIONAL
   ±2.5% bound because the ruler graduation (5 mm) is unconfirmed (ledger rows 13, 20; `docs/DECISIONS.md`
   2026-10-17 "T"). The manuscript says the archived intrinsics are "unverified" and "no intrinsic value from
   them is used or quoted anywhere in this paper" (tex lines 228-232).
3. **The amplitude content is outside the paper's question.** The paper's three contributions are per-camera
   spectral features, cam1/cam2 agreement and cam3 differences (tex lines 137-148). RMS is a different
   estimand (full-band to about 30 Hz, noise included; ledger row 4).
4. **A supplement can carry it with an explicit exception.** The same pattern is already used in the
   manuscript for material that is reported "in the Supplementary Material and appears nowhere in Section 3"
   (tex lines 513-516).

## 3. Manuscript statements the exception must cover

| Location (paper2_sensors_synthesis.tex, audit-package copy) | Statement | Treatment under B |
|---|---|---|
| lines 133-135 | physical metric displacement reconstruction "is not required for this frequency analysis" | Still true for the main analysis; add "(a supplementary RMS analysis uses a metric reconstruction)" |
| lines 228-232 | no intrinsic value from the archived calibration is used or quoted anywhere in this paper | Needs one clause: the supplementary RMS analysis uses the intrinsics stored in the bag `camera_info` (`docs/DECISIONS.md` 2026-10-16: identical to `omrpr_fin` config), not the archived calibration files |
| lines 319-320 | no cross-camera composite is formed and no torsion angle is reconstructed | Still true for per-camera RMS (no cross-camera composite). The H2 roll is an in-plane rotation of one tag in one camera, not a torsion angle; state this |
| lines 333-335 | "no PnP or world-frame reconstruction is applied to the primary observable" | True for the primary observable; the supplement uses a homography rectification, not world-frame reconstruction. State this |
| lines 1301-1309 | no common metric coordinate system or cross-camera physical amplitude is reconstructed | Still true; per-camera values are never compared as a common-unit amplitude except as labelled ratios |
| lines 190-193, 254-258, 696-698, 797-799 | cam1/cam2 view the center/near-center marker; cam3 views the off-center/side marker | REVERSED relative to the owner decision (section 5): replace with side/off-center (cam1/cam2, ID-0-1) and centre (cam3, ID-0-2) |
| line 1302 | "magnitude of the 2025 center-to-side marker offset was not physically surveyed" | The ~125 mm lever arm is a descriptive approximation (`PER_CAMERA_RMS_GO_NO_GO.md` condition 4), not a survey; label it so |

## 4. Content allowed in the supplement under B

- Per-stream RMS tables for the 61 pose streams (DM07), with `admissibility` and `flags` columns, and the e0
  noise-floor ratios (`PER_CAMERA_RMS_VALUES.csv`).
- Cam1 vs cam2 same-marker ratios and cam3 vs cam1/cam2 ratios (`PER_CAMERA_RMS_COMPARISON.csv`, stage `full`
  then `sensitivity`), labelled RMS magnitude only, no phase.
- Cam1/cam2 H1,y labelled "vertical metric motion of the side/off-center marker (handwritten label ID-0-1),
  including a lever-arm x roll term; not direct heave".
  Cam3 labelled "centre marker (handwritten label ID-0-2); heave proxy with geometry and bandwidth limits; any
  near-axis statement is data-derived and unsurveyed".
- A cam3-vs-laser comparison only against laser session B (y2025) and only if the owner keeps construct B
  (ESTIMAND_SCOPE_DECISION.md ED-02); the y2024 comparison stays internal (decision A1).
- The ±2.5% bound on mm quantities, none on rad quantities.

Not allowed in either main text or supplement: calibration, accuracy, equality-of-amplitude, "heave" for
cam1/cam2, any combination of cameras, the pooled table (ED-03), a torsion angle.

## 5. Marker labels (resolved by owner decision)

Owner decision (confirmed 2026-10-22; consistent with `docs/DECISIONS.md` 2026-10-15): cam1 and cam2 view the same
side / off-center marker (handwritten label ID-0-1); cam3 views a distinct centre marker (handwritten label
ID-0-2). Both decode as AprilTag ID 0, so the machine ID alone does not distinguish them, and the exact physical
separation was not surveyed. The manuscript says the opposite (cam1/cam2 the center/near-center marker, cam3 the
off-center/side marker), and so does the audit-package provenance report
(`14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md` lines 23-27); both are superseded and the text must be changed
when manuscript edits begin (`MARKER_IDENTITY_RECONCILIATION.md`; OD-4 closed). Pure spectral statements in the
manuscript are unaffected because cam1/cam2 vs cam3 is still "same marker versus a different marker"; only the
location words change.

## 6. Minimum main-text change under B (not applied)

1. Add the supplement items to the `\supplementary{}` list.
2. Add one sentence to Methods (after the spectral estimator paragraph): the supplement contains a separate
   per-camera RMS analysis that uses a tag-plane rectification and is not used for any main-text result.
3. Amend the sentences in section 3 above by a clause each.
4. If the owner refuses these edits, fall back to Option A.

Supplement release remains gated by owner item O-07 (permission to publish derived tables).
