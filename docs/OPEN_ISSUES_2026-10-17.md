# Open-issue checks (2026-10-17): tag size, camera scale sensitivity, laser head spacing
Script: scripts/open_issues_check.py; output: results/open_issues_check.txt; figure: results/figures/ruler_ticks_cam1.png. All three are consistency checks. Nothing here changes a pipeline value.

## 1. Tag size (the 20 mm assumption)
Independent scale: the images contain a metal ruler with graduation marks. In cam1 the tag is mounted on the ruler (same plane); in cam3 a ruler runs along the bottom of the view (not necessarily the same depth).
Measured (e0 frame 0, tick positions by a comb fit on the ruler's tick band): tick period 72.08 px (cam1), 72.26 px (cam3); tag side 289.92 px and 292.44 px. Tag side / tick = 4.022 (cam1) and 4.047 (cam3). With 5 mm ticks the tag is 20.1 mm (cam1) and 20.2 mm (cam3).
Assumption: each tick is 5 mm. Basis: the printed numbers 10 and 5 are about 10 ticks apart (read as centimetres); a 35 mm tag would need 8.75 mm ticks, which no ruler has. The owner can confirm the graduation from the physical ruler.
Further evidence: the acquisition GUI committed on 2025-10-02 sets tag_size 0.02 m (ledger section J); the standoff computed from 20 mm (1.40 to 1.78 m) matches the standoff in the Measurement paper (possibly the same source, so only weak support).
Conclusion: 20 mm is supported to about 1% by an independent scale. Carry 2.5% in the budget until the ruler graduation is confirmed, then reduce.

## 2. Camera scale sensitivity
Heave amplitudes scale linearly with the tag size; the roll (pitch) angle does not depend on it. On the primary heave error E (arm A, 19 conditions): 2025 laser 0.448 / 0.445 / 0.442 for -2.5% / 0 / +2.5%; 2024 laser 0.566 / 0.568 / 0.571. So +/-2.5% moves E by at most 0.003.
The scale that would minimise E is x1.33 (26.5 mm) against the 2025 laser and x0.74 (14.9 mm) against the 2024 laser, with 95% intervals [0.88, 2.00] and [0.50, 1.39]: opposite directions, both intervals include 1.0, and E improves only from 0.445 to 0.427 and from 0.568 to 0.554. The laser comparison cannot determine the tag size, and the tag size is not what drives the heave disagreement (the regime-boundary conditions are).

## 3. Laser head spacing d
Pitch from two heads is (side - centre) / d for a rigid rotation about ANY axis: d is the separation of the two beam spots; where the rotation axis lies, and whether the heads look symmetric about the deck centre, do not matter. Therefore the question is only whether d is the full spacing or half of it.
Test with an angle that needs no length: the camera in-plane roll. Strong-torsion conditions (both instruments' dominant peak within 0.1 Hz of the torsion line and both pitch amplitudes > 0.004 rad: 90, 140, 160, 180, 200, 220 RPM, both sessions):
 2025: camera/laser pitch ratio median 1.12 with d = 13 cm. If the vendor's halving were right the ratio would be about 0.56. Implied d = 11.7 cm [10.5, 12.5].
 2024: ratio median 1.19 with d = 10 cm; the halving would give about 0.60. Implied d = 8.4 cm [5.9, 8.9].
So the full difference over 13 cm (10 cm) is supported; the vendor's half is off by a factor 2. Both sessions imply d about 10-16% smaller than the vendor value, and the vendor value lies just outside both intervals. Possible reasons (not separable here): beam-spot spacing differs from the housing spacing; laser calibration (2.7 cm/V); different lock-in amplitude in the separate recordings; camera roll bias. The heave comparison involves no d and shows no such systematic offset (mixed ratios), which argues against a calibration error and for d or session effects.
Treatment: use the vendor values 13 cm and 10 cm as inputs, carry +/-15% on d in the budget, report the camera-implied spacing as a consistency check, and do NOT tune d to the camera. A measurement or a vendor drawing of the beam-spot spacing would settle it.
The 2024 vendor photograph (Displacement Measurement System_V2.pdf, page 2) shows ch1 and ch2 on an overhead rail with no dimension.
