# Paper 2B Sensors — Master Status and Revision Plan

**Project:** Paper 2B, Sensors manuscript\
**Record date:** 2026-10-21\
**Working directory:** `/home/ammar/Paper2_Sensors_Finalization_2026-10/`\
**Consolidation root:** `/mnt/space/adev/research/publications/paper2_fin/`\
**Manuscript branch:** `revision/oct-2026-edit`\
**Current manuscript:** `/mnt/phd_data/phd_master/05_publications/p02_sensors_mdpi_revision_2026-10/paper2_sensors_synthesis.tex`

## Executive status

Paper 2B has moved from conceptual rescue into controlled evidence-bounded reconstruction. The physical-record audit is substantially complete for timestamp provenance and downstream numerical reproducibility. The manuscript has not been substantially rewritten from these findings, and no manuscript, supplement, frozen result table, raw data, or canonical source has been modified during this audit sequence.

The defensible scientific identity is:

> An empirical study of the repeatability and interpretability of dominant spectral features extracted independently from multiple camera observations of a bridge-deck model.

It is not currently a new Lomb–Scargle method, synchronization method, modal-identification study, or camera-accuracy validation paper.

## Current evidence classification

| Area | Current classification | Meaning |
|---|---|---|
| ROS record-time provenance | **VERIFIED** | Exhaustive replay of 21/21 bags, 63/63 streams, 115,276/115,276 rows matched to nine decimal places. |
| Exposure-event timing | **UNRESOLVED** | Neither bag record time nor `header.stamp` establishes the optical exposure epoch. |
| Detection-table linkage | **VERIFIED** | Step 01 timestamps and `per_frame_detections.csv` match for all 115,276 rows. |
| Downstream spectral results | **REPRODUCED** | Recomputed from candidate derived inputs and matched frozen outputs. |
| Camera-to-laser frequency correspondence | **HISTORICALLY REPORTED / EXPLORATORYALLY RECOMPUTED** | Cross-campaign condition-level comparison; not simultaneous validation. |
| Camera displacement accuracy | **UNRESOLVED** | No simultaneous, co-located, calibrated waveform comparison exists. |
| Structural modal identification | **UNRESOLVED** | No complete multi-point, spatially registered phase/mode-shape evidence exists. |
| Manuscript promotion | **NOT AUTHORIZED** | Numerical rewriting should wait until the claim ledger and manuscript authority are reconciled. |

## Scientific boundaries that must remain visible

1. `timestamp_s` is normalized ROS bag record time, not verified exposure time.
2. Camera synchronization at the exposure level is not established.
3. Cam1/cam2 agreement demonstrates repeatability on the same marker, not accuracy.
4. Cam3 differences cannot be attributed uniquely to marker location, torsion, bending, or a structural mode because marker location and optical path are confounded.
5. The approximately 9 Hz/background feature has unresolved origin.
6. The laser comparison is cross-session correspondence, not simultaneous physical validation.
7. Synthetic benchmark results characterize estimator behavior under imposed models; they do not validate physical camera accuracy.
8. Lomb–Scargle is established and must not be presented as novel.
9. Rayleigh resolution, frequency-grid spacing, estimator uncertainty, and completeness are distinct quantities.
10. Preserved unfavorable, null, and inconclusive findings are part of the evidence, not errors to remove.

## Research questions and bounded contributions

### RQ1 — Same-marker repeatability

To what extent do independently processed cameras observing the same marker recover consistent dominant spectral features?

### RQ2 — Observation-path and temporal dependence

How do camera–marker observation paths, temporal segmentation, and background conditions affect the selected dominant features?

### RQ3 — Processing sensitivity

How sensitive are the extracted features to native timestamps, uniform interpolation, nominal timing, and FFT processing?

### RQ4 — External correspondence

What bounded frequency correspondence exists between the camera results and the separately acquired 2025 laser measurements?

### Permitted contributions

1. Reproducible per-camera spectral characterization of the wind-tunnel camera dataset.
2. Same-marker repeatability analysis distinguished explicitly from accuracy.
3. Observation-path, temporal, background, and processing-sensitivity analysis.
4. Fixed-rule cross-session comparison with the 2025 laser campaign, described as correspondence.

## Project organization

Consolidated master root:

