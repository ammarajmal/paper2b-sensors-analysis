Stage: S1b (timing census of the 20 static bags)   Date written: 2026-10-18
HONEST STATUS: the census table results/s1_census_static.csv was produced and committed on 2026-10-16 (commit 031c293) without a gate file, and its flag columns (clean, low, drops) came from an ad hoc step that is not in the repository. This file fixes the flag definitions now, BEFORE the counts are recomputed under them, and records the plan's pre-written target (docs/STAGE_PLAN.md: 5 clean bags, 7 below 55 Hz, 8 with dropped frames; earlier extraction, SHARED_FACTS B4). The earlier extraction's own definitions are not recorded, so the counts need not reproduce and the definitions below are not tuned to reach 5/7/8.
Data: 20 static bags (5 cam1, 10 cam2, 5 cam3), recomputed from the bags by `bvp census static` (read-only), columns as in results/s1_census_static.csv. Different intrinsics from the wind-tunnel set (NOTES F16); not pooled.
Definitions (physical, fixed now):
 low: mean frame rate (n-1)/duration of the record stamps below 55 Hz (the plan's threshold).
 dropped: any missing sequence number (seq_missing > 0). Alternative reported alongside: any inter-frame gap above 2.5 nominal intervals (n_gap_gt2p5 > 0).
 clean: mean rate between 59.9 and 60.1 Hz AND seq_missing = 0 AND no gap above 2.5 nominal intervals.
Pass criteria: (1) the table is reproduced from the bags: every column equal to the committed table (max abs difference 0); (2) the counts under the definitions above are reported per camera, with the plan's target beside them; (3) record stamp equals header stamp in every static bag (stated earlier: unlike the campaign) is re-verified; (4) no duplicate payloads are found in cam3 static bags (counter-check of the campaign duplicate frames, B3).
Not a criterion: reaching 5/7/8. A different count is reported with the reason (definition or data), not forced.
Result: (filled after the run)
