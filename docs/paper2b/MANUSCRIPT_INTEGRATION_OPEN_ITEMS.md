# Paper 2B statistical integration: open items

**Status:** guidance only. No `.tex`, manuscript, supplement, audit-package or analysis file was edited.
The items below must be resolved (or consciously accepted) before the proposed text is applied to a
`revised/` manuscript workspace. Blocking items are marked **BLOCKING**.

Sources read: `00_CONTROL/MASTER_README.md`, `00_CONTROL/REVISION_WORKFLOW.md`, the synthesis manuscript
and supplement `.tex`, `OWNER_PENDING_ITEMS.md`, `72_FINAL_SYNTHESIS_PRE_SUBMISSION_CHECKLIST.md`, and
the files in `analysis/paper2b/statistical/` and `analysis/paper2b/per_camera_rms/`.

## A. Conflicts between the statistical layer and the current manuscript text

**OI-01 (BLOCKING) The numbers 60 and 20 mean different sets.**
The manuscript's 60 admitted streams are e0-e19 x 3 cameras and its 20 admitted conditions include the
camera-only 0 RPM condition. The statistical package's 60 camera-laser matched streams are e1-e20 x 3
cameras (they exclude 0 RPM and include the three 320 RPM streams), and its 20-condition laser domain
includes 320 RPM. The frequency domain is 19 non-320 conditions (57 streams, 114 condition-camera-target
rows), so cam1/cam2 repeatability here uses 19 conditions where manuscript Table 3 uses 20. Every sentence
must name its set; the proposed text does so. The owner should confirm the wording.