`/mnt/space/adev/research/publications/paper2_fin/`

Important Paper B paths:

- Master: `/mnt/space/adev/research/publications/paper2_fin/02_paper_B_sensors/master`
- Revised workspace: `/mnt/space/adev/research/publications/paper2_fin/02_paper_B_sensors/revised/`
- Audit package: `/mnt/space/adev/research/publications/paper2_fin/02_paper_B_sensors/audit_package`
- Current reconciliation: `/mnt/space/adev/research/publications/paper2_fin/02_paper_B_sensors/audit_outputs/current_reconciliation`
- Shared linked data: `/mnt/space/adev/research/publications/paper2_fin/03_shared_linked_data/`
- Large raw bags: linked, not copied.
- Large extracted PNG frames: linked, not copied.

The initial timestamp audit attempt failed because `pr03_readonly_audit.py` was absent from `analysis_outputs`; therefore the original diagnostics CSV was empty and the audit log contained a missing-file error. Later audits used the actual source and derived artifacts.

## Completed audit and reconciliation work

### 1. Initial packaging and preservation

The five earlier physical reconciliation outputs were packaged as:

`PR03_PR01_audit_outputs_2026-10-21.zip`

Recorded ZIP SHA-256:

`533b2ed9b99cec58c9c4e4ba197b6ea3359a18b6d77225ec92e845f6ff32f5b6`

The ZIP contained:

- `PR03_TIMESTAMP_PROVENANCE_REPORT.md`
- `PR01_CAMERA_SPECTRAL_RECONCILIATION.md`
- `PR03_PR01_CLAIM_LEDGER.csv`
- `RECONCILIATION_DISCREPANCIES.csv`
- `SOURCE_HASH_MANIFEST.sha256`

### 2. Claude read-only inventory

Inventory report:

`02_paper_B_sensors/revised/independent_audits/claude/CLAUDE_PROMPT1_INVENTORY_REPORT.md`

Inventory TSV:

`02_paper_B_sensors/revised/independent_audits/claude/CLAUDE_PROMPT1_INVENTORY.tsv`

Main findings:

- The master manuscript and Oct-01 audit manuscript diverge.
- The master and audit supplement have an author-list conflict.
- The supplement PDF is stale relative to its TeX source.
- `canonical_apriltag_frames.csv` is absent.
- Producer lineage for some derived tables is incomplete.
- Some historical 2024-reference artifacts remain in the package.
- Old sweep metadata contains stale `/run/media/...` paths even where hashes match copied inputs.

### 3. Antigravity Job 1 integrity audit

Location:

`02_paper_B_sensors/revised/independent_audits/agy/`

Result: **PASS, exit code 0**.

Verified:

- 11 canonical files across 23 filesystem instances.
- 63 condition–camera keys.
- 60 admissible, 2 rejected, 1 diagnostic-only.
- 315 retained peaks.
- 115,276 full frames and 113,852 valid samples.
- Strict timestamp monotonicity for 63/63 streams.
- Symlink resolution.

### 4. Antigravity Job 3 numerical reconciliation

Location:

`02_paper_B_sensors/revised/independent_audits/agy_job3/`

Result: **PASS, exit code 0**.

The validator checked 6,299 numerical comparisons and found zero failures. It reproduced:

- 63 streams.
- 115,276 full frames.
- 113,852 valid samples.
- 315 retained spectral peaks.
- 60/2/1 admissibility classification.
- Maximum cam1/cam2 dominant-peak separation: `0.002356158 Hz`, or `0.071885672 Rayleigh bins`, at `e1_20rpm`.

This is downstream mathematical reproduction from candidate derived inputs, not by itself exhaustive raw-bag regeneration.

### 5. Claude timestamp provenance audit

Location:

`02_paper_B_sensors/revised/independent_audits/claude/CLAUDE_PROMPT2_TIMESTAMP_REPORT.md`

The code path showed:

```text
timestamp_s = (ROS bag record timestamp - first image record timestamp in the bag) / 1e9
```

It is not `header.stamp`, not frame index, and not an exposure timestamp.

### 6. Antigravity Job 4 exhaustive raw-bag replay

Location:

`02_paper_B_sensors/revised/independent_audits/agy_job4/`

