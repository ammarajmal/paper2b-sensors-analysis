# Tree 14 Summary: Legacy Code and Software (Unfiltered historical code archives and early utility scripts)

## Overview and Scope
Tree 14 contains 126 total scanned files (126 catalogued, 0 identical duplicates).
Legacy Code and Software (Unfiltered historical code archives and early utility scripts).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `codes_unfiltered/TESolutionbig/TESolution/NEW/chec.py`
- `codes_unfiltered/roscodes/get_robot_loc.py`
- `codes_unfiltered/roscodes/listener.py`
- `codes_unfiltered/roscodes/robot_move.py`
- `codes_unfiltered/roscodes/talker.py`
- `codes_unfiltered/testcode/test.cpp`

## Key Results and Stated Findings
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_2s_2025-03-22_01-13-28_analysis.txt`**: "Average Interval Cur Time: 0.016674 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_2s_2025-03-22_01-13-28_analysis.txt`**: "Max Interval Cur Time: 0.022763 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_5s_2025-03-22_01-13-56_analysis.txt`**: "Average Interval Cur Time: 0.016689 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_5s_2025-03-22_01-13-56_analysis.txt`**: "Max Interval Cur Time: 0.024292 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_5s_2025-03-22_01-14-51_analysis.txt`**: "Average Interval Cur Time: 0.025342 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_5s_2025-03-22_01-14-51_analysis.txt`**: "Max Interval Cur Time: 0.069054 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_5s_2025-03-22_01-16-01_analysis.txt`**: "Average Interval Cur Time: 0.016690 s"
- **`codes_unfiltered/TESolutionbig/TESolution/2/Static_Exp1_5s_2025-03-22_01-16-01_analysis.txt`**: "Max Interval Cur Time: 0.024158 s"

## Planned or Missing Elements
- No explicit unresolved tasks or unverified assumptions flagged.

## Duplicate Files Across Trees
- No cross-tree duplicate files identified in this tree.
