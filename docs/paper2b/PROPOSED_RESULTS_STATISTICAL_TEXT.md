# Proposed Results text: statistical supporting layer (Paper 2B)

**Status:** guidance only. No `.tex` file was edited. Every number below is read from a
validated CSV in `analysis/paper2b/statistical/` or `analysis/paper2b/per_camera_rms/` and is
printed at the precision stored in the file (no rounding, no new statistics).
Display precision for the manuscript is an owner decision (see
`MANUSCRIPT_INTEGRATION_OPEN_ITEMS.md`, item OI-06). Source cell for each value:
`MANUSCRIPT_INTEGRATION_CLAIM_MAP.csv`.

Proposed placement: a new Results subsection after the post-hoc reference comparison
(`sec:posthoc-reference`) and before `sec:robustness`, titled below.

**Integration note (not manuscript text):** the number 60 appears in two different senses. The manuscript's *60 admitted streams* are e0-e19 x 3 cameras (they include the camera-only 0 RPM streams and exclude 320 RPM). The statistical package's *60 camera-laser matched streams* are e1-e20 x 3 cameras (they exclude 0 RPM and include the three 320 RPM streams). The sets overlap but are not identical. Any sentence carrying either 60 must name its set.

---

## Proposed subsection: Condition-Level Statistical Characterization of the Per-Camera Features

### Role, unit and denominators

This subsection adds a supporting methodological layer to the per-camera analysis above. It does not
alter any feature extracted in the preceding subsections and does not change the reference-blind
freeze. All statistics use the RPM condition as the unit (camera-laser comparisons), the
condition-camera stream (per-camera spectral results) or the cam1/cam2 same-marker condition pair
(repeatability). No frame-level hypothesis test is performed. Intervals are percentile intervals from
10000 bootstrap resamples of complete conditions with seed 0.

The denominators are as follows.

| Quantity | Value | Source |
|---|---|---|
| Camera streams classified (21 conditions x 3 cameras) | 63 | STREAM_INVENTORY_VALIDATION.csv |
| Admissible streams | 60 | same |
| Rejected streams (cam1, cam2 at 320 RPM) | 2 | same |
| Diagnostic-only streams (cam3 at 320 RPM) | 1 | same |
| Camera-only 0 RPM streams (no matched laser condition) | 3 | same |
| Camera-laser matched streams (inventory minus camera-only 0 RPM; still contains the three 320 RPM streams) | 60 | same |
| Laser-matched RPM conditions (20-320 RPM) | 20 | STATISTICAL_RUNTIME.txt (matched_laser_conditions) |
| Frequency-correspondence conditions per camera (non-320) | 19 | FREQUENCY_CORRESPONDENCE_RESULTS.csv |
| Frequency-correspondence sensitivity conditions (excluding 60 and 80 RPM) | 17 | same |
| Condition-camera-target rows, three cameras x two targets x 19 conditions | 114 | STATISTICAL_RUNTIME.txt (frequency_condition_camera_target_rows=114) |
| Bootstrap resamples / seed | 10000 / 0 | BOOTSTRAP_RESULTS.csv |

The camera inventory classifies 63 condition-camera streams, of which 60 are admissible,
2 are rejected and 1 is diagnostic-only, matching the admissibility result reported earlier.
The three camera-only 0 RPM streams are in the inventory but have no matched laser condition and
enter no camera-laser comparison; 0 RPM is a camera-only condition. The laser domain contains 20 RPM
conditions (20-320 RPM). Because the cam1 and cam2 streams at 320 RPM are rejected and the cam3 stream
is diagnostic-only, the camera frequency domain is the 19 non-320 conditions. The frequency analysis
therefore has 19 conditions per camera and 114 condition-camera-target rows over three cameras and two targets.
RMS response trends use the pooled camera and laser table, which covers all 20 laser-matched conditions.
That table is not camera-specific (see the RMS subsection below).

Within every analysis the full set is reported first and the sensitivity subset second. The
sensitivity subset excludes 60 and 80 RPM (17 conditions), the two conditions flagged as a
regime-boundary region in the per-camera RMS package.

### Operational frequency correspondence (full set first)