**OI-02 (BLOCKING) Which laser session is the "2024 campaign"?**
The manuscript says the only external reference is the 2024 laser campaign, about eleven months before the
2025 cameras. `PER_CAMERA_RMS_REPORT.md` uses datasets labelled `laser_y2025` (chosen as primary "on dataset
naming only") and `laser_y2024`, and states the author did not verify whether the y2025 laser session shares
a campaign with the cameras. The proposed text therefore says "the dataset labelled y2025/y2024" and makes
no campaign-date claim. Resolve the session identity from facility records before naming campaigns.

**OI-03 (BLOCKING) Reference construct.**
Manuscript Section 2.3 states that `f_v = 1.4303 Hz` and `f_t = 3.1036 Hz` are "the only external reference
values used anywhere in this study". The statistical layer instead uses per-condition laser target
frequencies (the forced-alignment rows carry `laser_target_frequency_hz`, for example 3.35 and 4.35 at
20 RPM) and per-condition laser RMS. Either the Methods sentence and Figure 1 (the reference lane) are
extended to cover the laser RPM-sweep data, or the statistical layer is confined to the supplement with an
explicit exception. The definition of the per-condition laser target should also be verified against
`EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv` before it is described in the Methods.

**OI-04 (BLOCKING) Image-plane-only claims versus mm/rad RMS.**
The manuscript says the analysis is image-plane only, that no PnP or world-frame reconstruction is applied
to the primary observable, that "no intrinsic value" from the archived calibrations "is used or quoted
anywhere", that no torsion angle is reconstructed and that no physical amplitude is reconstructed. The
per-camera RMS package computes H1,y (mm) and H2 roll (rad) from pose estimation on rectified corners
using `config/intrinsics_bag.json` and a 20 mm tag side, with a provisional +/-2.5% scale bound
(ruler graduation unconfirmed). Including those RMS values contradicts several existing sentences
(Sections 2.1, 2.3, Limitations). Options: confine mm/rad RMS to the supplement with a stated exception,
or revise those sentences deliberately. The pixel-RMS ratio in `REPEATABILITY_RESULTS.csv` does not have
this problem.

**OI-05 Post-hoc status and thresholds.**
The manuscript states that no numeric tolerance was predeclared and that no pass/fail ruling is issued. The
statistical layer reports fractions within 0.1 Hz and within one Rayleigh interval. These are descriptive
post-hoc fractions, not acceptance criteria. The analysis plan was written after the freeze and is not
preregistered; the text should say so once, in the Methods.

## B. Number handling

**OI-06 Display precision.**
All values in the proposed text and claim map are verbatim from the CSVs (up to 16 significant digits).
Nothing was rounded. The manuscript needs a display rule (for example, significant digits justified by the
bootstrap interval width). Apply it by script from `MANUSCRIPT_INTEGRATION_CLAIM_MAP.csv`, not by hand, and
keep the claim map as the audit trail. Also decide whether to quote the 16-digit bootstrap bounds at all.

**OI-07 Forced alignment has no validated aggregate.**
`STATISTICAL_COMPARISONS.csv` holds 114 per-row diagnostics but no summary statistic over them, so the
proposed text gives the design and denominators only. Any median, range or count of held-out correlation
is a new computation and should be added to `run_statistical_analysis.py` (and re-validated) before it is
quoted. Treat the diagnostic as a stress test; do not describe it as supporting alignment.

**OI-08 Cam1/cam2 permutation test.**
It returned p = 1.0 in both subsets. This is uninformative and must not be presented as significance or
equivalence. Consider omitting it from the main text.

**OI-09 Pooled RMS source.**
The statistical RMS table is a pooled camera/laser source, not camera-specific, and its scope for cam3 is
recorded as unavailable (0 conditions). Define what "pooled camera" means (which cameras, which
averaging) before the Methods describe it. The camera-specific RMS values come from the per-camera package.

## C. Inconsistencies inside the committed evidence package (not edited here)

**OI-10 `PER_CAMERA_RMS_REPORT.md` text versus code (corrected 2026-10-22).**
The report prose for the bootstrap has been corrected to match the generator (`SEED, NBOOT = 0, 10000`), the
runtime file and the CSV notes: 10,000 resamples of conditions, seed 0. The report header no longer hard-codes a
repository HEAD; the runtime file records the commit at the last run. The values were not affected.

**OI-11 Absolute paths in shipped provenance files.**
`STATISTICAL_SOURCE_HASHES.sha256` and the per-camera hash file contain absolute `/mnt/space/...` paths.
They are legitimate provenance, but check them before they are shipped as supplement files.

## D. Scope, figures and process

**OI-12 Figure selection and quality.**
The manuscript has 5 figures and 4 tables. Decide which of the 10 statistical plots and 4 per-camera plots go
in the main text, and which in the supplement. Statistical plots are PNG; 300 dpi (checklist B1-B3) and vector
status are unchecked, and `FIGURE_CAPTIONS.md` should not be reused verbatim because its "60 matched
streams" differs from the manuscript's 60 (OI-01).

**OI-13 Identity, abstract and conclusions.**
Paper 2B stays a reference-blind per-camera spectral analysis. The proposed text adds a supporting layer
and does not alter the title, the three stated contributions, or the abstract. Whether to add a single
abstract or conclusion sentence is an owner decision; if so, keep it to "condition-level statistical
characterization", with no accuracy language.

**OI-14 Supplement release gate.**
Owner item O-07 (permission to publish derived tables) is still BLOCKING and extends to the new statistical
tables S13-S20 proposed in `PROPOSED_SUPPLEMENT_STATISTICAL_TEXT.md`. Also noted from the checklist: S4/S5
producer scripts are missing (O-09), and the synthesis candidate has not passed an independent re-audit.

**OI-15 Workflow when editing starts.**
Per `REVISION_WORKFLOW.md`: edit only under `02_paper_B_sensors/revised/`; record the starting git commit
and working-tree status; list the affected claim-ledger rows (`STATISTICAL_CLAIM_LEDGER.csv` C01-C07 and the
claim map); build with `pdflatex` x3; run source searches for stale claims; re-run numerical checks against
the linked source data; record hashes; obtain review before replacing the master. Other owner-pending items
(O-01b to O-06) are independent of this work.

## E. Wording to keep out of the manuscript

Accuracy, synchronization or synchronized exposure, simultaneous validation, modal identification, a unique
torsional or bending mode, calibration, causal attribution of the cam3 difference, ground truth, and
describing the laser as a reference of record for the camera values. Cam1/cam2 H1,y must never be called heave.