Result: **ALL 21 BAGS / 63 STREAMS / 115,276 ROWS MATCHED**.

Verified:

- 21/21 raw bags replayed.
- 63/63 streams matched.
- 115,276/115,276 rows matched at nine decimal places.
- Zero missing rows.
- Zero extra rows.
- Zero mismatches.
- No PNG image files decoded or opened.

Header diagnostic:

- 20 rows matched the earliest-frame condition.
- 115,256 rows did not match header-based normalization.
- Global observed record/header offset: 7.042–25.321 ms.
- Mean offset: 9.519 ms.
- Physical cause of the offset is not established.

Final classification:

- ROS record-time provenance: **VERIFIED**.
- Step 01 to detection table: **VERIFIED**.
- Detection to spectrum: **REPRODUCED**.
- Exposure-event timing: **UNRESOLVED**.

## Verified numerical findings

| Quantity | Result | Scope |
|---|---:|---|
| Full native frames | 115,276 | All 63 streams |
| Valid spectral samples | 113,852 | Lomb–Scargle inputs |
| Dropped frames | 1,424 | 717 cam1 + 707 cam2 at 320 RPM |
| Retained peaks | 315 | 63 streams × 5 peaks |
| Admissible streams | 60 | e0–e19, all cameras |
| Rejected streams | 2 | e20 cam1/cam2 |
| Diagnostic-only streams | 1 | e20 cam3 |
| Cam1/cam2 maximum separation | 0.002356158 Hz | e1_20rpm |
| Cam1/cam2 maximum separation | 0.071885672 Rayleigh bins | e1_20rpm |

## Exploratory camera–laser work completed

Exploratory outputs are under:

`/home/ammar/Paper2_Sensors_Finalization_2026-10/exploratory_validation/`

They are not manuscript-authorized evidence.

### Frequency and RMS comparison

Generated:

- `EXPLORATORY_CAMERA_LASER_ACCURACY_MODAL_REPORT.md`
- `EXPLORATORY_CAMERA_LASER_DOMINANT_SUMMARY.csv`
- `EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv`
- `EXPLORATORY_CAMERA_LASER_FREQUENCY_SUMMARY.csv`
- `EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv`
- `EXPLORATORY_CAMERA_LASER_RMS_SUMMARY.csv`
- `EXPLORATORY_SOURCE_HASHES.json`

Findings:

- Cam1/cam2 versus laser bending dominant frequency: median absolute error approximately `0.034 Hz` over 19 non-320-RPM matched conditions.
- Cam1/cam2 versus laser torsional dominant frequency: median absolute error approximately `0.846 Hz`.
- RMS bending correlation: `r = 0.815` across 19 non-320-RPM conditions; `r = 0.990` after excluding 60 and 80 RPM, which is a post-hoc sensitivity subset.
- RMS torsional correlation: `r = 0.943` across 19 non-320-RPM conditions; `r = 0.988` after excluding 60 and 80 RPM.
- Mean camera/laser torsional RMS ratio is approximately `0.57–0.63`.

These are condition-level, cross-session correspondences. They are not waveform accuracy or simultaneous validation.

### Waveform-shape and apparent spatial-response analysis

Generated:

- `EXPLORATORY_WAVEFORM_SPATIAL_REPORT.md`
- `EXPLORATORY_WAVEFORM_SPECTRAL_SHAPE.csv`
- `EXPLORATORY_WAVEFORM_SPECTRAL_SHAPE_SUMMARY.csv`
- `EXPLORATORY_APPARENT_SPATIAL_RESPONSE.csv`
- `EXPLORATORY_APPARENT_SPATIAL_RESPONSE_SUMMARY.csv`

Findings:

- Normalized spectral-envelope cosine similarity, bending: median approximately `0.68` for RPM below 320.
- Normalized spectral-envelope cosine similarity, torsion: median approximately `0.14` for RPM below 320.
- Cam1/cam2 centroid-RMS ratio: mean approximately `0.996`, median approximately `1.003`.
- Cam3 relative to the cam1/cam2 mean: mean approximately `0.64`, median approximately `0.89` below 320 RPM.

The spatial table is an apparent observation-path response pattern, not a structural mode shape. Camera centroid values remain in pixels because no authoritative in-situ pixel-to-millimetre calibration was established for this analysis.