For each camera and condition, the camera frequency was taken as the nearest of the stream's five
retained reference-blind peaks to the laser target frequency of that condition. This is the
operational matching rule of the existing exploratory comparison, not an independent frequency
estimate. The results describe operational correspondence between two non-simultaneous sessions. They are not a
measure of frequency accuracy, because no common-observable reference exists, and the "within one
Rayleigh interval" fraction describes record resolution, not estimator uncertainty.

**Bending target, 19 non-320 conditions (full set):**

| Camera scope | Conditions | Denominator (rows) | Median abs. difference (Hz) | Bootstrap interval of the median (Hz) | IQR abs. (Hz) | RMSE (Hz) | 90th pct. abs. (Hz) | Fraction within 0.1 Hz | Fraction within one Rayleigh interval |
|---|---|---|---|---|---|---|---|---|---|
| cam1 | 19 | 19 | 0.004003666240242 | [0.0020874502223426, 0.0284971790156873] | 0.029827673775614 | 1.1586551586600766 | 1.7293116268463922 | 0.7894736842105263 | 0.7368421052631579 |
| cam2 | 19 | 19 | 0.002952072722131 | [0.0011631640041129, 0.0281832269020776] | 0.0306605773490065 | 1.1489528427327809 | 1.7292216466242452 | 0.7894736842105263 | 0.7368421052631579 |
| cam1_cam2_pooled | 19 | 38 | 0.0034778694811865 | [0.0023801287706107, 0.0260700265398055] | 0.0312933717738762 | 1.1538141989751525 | 1.817479137340852 | 0.7894736842105263 | 0.7368421052631579 |
| cam3 | 19 | 19 | 0.0049045575413138 | [0.0005264408801739, 0.0281107394675974] | 0.0310693896349954 | 1.341013612384672 | 1.9398127335986823 | 0.8421052631578947 | 0.7368421052631579 |
| all_cameras | 19 | 57 | 0.004003666240242 | [0.0024167619058261, 0.0189218014472649] | 0.0336498384588276 | 1.219411322471398 | 1.9057366280574497 | 0.8070175438596491 | 0.7368421052631579 |

**Torsion target, 19 non-320 conditions (full set):**

| Camera scope | Conditions | Denominator (rows) | Median abs. difference (Hz) | Bootstrap interval of the median (Hz) | IQR abs. (Hz) | RMSE (Hz) | 90th pct. abs. (Hz) | Fraction within 0.1 Hz | Fraction within one Rayleigh interval |
|---|---|---|---|---|---|---|---|---|---|
| cam1 | 19 | 19 | 0.0246298297080618 | [0.0025458255926311, 1.4385068433476318] | 1.4583812194376076 | 1.3773993170024077 | 2.7988234299786967 | 0.5263157894736842 | 0.5263157894736842 |
| cam2 | 19 | 19 | 0.023282873756814 | [0.0024167619058261, 1.441184900404057] | 1.459592203338684 | 1.3771142505373195 | 2.798951922369608 | 0.5789473684210527 | 0.5263157894736842 |
| cam1_cam2_pooled | 19 | 38 | 0.0239563517324379 | [0.0028414753016039, 1.4119521782291071] | 1.4699853285108258 | 1.3772567911452935 | 2.8097431286180408 | 0.5526315789473685 | 0.5263157894736842 |
| cam3 | 19 | 19 | 0.8222189526124177 | [0.0029190608511853, 1.4788911383548915] | 1.4785428418416453 | 1.5626641529851075 | 2.8361694976669325 | 0.4210526315789473 | 0.4210526315789473 |
| all_cameras | 19 | 57 | 0.0596603080982838 | [0.004003666240242, 1.4119521782291071] | 1.4802963111597192 | 1.4417109965288148 | 2.820534334866472 | 0.5087719298245614 | 0.4912280701754385 |

**Sensitivity subset excluding 60 and 80 RPM (17 conditions), bending target:**

