# Paper 2B — Consolidated State Report for ChatGPT Project

Date: 2026-10-22. Purpose: one paste-able document to rebuild context and get guidance on finishing Paper 2B.
Compiled from the repo documents listed in section 9. Numbers below are copied from those documents; they were not re-derived when this report was written.

## 1. What the paper is (and is not)

Working identity: an empirical study of the repeatability and interpretability of dominant spectral features extracted independently from three cameras observing a bridge-deck wind-tunnel model.
Working title: "Per-Camera Spectral Features in Multi-View Bridge-Deck Measurements".

It is NOT: a new Lomb-Scargle method, a synchronization method, a modal-identification study, or a camera-accuracy validation.

Research questions: RQ1 same-marker repeatability; RQ2 observation-path, temporal and background dependence; RQ3 processing sensitivity (timestamps, interpolation, FFT); RQ4 bounded cross-session correspondence with the 2025 laser campaign.

## 2. Evidence status

| Area | Status |
|---|---|
| ROS bag record-time provenance | VERIFIED: 21/21 bags, 63/63 streams, 115,276/115,276 rows matched to 9 decimals |
| Exposure-event timing | UNRESOLVED (neither record time nor header.stamp is exposure time; record/header offset 7.0-25.3 ms, mean 9.5 ms, cause unknown) |
| Detection table linkage | VERIFIED |
| Downstream spectral results | REPRODUCED (6,299 comparisons, 0 failures) |
| Camera-laser frequency/RMS | Exploratory, cross-session, condition-level only |
| Camera accuracy / synchronization / modal identification | NOT SUPPORTED by current data |
| Per-camera metric RMS package | VERIFIED (20/20 checks) but Supplement-only by decision |
| Manuscript promotion | NOT AUTHORIZED until open items below are closed |

Key counts: 115,276 frames; 113,852 valid samples; 1,424 dropped (717 cam1 + 707 cam2 at 320 RPM); 315 retained peaks; 60 admissible / 2 rejected / 1 diagnostic-only streams. Max cam1/cam2 dominant-peak separation 0.00236 Hz = 0.072 Rayleigh bins (e1_20rpm).

## 3. Work completed in the repo

1. Timestamp provenance audit and exhaustive bag replay (record-time verified, exposure time not).
2. Exploratory camera-laser analysis (frequency, RMS, spectral shape, apparent spatial response).
3. Forced-alignment stress test (60/40 lag fit and hold-out). Corrected results: held-out correlation about 0.12 (bending) and 0.08 (torsion); the earlier -0.118 is obsolete. Conclusion: numerical lag fitting does not create a shared clock.
4. Statistical package `analysis/paper2b/statistical/run_statistical_analysis.py` (commit acc126f on branch `paper2b-statistical-analysis`). This session fixed: repo-root resolution (parents[3]), input paths to `analysis/paper2b/exploratory/`, unused variable (ruff F841), paired-bootstrap indexing, statsmodels 0.15.0 in runtime metadata, a list-vs-DataFrame crash in plotting, and a wrong stream count in the hardcoded report text. Runs to completion; ruff clean. Outputs: 6 CSVs (rows: frequency 20, RMS scaling 7, repeatability 2, comparisons 116, leave-one-out 124, bootstrap 36), claim ledger (7 claims), plan, report, runtime, hashes, 10 plots. 10,000 bootstrap resamples, seed 0.
5. Per-camera RMS reconstruction (`analysis/paper2b/per_camera_rms/`, branch `paper2b-per-camera-rms-reconstruction`). Parity with earlier stream table within 4.4e-16, deterministic rerun, 61 pose streams.
6. Manuscript-integration layer in `docs/paper2b/`: domain reconciliation, laser session provenance, estimand scope decision, per-camera RMS scope decision, claim map, proposed Results/Discussion/Supplement text, figure captions, updated open items.

Key decisions made: per-camera RMS goes in the Supplement only (Option B); main text keeps its image-plane spectral identity; construct A (fixed reference frequencies) is the only main-text reference; construct B (per-condition 2025 laser targets) is Supplement-only if kept; pooled-camera RMS results are withdrawn (see NF-2).

## 4. Superseded statements (do not reuse)

- The statistical package's "no per-camera RMS available" limitation is superseded by the per-camera RMS package. The pooled-RMS tables and statistical figures 02, 03 and 10 are withdrawn.
- r_test = -0.118 forced-alignment value: obsolete.
- "all 21 flow conditions" wording: wrong; the matched laser domain is 20 RPM conditions.
- "within the Rayleigh limit" for the 0.034 Hz median bending difference: wrong (0.034 > 0.0327). Use "about one Rayleigh interval".
- Statistical report text said 63 streams / 60 admissible; correct is 60 streams / 57 admissible / 2 rejected / 1 diagnostic-only in the statistical table (the manuscript domain is 60 admitted streams e0-e19; they share 57 streams).

## 5. Blocking issues

