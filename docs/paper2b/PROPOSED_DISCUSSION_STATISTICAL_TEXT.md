# Proposed Discussion text: statistical supporting layer (Paper 2B)

**Status:** guidance only; no `.tex` edited. Numbers appear only where they restate a value already
tabulated in `PROPOSED_RESULTS_STATISTICAL_TEXT.md`; the claim map gives each source cell.

Proposed placement: one new Discussion subsection after "Same-Marker Cross-View Agreement" and
"Differences at the Distinct Observation Location", or a single subsection titled below.

---

## Proposed subsection: What the Condition-Level Statistics Add and Do Not Add

The condition-level statistics were added as a supporting methodological layer. They quantify, with
the RPM condition as the unit, three things the per-camera analysis had described only per condition:
how closely two cameras on the same marker agree, how a camera on a separate marker departs from them,
and how the camera features and RMS levels trend alongside the laser sessions. The identity of the
study is unchanged: it remains a reference-blind per-camera spectral analysis, and the statistics are
computed after the camera features were frozen.

**Repeatability and observation path are different questions.** The cam1/cam2 results measure the
repeatability of two processing branches viewing one marker. The cam3 results measure dependence on the
observation path, in which marker location and camera channel are confounded. The statistics keep the
two apart, and the discussion should do so: a cam3 departure from the cam1/cam2 mean is not a
repeatability failure, and cam1/cam2 agreement says nothing about cam3.

**Frequency results are operational correspondence.** The camera frequency was the nearest retained peak
to a per-condition laser target. The laser data come from sessions that are not simultaneous with the
camera campaign. The fractions within 0.1 Hz and within one Rayleigh interval describe how often the
nearest retained peak falls near the target, which depends on how many peaks are retained and on record
resolution. They are not accuracy, and torsion and bending differ in how dispersed the differences are
(report the median together with RMSE and the 90th percentile).

**RMS results are response-trend correspondence.** The pooled RMS statistics describe whether camera
and laser response levels rise and fall together across conditions. The slope is a cross-session
descriptive regression, not a calibration. Two regime-boundary conditions (60 and 80 RPM) strongly
influence rank agreement, so the full set and the sensitivity subset must be quoted together.

**Cam1/cam2 H1,y is vertical metric motion of the side/off-center marker, not direct heave.** Both
cameras view the same side/off-center marker (handwritten label ID-0-1); its vertical metric motion
contains a lever-arm x roll contribution. Comparisons of cam1/cam2 H1,y with laser heave must carry that
label, and the laser pitch cannot be compared with roll without the unmeasured lever distance. Both
markers decode as AprilTag ID 0, so the decoded ID does not distinguish them.

**Cam3 is a heave proxy with limits.** Cam3 views a distinct centre marker (handwritten label ID-0-2),
whose apparent distance from the rotation axis, estimated from the data and not surveyed, is small
(about 6 mm median). That makes it the closer camera analogue of heave, but any near-axis statement is
data-derived and qualified. The marker geometry and the separation between the two markers were not
surveyed, its record is 60 Hz and about 30 s against a 360 Hz, 100 s laser record, and no
camera-specific common-unit calibration enters the pooled RMS table. A ratio below or above one is
therefore not an error estimate.

**Forced alignment is mathematical.** Fitting a lag on 60% of a record and applying it to the remaining
40% tests whether a time offset generalizes within the procedure. It does not recover a physical shared
clock and does not show that the two sessions were synchronized.

**What the statistics do not support.** They do not support camera accuracy, simultaneous validation,
synchronization, calibration, modal identification, a unique torsional or bending mode, causal
attribution of the cam3 difference, or treating the laser sessions as ground truth. The 0 RPM condition
is camera-only and enters none of the camera-laser comparisons.

### Suggested additions to the Limitations section

- All camera-laser comparisons are cross-session and non-simultaneous; between-session confounding is not quantified.
- The unit of inference is the condition (19 non-320 conditions per camera; 20 for pooled RMS); there is
  no replication within a condition and no frame-level test.
- Bootstrap intervals with 19 or 17 conditions are wide and, for rank statistics, depend on two
  regime-boundary conditions.
- The pooled RMS table has no camera-specific common-unit RMS for cam3.
- The +/-2.5% camera scale bound is provisional, and the laser scale uncertainty is not propagated.
- Frequency and RMS statistics were computed after the reference-blind freeze, are post-hoc, and no
  acceptance tolerance was predeclared for them.