| Camera scope | Conditions | Denominator (rows) | Median abs. difference (Hz) | Bootstrap interval of the median (Hz) | IQR abs. (Hz) | RMSE (Hz) | 90th pct. abs. (Hz) | Fraction within 0.1 Hz | Fraction within one Rayleigh interval |
|---|---|---|---|---|---|---|---|---|---|
| cam1 | 17 | 17 | 0.004003666240242 | [0.002064588011521, 0.0284971790156873] | 0.0264325910041663 | 1.1656115610119615 | 1.3007409944255377 | 0.8235294117647058 | 0.7647058823529411 |
| cam2 | 17 | 17 | 0.002952072722131 | [0.0005119106628921, 0.0281832269020776] | 0.0276713162391855 | 1.154807227218813 | 1.3009273898067064 | 0.8235294117647058 | 0.7647058823529411 |
| cam1_cam2_pooled | 17 | 34 | 0.0034778694811865 | [0.0023434956353955, 0.023700220161965] | 0.0270714753760766 | 1.160221970831777 | 1.8681044810818848 | 0.8235294117647058 | 0.7647058823529411 |
| cam3 | 17 | 17 | 0.0049045575413138 | [0.0003503996940197, 0.0281107394675974] | 0.0277603397735777 | 1.3667848770423523 | 1.4193556011302555 | 0.8823529411764706 | 0.7647058823529411 |
| all_cameras | 17 | 51 | 0.004003666240242 | [0.0023434956353955, 0.0189218014472649] | 0.0277912523256534 | 1.2329275381942528 | 2.4352815723570664 | 0.8431372549019608 | 0.7647058823529411 |

**Sensitivity subset excluding 60 and 80 RPM (17 conditions), torsion target:**

| Camera scope | Conditions | Denominator (rows) | Median abs. difference (Hz) | Bootstrap interval of the median (Hz) | IQR abs. (Hz) | RMSE (Hz) | 90th pct. abs. (Hz) | Fraction within 0.1 Hz | Fraction within one Rayleigh interval |
|---|---|---|---|---|---|---|---|---|---|
| cam1 | 17 | 17 | 0.019987286105449 | [0.0023523719239118, 1.4119521782291071] | 1.409599806305195 | 1.2349429110662005 | 2.044599081402505 | 0.5882352941176471 | 0.5882352941176471 |
| cam2 | 17 | 17 | 0.0180935018085031 | [0.0023271622597986, 1.4120210650171423] | 1.4096939027573436 | 1.2344979960702973 | 2.0437586872061884 | 0.6470588235294118 | 0.5882352941176471 |
| cam1_cam2_pooled | 17 | 34 | 0.019040393956976 | [0.0025458255926311, 0.7619220599383959] | 1.409658128612609 | 1.2347204736081443 | 2.464643238563183 | 0.6176470588235294 | 0.5882352941176471 |
| cam3 | 17 | 17 | 0.1949074458595951 | [0.0015350769040467, 1.4412956250692204] | 1.4397605481651736 | 1.460764480557145 | 2.118939889789716 | 0.4705882352941176 | 0.4705882352941176 |
| all_cameras | 17 | 51 | 0.023282873756814 | [0.0029190608511853, 1.362655797373515] | 1.4232236304471813 | 1.314394938561926 | 2.8852815723570657 | 0.5686274509803921 | 0.5490196078431373 |

*Reading guide for the authors:* for the torsion target the median absolute difference and the RMSE
differ in magnitude within the same row, and the within-0.1-Hz fractions are well below those of the
bending target. Report both columns; do not quote the median alone. The cam3 torsion row is
reported separately from the cam1/cam2 rows and is not pooled with them.

### Cam1/cam2 same-marker repeatability (kept separate from cam3)

Cam1 and cam2 view the same physical marker. Their paired condition-level differences are therefore a
repeatability measure of the two processing branches, not a comparison against an external quantity.

Full non-320 set (19 conditions): median absolute dominant-frequency
difference 0.0007699814667248 Hz (bootstrap interval
[0, 0.0008057945582009] Hz), median signed difference
0 Hz, median cam1/cam2 pixel-RMS ratio
1.0031270675030413 (bootstrap interval [1.0028541311843655, 1.003366501352062]),
mean relative difference -0.0041259178027719.