- NF-1 (resolved by owner decision 2026-10-22; manuscript text still to be changed): the manuscript has the marker labels reversed (cam1/cam2 centre marker, cam3 off-centre). Owner-confirmed: cam1/cam2 view the same side/off-center marker (handwritten label ID-0-1), cam3 views a distinct centre marker (ID-0-2); both decode as AprilTag ID 0; separation not surveyed. Text changes once, coordinated.
- NF-2 (blocking, resolved by withdrawal): the "pooled camera" RMS included rejected 320 RPM streams and a cross-camera combination.
- Manuscript authority: live master and the Oct-01 audit-package copy differ; the numbers in the integration files cite the audit-package copy and were not diffed against the master (NF-5).
- Supplement release gate O-07 (permission to publish derived tables) still open.
- Other open items from the integration file (OI-05 post-hoc subset, OI-06, OI-07 re-validate statistical script, OI-08, OI-11 absolute paths, OI-12 figure selection, OI-15 workflow; OI-10 seed/HEAD text is now corrected): details were truncated when this report was compiled; read `UPDATED_MANUSCRIPT_INTEGRATION_OPEN_ITEMS.md` for exact wording.
- Smaller: author-list conflict (master vs audit supplement), stale supplement PDF, residual 2024-reference artifacts, missing `canonical_apriltag_frames.csv` lineage, producer lineage for tables 26/28 and some figures, dataset `metadata.yaml` camera dates (2024-11/2025-01) vs bag index (2025-10-01).

## 6. Owner decisions needed

| ID | Decision | Recommendation in repo |
|---|---|---|
| OD-1 | Reference frequencies: keep 1.4303/3.1036 (2024 facility) or adopt 1.4318/3.0982 | Keep 2024 values for this revision; choose one, never both |
| OD-2 | Include construct B (per-condition 2025 laser targets)? | Supplement only, labelled exploratory cross-session |
| OD-3 | Accept one-sentence Methods exception for supplementary per-camera RMS | Accept; otherwise fall back to Option A (exclude) |
| OD-4 | Marker labels (NF-1) | RESOLVED 2026-10-22: cam1/cam2 = same side/off-center marker (ID-0-1), cam3 = distinct centre marker (ID-0-2); change manuscript text once |
| OD-5 | Campaign wording | Neutral labels "laser session A (2024)" / "B (2025, shortly before camera recordings)" |

## 7. Claims that are safe vs prohibited

Safe: same-marker cam1/cam2 repeatability; operational frequency correspondence with laser (cross-session, 19 non-320 conditions); cam3 observation-path dependence (marker and optical path confounded); processing-sensitivity results; forced alignment as a stress test (Supplement/Limitations).
Prohibited: camera accuracy, synchronization, simultaneous validation, calibration, modal identification, unique torsion/bending attribution for cam3, "non-resonant" for 60/80 RPM, any pooled or cross-camera amplitude combination, torsion angle from the in-plane roll.
Always report full results before sensitivity subsets (for example bending r = 0.815 full vs 0.990 after post-hoc exclusion of 60/80 RPM, though these figures come from the now-withdrawn pooled RMS and need recomputation from per-camera data before use).

## 8. Recommended path to completion

1. OD-4 (marker labels) is resolved (owner decision 2026-10-22). Owner then decides OD-1 to OD-3 and OD-5. These are quick and unblock everything else.
2. Pick the authoritative manuscript copy; diff master vs audit-package copy; fix author list; retire or rebuild the stale supplement PDF.
3. Apply the pending edits to the proposed-text files (remove pooled-RMS paragraphs/captions, mark CM12/CM13 WITHDRAWN, add construct B/D items to the Supplement list).
4. Re-run the statistical script on the corrected domain, fix the seed/HEAD metadata (OI-10), and freeze the claim ledger as the single numerical authority.
5. Rewrite Methods, then Results, then Discussion/Limitations, then Introduction/Abstract/Conclusions (in that order, only after the ledger is frozen).
6. Final verification: every number vs source table and script hash, citation check, figure/caption/denominator audit, clean TeX compile, reviewer-style read.
7. Optional, for the dissertation or a follow-up paper: a simultaneous, hardware-triggered, calibrated camera-laser campaign is the only route to waveform accuracy or modal identification.

Suggested single next action: OD-4 (marker labels) is now settled by owner decision (see `MARKER_IDENTITY_RECONCILIATION.md`); apply the marker wording in the text edits and per-camera supplement wording.

## 9. Source files (all under the repo root unless noted)

- `docs/paper2b/PAPER2B_REVISION_MASTER_STATUS_AND_PLAN_2026-10-21.md`
- `docs/paper2b/UPDATED_MANUSCRIPT_INTEGRATION_OPEN_ITEMS.md`
- `docs/paper2b/PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md`
- `docs/paper2b/ESTIMAND_SCOPE_DECISION.md`, `DOMAIN_RECONCILIATION.csv`, `LASER_SESSION_PROVENANCE_REVIEW.md`
- `docs/paper2b/MANUSCRIPT_INTEGRATION_CLAIM_MAP.csv`, `PROPOSED_*_STATISTICAL_TEXT.md`, `STATISTICAL_FIGURE_CAPTIONS.md`
- `analysis/paper2b/statistical/` and `analysis/paper2b/per_camera_rms/` (reports, CSVs, runtime and hash files)
- `docs/DECISIONS.md` (2026-10-15 to 2026-10-17 owner decisions)

Not checked when compiling this report: whether the manuscript master matches any quoted line numbers; whether the per-camera RMS numbers agree with the statistical package; the uncommitted edit to `PER_CAMERA_RMS_REPORT.md` and the `docs/catalog_agy/audit` changes (not mine, left untouched).
