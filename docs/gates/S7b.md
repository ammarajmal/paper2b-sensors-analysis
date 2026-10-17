Stage: S7b (Monte Carlo uncertainty propagation and statistical consistency tests)   Date written: 2026-10-18 (BEFORE any of it is computed)
Literature basis (docs/LITERATURE_LEADS.md, excerpt-level, unverified): JCGM 101 (Monte Carlo), ISO 13528 En score, Birge ratio / random-effects dark uncertainty, Passing-Bablok and Deming, jackknife influence.
PART 1  Monte Carlo through the estimators (N = 200 draws per stream and condition; seed 11)
 Streams: all 19 compared conditions (20-300 RPM) x 3 cameras; laser side for both sessions. Estimators: Q1 heave = P1_y_mm line amplitude at f_h; Q2 pitch = P5_roll_rad line amplitude at f_alpha, then the camera mean over cameras (as in S6). The Monte Carlo uses the same line_amplitude routine as S6 (half-width 0.08 Hz).
 Perturbed inputs and their distributions (each documented with its source):
  corner position noise: independent Gaussian on each of the 8 corner coordinates per frame, SD per camera from the e0_0rpm record = SD of the frame-to-frame difference of each corner coordinate divided by sqrt(2) (robust to slow motion and the common-mode line);
  timestamp noise: Gaussian on every record stamp, SD per camera = the S1 header-to-record latency SD (0.7-1.4 ms), i.e. the part of the stamp that is not exposure time;
  tag size: rectangular +/- 2.5% about 20 mm (owner decision T; ruler supports about 1%): heave only; pitch does not depend on it;
  laser: white noise added to the volts with the SD of the session's bias record; spacing d rectangular +/- 15% (pitch only).
  Intrinsics: no calibration covariance exists in the bags (camera_info is a single value set) and the static bags use another zoom (NOTES F16), so intrinsics are NOT drawn. Instead a deterministic sensitivity is reported: distortion coefficients from the bag versus zero, and fx, fy +/- 5%, on e0, e7, e14 (change of line amplitude), labelled sensitivity, not uncertainty.
 Output: per condition and quantity, MC standard deviation of the camera amplitude and of the laser amplitude (relative), and the MC standard uncertainty of the ratio.
 Criterion S7b-1: for the components that both approaches contain (camera: scale C1, timebase C4, noise C7; laser: spacing L1, noise L3) the median over rule-a conditions of MC relative SD divided by the GUM quadrature sum of the same components lies between 0.5 and 2 for each quantity; otherwise the difference is explained in the result text. The MC-only component (corner noise through the whole estimator, including its effect on the fitted amplitude) is reported separately.
PART 2  Consistency tests on the existing S7 budget (results/s7_budget_by_condition.csv), both lasers, rule a and all 19, quantities Q1 and Q2
 T1 En per condition: En = ln(camera/laser) / (2 u_R), k = 2 (ISO 13528 form on the log scale); report the share with |En| <= 1 and the list of conditions with |En| > 1.
 T2 Birge ratio: sum((ln ratio / u_R)^2) / n, and the random-effects (REML) estimate of the common bias mu and the dark between-condition SD tau of ln ratio with weights 1/(u_R^2 + tau^2); 95% intervals by a bootstrap over conditions (2,000, seed 11). tau is the unexplained component; it is reported, not subtracted from any result.
 T3 Laser-versus-laser: the same statistics on ln(laser 2025 / laser 2024) with u = sqrt(u_L2025^2 + u_L2024^2) (same RPM, different sessions): how much of the session effect the quantified laser components explain.
 T4 Camera-versus-camera: cam1 versus cam2 (same marker) per condition on the P1 line amplitude: ln ratio against sqrt(2) times the spread expected from the camera noise, Birge ratio.
 T5 Robust slope: Passing-Bablok (Part I) slope and 95% CI for camera versus laser (all 19 and rule a), next to the Deming slope already in S6; a difference above 15% is reported as evidence of outlier or variance-ratio problems.
 T6 Influence: leave-one-out on the Pearson r (log scale), the Deming slope and E for each of the 19 conditions; the three conditions with the largest influence are named.
 T7 Paired permutation (sign-flip, 10,000 draws, seed 11) of the 2025-versus-2024 closeness difference dE per quantity, replacing the bootstrap P as a cross-check.
 T8 Repeat recordings: the 5-second bags against the main bags at the same condition, line amplitude in a +/- 0.15 Hz search (the 5 s resolution is 0.2 Hz), reported for conditions with amplitude above the rule-a floor; informational.
Pass criteria (machinery): all parts run for all conditions with no missing value; two runs identical; criterion S7b-1 as stated; every test writes its inputs and outputs to results/s7b_*.csv.
Not a criterion: any test statistic value; failed consistency is a finding.
Result: (filled after the run)