### Forced temporal alignment experiment

Location:

`/home/ammar/Paper2_Sensors_Finalization_2026-10/exploratory_validation/forced_alignment/`

Generated:

- `FORCED_ALIGNMENT_REPORT.md`
- `FORCED_ALIGNMENT_WAVEFORM_RESULTS.csv`
- `FORCED_ALIGNMENT_SUMMARY.csv`
- `APPARENT_CAMERA_PHASE_MODE_SHAPE.csv`
- `clean_plots/`
- `FORCED_ALIGNMENT_SOURCE_HASHES.json`
- `FORCED_ALIGNMENT_RUNTIME.txt`

Method:

1. Estimate a relative lag using cross-correlation on the first 60% of each condition.
2. Apply that lag unchanged to the remaining 40%.
3. Interpolate camera and laser signals onto one corrected common time grid.
4. Report training correlation, held-out correlation, standardized RMSE, conditional coherence, and conditional phase.

Corrected results:

- Cam1 bending, 19 non-320-RPM conditions: median training correlation approximately `0.597`.
- Cam1 bending, same conditions: median held-out correlation approximately `0.109`.
- Cam1 bending, same conditions: median held-out standardized RMSE approximately `1.063`.
- Across all admissible streams, bending median held-out correlation approximately `0.118`.
- Across all admissible streams, torsion median held-out correlation approximately `0.083`.

The earlier `-0.118` aggregate held-out value must not be used; it came from an inconsistent lag-indexing implementation and was corrected.

The forced-alignment experiment demonstrates that numerical lag optimization can create apparent alignment without establishing a physical shared timebase. It is a methodological stress test, not waveform validation.

## Manuscript authority and unresolved conflicts

Before numerical rewriting, resolve these items:

1. Select the authoritative manuscript copy: the live master differs from the Oct-01 audit copy.
2. Resolve the author-list conflict between the master and audit supplement.
3. Rebuild or explicitly retire the stale supplement PDF.
4. Decide whether historical 2024-reference artifacts remain, are regenerated, or are excluded.
5. Resolve the absent `canonical_apriltag_frames.csv` lineage gap by documenting the candidate-input boundary.
6. Resolve producer lineage for tables 26 and 28.
7. Resolve figure-producer lineage and missing pass-2 script references.
8. Resolve cam3 wording so no unique physical mechanism is assigned.
9. Retain the 2025 laser comparison as cross-session correspondence only.
10. Reconcile the current manuscript against the corrected claim ledger before writing Results.

## Master revision plan

### Stage 0 — Freeze and record

- [ ] Hash the authoritative manuscript, supplement, figures, frozen tables, and audit outputs.
- [ ] Record the selected manuscript authority and commit/branch state.
- [ ] Preserve the baseline manuscript unchanged.
- [ ] Keep exploratory outputs outside the canonical manuscript data tree.

### Stage 1 — Close evidence authority

- [ ] Resolve manuscript-copy authority.
- [ ] Resolve author metadata.
- [ ] Resolve stale supplement PDF.
- [ ] Resolve residual 2024 material.
- [ ] Freeze the physical claim ledger.
- [ ] Freeze the discrepancy register.

### Stage 2 — Freeze manuscript blueprint

- [ ] Approve title: `Per-Camera Spectral Features in Multi-View Bridge-Deck Measurements`.
- [ ] Approve RQ1–RQ4.
- [ ] Approve bounded contributions.
- [ ] Approve figure/table allocation.
- [ ] Mark prohibited claims in the ledger.

### Stage 3 — Rebuild Methods first

Recommended sections:

1. Experimental system and data acquisition.
2. Camera–marker geometry.
3. Marker tracking and admissibility.
4. Timestamp provenance and spectral estimation.
5. Time-representation and FFT comparisons.
6. Synthetic spectral benchmark.
7. Cross-camera, temporal, and background diagnostics.
8. 2025 laser comparison.
9. Reproducibility and evidence provenance.

Methods must state definitions, formulas, parameters, denominators, and provenance—not conclusions.

### Stage 4 — Rebuild Results from the ledger

Recommended sections:

