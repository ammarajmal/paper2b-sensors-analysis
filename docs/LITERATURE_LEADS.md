# Literature leads (web search 2026-10-16; abstracts/excerpts only, NOT read in full; verify before citing)
| Topic | Lead | What it may give us | Status |
|---|---|---|---|
| Uncertainty budget | "Vision-Based Displacement Measurement for Structural Health Monitoring: A Metrology-Oriented Review of Uncertainty Quantification", Buildings 16(13), 2659 (2026) (mdpi.com/2075-5309/16/13/2659) | GUM + Monte Carlo (JCGM 101) budget template: scale factor, subpixel localization, intrinsics, extrinsics, rolling shutter, platform motion, reference sensor. Maps onto SVR S09.2. | excerpt read |
| Marker accuracy | FMAC: Fair Fiducial Marker Accuracy Comparison, arXiv:2601.07723 | Uses AprilTag 3.4.5; reports mean pose bias and a possible constant half-pixel XY offset in that release; depth overestimated. A constant offset cancels in displacement but matters for absolute pose and scale. | excerpt read |
| Planar-marker pose | Rijlaarsdam et al., Front. Robot. AI 9:838128 (2022), doi:10.3389/frobt.2022.838128 | Pose ambiguity and loss of precision for frontal views of planar markers; relevant to our near-orthographic telephoto view (fx 20,000-26,000 px) | excerpt read |
| AprilTag state estimation | "Analysis and Improvements in AprilTag Based State Estimation", Sensors 19, 5480 (PMC6960891) | Orientation uncertainty dominates accuracy loss | excerpt read |
| Spectral significance | VanderPlas, "Understanding the Lomb-Scargle Periodogram", ApJS 236:16 (2018), doi:10.3847/1538-4365/aab766; astropy docs | False-alarm probability (Baluev 2008, bootstrap); states that periodogram frequency uncertainty is generally not a symmetric +/- and that FAP is not the probability the data are periodic. Use bootstrap/sinusoid-fit for frequency uncertainty and say so. | excerpt read |
| Bridge-deck section-model testing | wind-tunnel flutter-derivative papers (PMC5336026, MDPI Appl. Sci. 11(4):1642) | Context for heave/pitch and flutter derivatives; the search found NO video-marker section-model paper | gap NOT proven (search engine limits) |
| Earlier session leads | Xu et al. 2026 (Measurement, doi:10.1016/j.measurement.2026.121753); Mittal & Sadhu 2025 (J. Sound Vib. 612:119152); Zhu et al. 2026 (IEEE Sens. J., doi:10.1109/JSEN.2026.3716296); Rehfeld et al. 2011 | direct comparators / irregular-sampling spectra | see project kit |

## Ideas for the codebase taken from these leads
1. Uncertainty stage = GUM table (Type A/B per component) + Monte Carlo through the whole pipeline with synthetic noise at the measured static RMS (0.02-0.09 px) and a draw of intrinsics from an envelope.
2. Pose stage: report in-plane displacement from corner geometry (scale-factor estimator) next to the PnP pose; report the spread as the pose-ambiguity component. Flag frames where IPPE's two solutions have similar reprojection error.
3. Spectral stage: Lomb-Scargle (generalized, floating mean) with Baluev FAP and a bootstrap frequency interval; replace "peak within one bin" counts by condition-level tables with a shuffle baseline.
4. Add the vendor 2024 camera (NOTES F7) as a within-session comparison once its time column is understood.
