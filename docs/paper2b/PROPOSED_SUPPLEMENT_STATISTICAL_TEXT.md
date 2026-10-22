# Proposed Supplement text: statistical supporting layer (Paper 2B)

**Status:** guidance only; no `.tex` edited. Release of any derived table is gated by owner item O-07
(permission to publish derived tables); nothing here authorizes transmission.

Proposed new supplement items (numbering continues after S12; final numbers are an owner decision):

| Proposed item | File | Content |
|---|---|---|
| S13 | `FREQUENCY_CORRESPONDENCE_RESULTS.csv` | per camera/target/subset frequency-correspondence statistics (19 and 17 conditions) |
| S14 | `REPEATABILITY_RESULTS.csv` | cam1/cam2 same-marker repeatability, two subsets |
| S15 | `RMS_SCALING_RESULTS.csv` | pooled RMS response-trend statistics, three subsets |
| S16 | `STATISTICAL_COMPARISONS.csv` | cam3 observation-path dependence and forced-alignment rows (114) |
| S17 | `BOOTSTRAP_RESULTS.csv`, `LEAVE_ONE_CONDITION_OUT.csv` | condition-level bootstrap (10000 resamples, seed 0) and leave-one-out |
| S18 | `STREAM_INVENTORY_VALIDATION.csv`, `STATISTICAL_SOURCE_HASHES.sha256`, `STATISTICAL_RUNTIME.txt` | denominators and provenance |
| S19 | `PER_CAMERA_RMS_VALUES.csv`, `PER_CAMERA_RMS_COMPARISON.csv`, `PER_CAMERA_RMS_SOURCE_HASHES.sha256` | per-camera RMS (mm, rad) and comparisons |
| S20 | `run_statistical_analysis.py`, `run_per_camera_rms.py` | generating scripts |

Proposed supplement section text:

> **Statistical supporting layer.** This part of the supplement documents the condition-level
> statistical characterization that supports Section X. The statistical unit is the RPM condition. The
> camera stream inventory contains 63 condition-camera streams (60 admissible, 2 rejected,
> 1 diagnostic-only), including 3 camera-only 0 RPM streams that have no matched laser
> condition. The laser domain contains 20 conditions (20-320 RPM); frequency correspondence uses the
> 19 non-320 conditions, giving 114 condition-camera-target rows. Sensitivity subsets exclude
> 60 and 80 RPM (17 conditions) and are always reported after the full set. Intervals are percentile
> bootstrap intervals over complete conditions (10000 resamples, seed 0). No frame-level hypothesis
> test is performed. Frequency results are operational correspondence, not accuracy. RMS results are
> response-trend correspondence, not calibration. The forced-alignment diagnostic is mathematical forced
> alignment, not recovery of a physical shared clock.

Proposed provenance paragraph (the hashes are in the listed files and must be re-read at integration,
not copied from this document):

> Input hashes for the statistical layer are recorded in `STATISTICAL_SOURCE_HASHES.sha256` (including the
> canonical stream table `results/s2c_stream_table_dev.csv`) and for the per-camera RMS layer in
> `PER_CAMERA_RMS_SOURCE_HASHES.sha256`. Runtime, package versions, bootstrap seed and admissibility counts
> are in `STATISTICAL_RUNTIME.txt` and `PER_CAMERA_RMS_RUNTIME.txt`. Per-camera RMS values were recomputed
> from the frame-level pose Parquet source; agreement with the earlier per-stream table is a check only.

Proposed "What this supplement does not establish" addition:

> The statistical tables are descriptive and post-hoc. They do not establish camera accuracy,
> simultaneous validation, synchronization, calibration, modal identification, a unique torsional or
> bending mode, or physical shared-clock recovery.

Note for the authors: the per-camera RMS files contain absolute filesystem paths and a repository commit
hash in the runtime file. Check whether these should be shipped as is (see OI-11).