1. Dataset coverage and admissibility.
2. Per-camera dominant spectral features.
3. Same-marker repeatability.
4. Different camera–marker observation path.
5. Temporal variation.
6. Background feature near 9 Hz.
7. Timebase and FFT sensitivity.
8. Synthetic benchmark.
9. Cross-session laser correspondence.

Report full and sensitivity subsets together. Never report only favorable exclusions.

### Stage 5 — Discussion and Limitations

Explicitly explain:

- repeatability versus accuracy;
- cam3 observation-path confounding;
- unresolved 9 Hz origin;
- native recorded time versus exposure time;
- forced alignment as a stress test, not synchronization;
- cross-session laser correspondence;
- why waveform accuracy and modal identification are not established;
- transferability and calibration limitations.

### Stage 6 — Introduction, Abstract, Conclusions

Write these only after the Results and claim ledger are frozen. Do not build the Introduction around unverified anticipated results.

### Stage 7 — Final verification

- [ ] Verify every numerical claim against a source table and script hash.
- [ ] Verify every citation against its actual content.
- [ ] Audit all figures, captions, legends, units, and denominators.
- [ ] Compile TeX and supplement from clean sources.
- [ ] Run source and PDF residue searches.
- [ ] Perform adversarial reviewer review.
- [ ] Confirm no prohibited accuracy, synchronization, or modal-identification claims remain.

## Immediate next actions

1. Do not insert the supplied blueprint verbatim.
2. Use `CORRECTED_DISCUSSION_LIMITATIONS_GUIDANCE.md` as the safe starting point.
3. Freeze the authoritative manuscript copy and author metadata.
4. Create the claim ledger as the single numerical authority.
5. Reconcile current manuscript claims against that ledger.
6. Draft Methods only after authority conflicts are closed.
7. Keep forced-alignment figures in the Supplement or Limitations section as a stress test.
8. Prepare a main-text frequency/RMS figure only after correcting year, denominator, and exclusion wording.
9. Do not claim camera accuracy or modal identification from the current cross-session data.
10. Plan a future simultaneous camera–laser campaign if true waveform validation is required.

## Recommended future validation experiment

For genuine waveform accuracy and modal identification:

- acquire camera and laser signals simultaneously;
- record a common hardware trigger or synchronization pulse;
- survey the camera marker and laser measurement points;
- calibrate camera displacement into physical units with uncertainty;
- record shutter/exposure timing;
- use multiple spatially registered markers and laser points;
- preserve phase and amplitude information;
- predeclare matching, lag, tolerance, and exclusion rules;
- reserve held-out operating conditions;
- compare waveforms in common units;
- estimate mode shapes from spatial amplitude and phase, not dominant frequencies alone.

## Reproduction commands

From `/home/ammar/Paper2_Sensors_Finalization_2026-10/`:

```bash
python3 exploratory_camera_laser_analysis.py
python3 exploratory_waveform_spatial_analysis.py
python3 forced_alignment_validation.py
python3 make_clean_forced_alignment_plots.py
```

These commands write only to `exploratory_validation/` in this workspace. They do not edit the manuscript or frozen canonical outputs.

## Current completion gate

Paper 2B is **not ready for final manuscript numerical editing** until manuscript authority, the claim ledger, and the residual provenance conflicts are resolved. The strongest completed result is the exhaustive verification of normalized ROS bag record-time provenance and exact downstream reproduction from the candidate derived detection table.

## Educational interpretation and manuscript-use guide

This section is intended as a working theoretical guide for manuscript writing, research discussion, and later PhD dissertation integration. It explains what each analysis means, what it does not mean, and how a reviewer or defense examiner may evaluate it.

### The central scientific idea

The camera and laser systems were not used as two synchronized sensors measuring the same waveform at the same instant. They were separate measurement campaigns performed at matched nominal RPM conditions. Therefore, the strongest comparison is not:

> Do the two time histories match sample by sample?

It is:

> Do the two systems show comparable operational frequency and response-magnitude trends across the same experimental operating conditions?

This is a condition-level cross-campaign correspondence study. It can support repeatability and trend correspondence. It cannot, by itself, establish instantaneous waveform accuracy, absolute displacement accuracy, or structural modal identification.

### Why the main figure should use trends rather than overlaid time traces

