# Updated manuscript-integration open items

Supersedes the status of `MANUSCRIPT_INTEGRATION_OPEN_ITEMS.md` (left unchanged). No manuscript, supplement
or submission file, and nothing under `docs/catalog_agy/audit/`, was edited. Evidence behind each line is in
`DOMAIN_RECONCILIATION.csv`, `LASER_SESSION_PROVENANCE_REVIEW.md`, `ESTIMAND_SCOPE_DECISION.md` and
`PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md`.

## 1. Status of the earlier items

| Earlier item | Status | Resolution (source) |
|---|---|---|
| OI-01 two meanings of "60"/"20" | **RESOLVED** | The manuscript's 60 admitted streams (e0-e19) are domain DM01/DM03; the statistical 60 (e1-e20 x 3, includes the three e20 streams) is DM04. They share 57 streams. 20 conditions mean e0-e19 in the manuscript, e1-e20 (laser) in the statistics, and 19 for frequency (DM06). DOMAIN_RECONCILIATION.csv. |
| OI-02 which laser is "2024" | **RESOLVED** (identity); wording left to owner | y2024 = October 2024 session (matches the manuscript's 36,000-sample, 100 s record). y2025 = September 2025 session, about ten days before the camera bags of 2025-10-01; not simultaneous. LASER_SESSION_PROVENANCE_REVIEW.md R1-R3. |
| OI-03 reference construct | **RESOLVED** (scope); one owner choice open | Four constructs separated; A (fixed refs) stays the only main-text reference; B is Supplement-only. ESTIMAND_SCOPE_DECISION.md ED-01, ED-02. Open: OD-1, OD-2. |
| OI-04 image-plane versus mm/rad RMS | **RESOLVED** (scope); wording open | Option B, Supplement only, with a scope exception. PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md. Open: OD-3. |
| OI-05 post-hoc thresholds | OPEN | Unchanged. State once in Methods that 0.1 Hz and one-Rayleigh fractions are descriptive and were introduced after the freeze. |
| OI-06 display precision | OPEN | Unchanged. Apply a rounding rule by script from the claim map. |
| OI-07 forced alignment has no validated aggregate | OPEN | Unchanged. Add a summary to `run_statistical_analysis.py` and re-validate before quoting. |
| OI-08 permutation test p = 1.0 | OPEN | Unchanged; omit from main text. |
| OI-09 pooled RMS definition | **RESOLVED** | Defined: a cross-camera combination (ledger row 11) of an older pipeline (row 12). Withdrawn (ED-03). |
| OI-10 per-camera report seed/HEAD text | **RESOLVED** | `PER_CAMERA_RMS_REPORT.md` now states 10,000 bootstrap resamples, seed 0, matching code and runtime, and no longer hard-codes a repository HEAD. The validation report still names the HEAD it was run at (`8d03ba3`), which is a historical run record. |
| OI-11 absolute paths | OPEN | Unchanged. |
| OI-12 figure selection and quality | PARTLY RESOLVED | Statistical figures 02, 03, 10 (pooled RMS) are withdrawn. Others still need a main-text/supplement choice and a dpi check. |
| OI-13 identity, abstract | **RESOLVED** | No abstract or title change; the image-plane spectral identity is retained (default accepted). |
| OI-14 supplement release gate | OPEN | O-07 still blocking. |
| OI-15 workflow | OPEN | Unchanged. |

## 2. New findings from this review

**NF-1 (RESOLVED by owner decision, 2026-10-22; manuscript text still to be changed). Marker labels in the manuscript are reversed.**
Manuscript: cam1/cam2 view the center/near-center marker, cam3 the off-center/side marker (tex lines 190-193,
254-258, 696-698, 797-799). Owner-confirmed: cam1/cam2 view the same side/off-center marker (handwritten label
`ID-0-1`), cam3 views a distinct centre marker (`ID-0-2`). Both decode as AprilTag ID 0, so the machine ID alone does
not distinguish them. The exact separation is not surveyed; cam1/cam2 vertical metric motion is not direct heave;
any near-axis lever-arm statement stays data-derived and qualified. Also affects the audit-package provenance report
lines 23-27 (left unchanged) and the Table 3 caption "(Marker A)".

**NF-2 (BLOCKING). The "pooled camera" RMS contains the rejected 320 RPM streams and a cross-camera
combination.** Row `rpm=320`, flag `DCG-excl` of `table_2025_ldv_primary.csv`; ledger row 11. Every
`full_20` row of `RMS_SCALING_RESULTS.csv` is affected. Withdrawn from the manuscript (ED-03).

**NF-3. `ds004` `metadata.yaml` gives camera dates "2024-11 to 2025-01".** The bag index says 2025-10-01.
Do not cite the metadata dates. Correct the metadata in the dataset record (outside this repository).

**NF-4. Owner decisions A1 and A3 (2026-10-18) conflict with the Paper 2B manuscript lineage.** A1 drops the
2024 laser from papers; A3 sets the paper reference frequencies to 1.4318 Hz and 3.0982 Hz. The manuscript
and its frozen comparison use the 2024 values 1.4303 Hz and 3.1036 Hz and describe a 2024 laser lane.

**NF-5. Which manuscript file is current?** The status plan names
`/mnt/phd_data/phd_master/05_publications/p02_sensors_mdpi_revision_2026-10/paper2_sensors_synthesis.tex`; this
review read the audit-package copy (`.../audit_package/01_MANUSCRIPT/paper2_sensors_synthesis.tex`). Line numbers
cited in these files refer to the audit-package copy. They were not diffed against the other copy.

**NF-6. The lever arm of about 125 mm is descriptive.** Source `PER_CAMERA_RMS_GO_NO_GO.md` condition 4; not a
survey. Label it accordingly.

## 3. Owner decisions needed

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| OD-1 | Reference frequencies in Paper 2B | (a) keep 1.4303/3.1036 (2024, facility values; frozen comparison unchanged); (b) adopt 1.4318/3.0982 per A3 and recompute Table 4 and the 33/60 and 17/60 counts by script | (a) for this revision, because the freeze, Table 4 and Figure 7 are built on it and the 2024 lane is already documented; record that A3 applies to the other papers. Choose one, never both. |
| OD-2 | Include construct B (per-condition y2025 laser targets) at all | Supplement only / drop | Supplement only, labelled exploratory and cross-session. Dropping is consistent with A1's spirit if the owner wants a single laser lane. |
| OD-3 | Methods exception for the per-camera RMS supplement | accept the one-sentence exception and amendments in PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md section 6 / fall back to Option A | Accept. |
| OD-4 | Marker labels (NF-1) | **RESOLVED 2026-10-22**: cam1/cam2 = same side/off-center marker (ID-0-1), cam3 = distinct centre marker (ID-0-2) | Change the manuscript text once, using the labels in `MARKER_IDENTITY_RECONCILIATION.md` section 5. |
| OD-5 | Campaign wording | neutral labels "laser session A (2024)" and "B (2025, shortly before the camera recordings)" / dated wording | Neutral labels, consistent with the 2026-10-16 decision to omit exact dates. |

## 4. Edits to the earlier proposed text that follow from the decisions (not yet applied)

Applying these changes edits files created in the previous step; they were left untouched here because this
task allowed only five new files.

1. `PROPOSED_RESULTS_STATISTICAL_TEXT.md`: delete "Pooled RMS response-trend correspondence" and its table;
   delete "report both sessions" and the y2024 values; change "the dataset labelled y2025" to "laser session B";
   replace the marker wording with the owner-confirmed assignment (OD-4 closed; `MARKER_IDENTITY_RECONCILIATION.md`);
   move per-camera RMS paragraphs to the supplement text;
   keep frequency correspondence, repeatability, cam3 observation path and forced alignment, naming DM05 as
   withdrawn and DM06 as the frequency domain.
2. `PROPOSED_SUPPLEMENT_STATISTICAL_TEXT.md`: remove S15 (pooled RMS); add the construct B and construct D
   items with their domains; keep O-07 gating.
3. `STATISTICAL_FIGURE_CAPTIONS.md`: remove captions 02, 03 and 10.
4. `PROPOSED_DISCUSSION_STATISTICAL_TEXT.md`: delete the "RMS results are response-trend correspondence" paragraph
   as a statement about pooled RMS; restate it for per-camera RMS in the supplement only.
5. `MANUSCRIPT_INTEGRATION_CLAIM_MAP.csv`: set the `S:` rows (CM12, CM13 for RMS) to status WITHDRAWN.

## 5. Statements that remain valid

Frequency results are operational correspondence, not accuracy. 0 RPM is camera-only. Forced alignment is
mathematical, not recovery of a physical shared clock. Cam1/cam2 repeatability is kept separate from cam3
observation-path dependence. The statistical layer is a supporting methodological layer. No accuracy,
synchronization, simultaneous-validation, modal-identification, causal or ground-truth claim is supported.