Sensitivity subset excluding 60 and 80 RPM (17 conditions): median absolute
difference 0.0007699814667248 Hz (bootstrap interval
[0, 0.0015954252525349] Hz), median pixel-RMS ratio
1.0031270675030413 (bootstrap interval [1.0028541311843655, 1.003366501352062]).

The paired permutation test returned p = 1 in both subsets. Treat this as the
absence of a detectable paired difference. It is not evidence of equivalence and should not be
presented as a significance result. In the per-camera RMS package (millimetre H1,y RMS, 19 conditions) the cam1/cam2
geometric-mean ratio is 0.99233251 for H1,y and
0.94715786 for H2 roll. This is an RMS-magnitude comparison and
carries no phase information. Repeatability here is the strongest basis for the same-marker claim
in the statistical layer and is not accuracy.

### Cam3 observation-path dependence (kept separate from repeatability)

Cam3 views a distinct centre marker (handwritten label ID-0-2) and has its own calibration and timebase.
Its relative response is reported against the cam1/cam2 mean and is never averaged into the same-marker
pair (cam1/cam2 view one side/off-center marker, handwritten label ID-0-1). Both markers decode as
AprilTag ID 0.

Full non-320 set (19 conditions): median relative RMS
0.8908842763400092, mean 0.6423009215488505, IQR 0.7964858139087587,
bootstrap interval [0.2413190631676434, 0.9821956306014332]; mean frequency difference
-0.8983608968599353 Hz.
Sensitivity subset excluding 60 and 80 RPM (17 conditions): median relative RMS
0.6281554151879927, mean 0.5976607978657471, bootstrap interval
[0.1354117902954124, 0.9799020398030336].

In the per-camera RMS package the cam3/cam1 H1,y geometric-mean ratio is
0.45815262 and the cam3/cam2 ratio is
0.45463974 (Spearman
0.64912281 and
0.64912281); for H2 roll the cam3/cam1 and cam3/cam2 geometric-mean
ratios are 1.5857591 and
1.5019642. These differences show observation-path
dependence. They do not identify a unique torsional mode or a marker-location effect, because
marker location and camera channel are confounded (as stated in the cam3 subsection above).

### Side-marker lever arm and the cam3 heave proxy

Cam1 and cam2 view the same side/off-center marker (handwritten label ID-0-1). Their H1,y displacement is
the vertical metric motion of that marker. It includes a lever-arm x roll term and must not be called
direct heave. Cam3 views a distinct centre marker (handwritten label ID-0-2) and is treated as the heave
proxy. Both markers decode as AprilTag ID 0, so the decoded ID cannot tell them apart. Any near-axis
statement for cam3 is data-derived and qualified: the apparent distance from the rotation axis estimated
from the data is about 6 mm (median), against about 125 mm for cam1/cam2, and the physical separation
between the markers was not surveyed. The cam3 role is further limited by the camera's separate
calibration, and by the 60 Hz sampling and approximately 30 s record, which bound the band that cam3
can represent (the laser reference is sampled at 360 Hz over 100 s).

Against the laser heave channel of the dataset labelled y2025 in the repository (the primary session of the per-camera
package, selected on dataset naming only), the cam3 H1,y geometric-mean ratio is
0.51522643 with Spearman rank correlation
0.72631579 over
19 conditions. For the dataset labelled
y2024 the corresponding values are
0.77336996 and
0.6754386. Report both sessions. The sessions are not simultaneous with the camera
campaign. The camera RMS scale carries a provisional +/-2.5% bound (ruler graduation unconfirmed), and
the laser's own scale uncertainty is not propagated. These are response-trend correspondences, not calibration.

### Pooled RMS response-trend correspondence (full set first)

The pooled camera and laser table does not provide camera-specific common-unit RMS for cam3, and
`RMS_SCALING_RESULTS.csv` records the cam3-separate scope as unavailable (0 conditions). The
statistics below therefore describe response-trend association between the pooled camera source and the
laser source. Pearson r describes linear trend association and Spearman r monotonic trend association.
Neither establishes equality, calibration, causality or accuracy, and ratios are not expected to equal
one without a validated common-unit calibration. The regression is descriptive.