An overlay assumes that the two x-axes represent the same physical time. Here they do not. The camera timestamps are normalized ROS bag record times, while the laser records belong to a separate acquisition campaign. Even if both traces are resampled to 60 Hz and shifted until they visually overlap, that produces a mathematical alignment rather than a verified physical alignment.

The main figure should therefore show condition-level trends:

- Panel (a): camera and laser dominant operational frequencies versus RPM.
- Panel (b): camera and laser RMS response magnitudes or normalized RMS trends versus RPM.

The forced-alignment plots should appear only as a supplementary methodological stress test or a Discussion/Limitations figure.

## Corrected interpretation of the proposed two-panel figure

### Panel (a): dominant-frequency correspondence

The camera and laser dominant frequencies can be compared at matched RPM values. The laser table contains 20 matched RPM conditions from 20 to 320 RPM. The camera dataset additionally contains 0 RPM, which has no corresponding laser row in this comparison.

For cam1/cam2 and the laser bending-frequency comparison, the median absolute difference is approximately 0.034 Hz over 19 non-320-RPM matched conditions. The camera Rayleigh interval is approximately 0.0327–0.0328 Hz.

The correct interpretation is:

> The typical camera–laser bending-frequency difference is approximately one Rayleigh-resolution interval.

Do not write “within the Rayleigh resolution limit” because 0.034 Hz is slightly greater than approximately 0.0327 Hz. Use “comparable to the Rayleigh scale” or “approximately one Rayleigh interval.”

This is useful evidence of operational frequency correspondence, but not proof that either system measured the exact physical modal frequency.

### Panel (b): RMS response scaling

For a time series (x(t)), the RMS magnitude is commonly defined as

\[
x_{\mathrm{RMS}} = \sqrt{\frac{1}{N}\sum_{k=1}^{N} x_k^2},
\]

or, for a detrended signal, using (x_k-\bar{x}). RMS describes response magnitude or energy-like amplitude. It does not contain phase information and does not prove that two instruments measured the same instantaneous displacement.

The full non-320-RPM bending comparison gives approximately:

- Pearson correlation (r=0.815);
- mean camera/laser ratio approximately 0.917;
- median ratio approximately 0.998.

The stronger (r=0.990) value occurs after excluding 60 and 80 RPM in addition to 320 RPM. This must be presented as a sensitivity subset, not as the sole result. The exclusions may represent transition or regime-boundary behavior, but the manuscript must not call them “non-resonant” unless a separate physical criterion establishes that label.

The torsional RMS comparison gives approximately (r=0.943) over the full non-320-RPM set and approximately (r=0.988) after the same 60/80 RPM sensitivity exclusions. However, the camera/laser torsional RMS ratio is only approximately 0.57–0.63. Thus, the systems can track a similar condition-to-condition trend while disagreeing in absolute scale.

Recommended wording:

> The cross-campaign RMS responses followed similar operating-condition trends, while their absolute ratios remained condition- and channel-dependent. The full non-320-RPM bending comparison gave (r=0.815); a sensitivity subset excluding the documented 60 and 80 RPM transition conditions gave (r=0.990). These results indicate response-trend correspondence rather than calibrated displacement accuracy.

### Why frequency and RMS are useful but limited

Frequency and RMS answer different questions:

| Quantity | Simple question | Useful for | Does not prove |
|---|---|---|---|
| Dominant frequency | At what rate is the response oscillating? | Operational frequency correspondence | Exact mode identification or synchronized waveform agreement |
| RMS amplitude | How large is the response over a condition? | Response-trend scaling | Absolute displacement accuracy |
| Correlation (r) | Do two lists increase and decrease together? | Trend association | Causality, calibration, or equality of measurements |
| Ratio | Is one measurement larger or smaller on average? | Scale comparison | Stable calibration across campaigns |
| Phase | Are two signals delayed or shifted relative to one another? | Synchronized waveform analysis | Anything reliable when acquisition clocks are unrelated |
| Coherence | Is frequency-specific linear relation stable between simultaneous signals? | Same-session signal comparison | Cross-session physical coupling without synchronization |

## Corrected forced-alignment interpretation

### What the test did

For each condition, a relative lag was selected by maximizing camera–laser correlation on the first 60% of the available overlap. The same lag was then applied to the remaining 40%. Both traces were placed on one corrected mathematical time grid.

This is a deliberately favorable test for post-hoc alignment. If the signals had a stable shared physical waveform, the fitted lag should transfer to the held-out portion.

### Corrected results

The earlier values (r_{\mathrm{train}}=0.503\), (r_{\mathrm{test}}=-0.118), and standardized RMSE values of 1.36–1.44 came from an inconsistent lag-indexing implementation and are superseded.

After correction:

- all admissible bending streams: median training correlation approximately 0.503;
- all admissible bending streams: median held-out correlation approximately 0.118;
- all admissible bending streams: median held-out standardized RMSE approximately 1.14;
- cam1 bending only over 19 non-320-RPM conditions: median training correlation approximately 0.597;
- cam1 bending only: median held-out correlation approximately 0.109;
- cam1 bending only: median held-out standardized RMSE approximately 1.063;
- all admissible torsional streams: median training correlation approximately 0.143;
- all admissible torsional streams: median held-out correlation approximately 0.083;
- all admissible torsional streams: median held-out standardized RMSE approximately 1.25.

The precise values should be taken from `FORCED_ALIGNMENT_SUMMARY.csv`, not copied from earlier conversational drafts.

### What the test means in plain language

Training correlation asks:

> Can I choose a delay that makes the first part look similar?

Held-out correlation asks:

> Does the same delay continue to work on data that was not used to choose it?

The substantial reduction from training to held-out correlation shows that the apparent alignment is not reliably transferable. This is evidence against treating numerical lag optimization as a substitute for physical synchronization.

The result is scientifically useful, not a failure. It demonstrates a limitation that many waveform-comparison studies overlook.

### Safe Supplement caption concept

> Diagnostic stress test of post-hoc temporal alignment between separate camera and laser campaigns. The camera trace is reported as centroid position in pixels and the laser trace as displacement in millimetres. A relative lag was selected from the first 60% of the overlap and applied unchanged to the remaining 40%. The aligned overlay is a mathematical fit, not evidence of a shared physical clock. Held-out correlation and standardized RMSE are reported to show whether the fitted lag transfers beyond the fitting interval.

Do not use the earlier caption containing (r_{\mathrm{test}}=-0.118) or the claim that the experiment used “all 21 flow conditions.” The corrected matched comparison uses 20 laser RPM conditions and the admissible subsets must be stated explicitly.

## Recommended Results and Discussion structure

### Results subsection: Cross-campaign operational correspondence

Recommended order:

1. State that the comparison is condition-level and cross-session.
2. State the matched RPM domain: 20–320 RPM, 20 matched conditions.
3. Report frequency differences with the Rayleigh interval.
4. Report the full RMS comparison first.
5. Report the 60/80 RPM exclusion only as a sensitivity analysis.
6. State that frequency and RMS agreement do not establish accuracy.

### Results subsection: Same-marker camera repeatability

Report cam1/cam2 agreement separately. The ratio near 1.00 is a repeatability result because both cameras observe the same marker. Keep it separate from the camera–laser comparison.

### Supplement subsection: Forced-alignment stress test

Include:

- one or two clean plots, preferably 70 RPM and 200 RPM;
- the fixed lag used;
- the train/held-out split;
- corrected training and held-out statistics;
- the warning that the camera axis is in pixels and the laser axis in millimetres;
- the standardized panel only as a diagnostic, not as a physical amplitude comparison.

### Discussion subsection: Boundary of cross-campaign comparison

Recommended paragraph:

> The camera and laser records were obtained in separate campaigns and therefore did not share a verified physical timebase. We conducted a forced-alignment stress test by selecting a relative lag from the first 60% of each condition and applying that lag unchanged to the remaining data. The corrected results showed substantially weaker and condition-dependent held-out correspondence than the in-sample fit, with median held-out correlations of approximately 0.12 for bending and 0.08 for torsion across admissible streams. This demonstrates that numerical lag optimization can create apparent alignment without establishing a shared physical timebase. Accordingly, the cross-campaign comparison is restricted to operational frequency correspondence and condition-level RMS response scaling. Waveform RMSE, phase coherence, absolute displacement accuracy, and modal identification are not claimed without simultaneous acquisition, hardware timing, common calibrated units, and spatial registration.