| Target | Subset | Conditions | Pearson r | Spearman r | Winsorized r | Bootstrap interval of r | Slope | Bootstrap interval of slope | Intercept (mm) | R squared | RMSE (mm) | Median camera/laser ratio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bending | full_20 | 20 | 0.9020313613196936 | 0.7574276579267276 | 0.8783802215200656 | [0.419145948035248, 0.994953488645998] | 1.101232008063506 | [0.4516720467172024, 1.2753378906786703] | -0.0714499343844834 | 0.8136605768042605 | 0.4777453893027121 | 1.0284 |
| bending | non_320 | 19 | 0.8149096630940669 | 0.7169812010977267 | 0.8149096630940669 | [0.2573985010046056, 0.9945252187564736] | 0.898730652111046 | [0.2474278922461218, 1.1746100785153073] | 0.0672000129942017 | 0.6640777590040857 | 0.4398867611460692 | 0.9977 |
| bending | non_320_excl_60_80 | 17 | 0.9901473099099272 | 0.9503373950556911 | 0.9901473099099272 | [0.9596283339681486, 0.9975246900969352] | 1.107034405831566 | [1.060158393584406, 1.2105386043901716] | -0.0542574870544921 | 0.9803916953218658 | 0.1329888252713694 | 0.9977 |
| torsion | full_20 | 20 | 0.9921078682892276 | 0.9477247755587654 | 0.836172269088646 | [0.8453000234568645, 0.9993449642099824] | 0.6466154688624987 | [0.5871294231654287, 0.7063997557687745] | -0.0307957495532924 | 0.9842780223213958 | 1.5666651757794323 | 0.6375500000000001 |
| torsion | non_320 | 19 | 0.9431287730261608 | 0.9390084273862516 | 0.815865446017355 | [0.7798792336225138, 0.9945137684478038] | 0.6548922888861402 | [0.5367655166153811, 0.7311308379770723] | -0.0409299796758514 | 0.8894918825098316 | 0.754840902372637 | 0.6313 |
| torsion | non_320_excl_60_80 | 17 | 0.9875199990429768 | 0.9871246490578468 | 0.8961266765393597 | [0.9663019895417354, 0.9960252832435588] | 0.675398491790757 | [0.6326361751869707, 0.7500210299493506] | 0.0060584262156678 | 0.9751957485098408 | 0.6468777446091248 | 0.6446 |

Leave-one-condition-out summaries (range over single-condition removals, reporting minimum / median /
maximum) are given in `LEAVE_ONE_CONDITION_OUT.csv`. For the bending target on the full 20-condition
set the Pearson minimum, median and maximum are
0.8149096630940669 / 0.9015833448077109 / 0.9800179810589356
(maximum reached on removing 60 RPM, minimum on removing
320 RPM), and for the sensitivity subset
0.978592269733537 / 0.9901810356543532 / 0.9938427897097324.
The influence diagnostic inspected 60, 70, 80, 300 and 320 RPM and carries no causal interpretation.

### Mathematical forced-alignment stress test

The forced-alignment diagnostic reuses the corrected pre-existing outputs: a lag was estimated on the
first 60% of each record and applied unchanged to the last 40%, after interpolation onto a common mathematical
grid. It covers 114 condition-camera-target rows (three cameras x two targets x 19 non-320
conditions), of which the 60/80 RPM rows are labelled `non_320_including_60_80` in
`STATISTICAL_COMPARISONS.csv`. Training and held-out correlation, standardized RMSE and (where
defined) conditional coherence and phase are diagnostics of this mathematical procedure. They do not
recover a physical shared clock, do not establish synchronization or simultaneity, and are not
waveform validation. The obsolete r_test = -0.118 result is not used. Per-row values are in the CSV and
in the figure 08 plot; no summary statistic over the 114 rows exists in the validated package (see OI-07).

### Claim boundary for this subsection

Permitted: condition-level statistical characterization of camera spectral-feature repeatability,
response-trend correspondence, observation-path dependence and processing sensitivity.
Not permitted: camera accuracy, simultaneous validation, synchronized exposure, calibration, a unique
torsional or bending mode, structural modal identification.