## Reviewer and PhD-defense questions

### Question 1: Were the camera and laser measurements simultaneous?

Answer:

> No. They were separate campaigns matched by nominal operating condition. We therefore restricted the comparison to condition-level frequency and RMS trends and did not claim waveform validation.

### Question 2: Why not align the signals numerically?

Answer:

> We tested numerical lag optimization as a stress test. It produced an in-sample fit but weak held-out transfer, showing that numerical alignment cannot establish the missing physical timing relationship.

### Question 3: Why is (r=0.990) not proof of validation?

Answer:

> Correlation measures whether two condition-level lists vary together. It does not prove equality of the measured amplitudes, common timing, identical spatial observables, or causal equivalence. The full comparison and the sensitivity subset are reported together.

### Question 4: Why does the camera/laser ratio differ from one?

Answer:

> The campaigns were not simultaneous, the sensors did not necessarily observe identical spatial quantities, the camera response is affected by optical geometry and calibration, and the laser channels use a geometry-specific processing definition. The data support correspondence, not a stable calibration factor.

### Question 5: Does cam1/cam2 agreement prove camera accuracy?

Answer:

> No. It supports repeatability between independent cameras observing the same marker. Accuracy requires an external reference measured simultaneously at a geometrically equivalent point with known uncertainty.

### Question 6: Does cam3 identify a torsional mode?

Answer:

> No. Cam3 changes both the observed marker and the optical path. The effects are confounded, so the result is reported as observation-path dependence rather than unique modal evidence.

### Question 7: Does a dominant frequency identify a structural mode?

Answer:

> No. A dominant operational spectral feature can be associated with a structural response, forcing, background disturbance, or measurement-path effect. Modal identification additionally requires spatial mode-shape and phase evidence, together with a structural reference or model.

### Question 8: Why include a negative or inconclusive diagnostic?

Answer:

> The failed transfer of forced alignment is an important limitation result. It demonstrates why frequency-domain and condition-level comparisons are more defensible for these asynchronous records than waveform overlays.

## How this transfers to the PhD dissertation

The dissertation can use Paper 2B as a case study in evidence-bounded multi-view sensing:

1. Define repeatability, correspondence, accuracy, and modal identification as separate levels of evidence.
2. Show how provenance determines what a numerical result means.
3. Present the forced-alignment test as a caution against confusing software resampling with physical synchronization.
4. Use the camera–laser comparison to motivate a future synchronized experiment.
5. Preserve the distinction between operational response tracking and structural modal identification.

The dissertation should not generalize the cross-campaign results into a universal camera-validity claim.

## Additional analysis that would strengthen the paper without overclaiming

- Report confidence intervals for correlations and ratios, not only point estimates.
- Report both full and sensitivity subsets in one table.
- Use leave-one-condition-out sensitivity analysis to show whether one RPM drives the correlation.
- Report median absolute frequency error and the full distribution, not only the median.
- Separate cam1/cam2 same-marker results from cam3.
- Report the number of matched conditions for every statistic.
- Keep 320 RPM visible as a quality/admissibility boundary.
- Use normalized trends only when the normalization rule is stated.
- Avoid interpreting coherence or phase from asynchronous records as physical coupling.

## Final decision rule for manuscript inclusion

| Result | Include? | Safe framing |
|---|---|---|
| Cam1/cam2 same-marker agreement | Yes | Optical repeatability |
| Full camera–laser frequency correspondence | Yes | Cross-campaign operational correspondence |
| Full RMS trend correlation | Yes | Condition-level response scaling |
| 60/80 RPM sensitivity correlation | Yes, with full result | Sensitivity analysis; not sole evidence |
| Forced-alignment plots | Yes, preferably Supplement | Methodological stress test |
| Forced-alignment as synchronization | No | Not supported |
| Camera/laser absolute accuracy | No | Requires simultaneous calibrated acquisition |
| Cam3 as unique mode evidence | No | Observation-path confounding |
| Camera dominant peaks as identified modes | No | Operational spectral features only |

The paper can become stronger by making these boundaries explicit. The unfavorable alignment result should be retained because it explains why the manuscript uses frequency and RMS correspondence rather than unsupported waveform-validation claims.
