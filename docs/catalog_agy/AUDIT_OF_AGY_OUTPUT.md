# Audit of agy's catalogue (2026-10-16, done by checking its files against the sources)
Scope: 2,095 entries in catalog_1..14.jsonl, plus its summary documents.
Good (verified):
- All 2,095 lines are valid JSON, all paths exist, and all 3,356 numbers listed in `key_results` occur in the files.
- Cross-tree duplicates were found by content hash (1,153 files) and linked in `also_at`.
- It stayed read-only on the scanned trees (only `.git/index` timestamps changed, which `git status` does).
Weak (measured):
- It generated most entries with its own 656-line Python parser (`catalog_parser.py`), not by reading each file: purpose is a line copied from the file in 1,051 entries (50%), a boilerplate template in 578 (28%, e.g. "Configuration file specifying parameters for summary.json." x255), and a real description in 466 (22%).
- `method` is a list of function names, not methods; only 14 of 692 code entries list outputs. 462 entries have no evidence quote, and some quotes are trivial (e.g. "from pathlib import Path").
- Tree 3 (the `omrpr` results folders) has 351 of 395 entries as the template.
- `WHAT_EXISTS_FOR.md`: 12 of 49 listed file paths do not exist (e.g. tree 6 `scripts/analyze_frequencies.py`, tree 11 `reports/timing_jitter_analysis.md`, tree 9 `src/charuco_calibration/src/calibrate.py`). It also says the ~9 Hz line was "identified as an electrical/mechanical facility artifact", which no file supports and which its own OVERVIEW.md contradicts (several entries call it unresolved). Its Hamming-tolerance statement (<= 1) conflicts with the Sensors-line reports (maxhamming 0).
Use: the JSONL and `also_at` as an inventory and duplicate map; OVERVIEW.md rows only where the quoted source line is shown; do NOT use WHAT_EXISTS_FOR.md or the TREE summaries as facts without opening the cited file.

## Second pass (refine/, checked 2026-10-16)
`WHAT_EXISTS_FOR_v2.md` and `VALUE_CONFLICTS.md`.
- Paths: 69 distinct cited paths, all exist (first-pass file had 12 of 49 missing). Quotes: none over 15 words; no facility name in prose.
- Quotes: 99 of 140 (about 70%) match their cited file almost word for word; the rest are reformatted or paraphrased text in quote marks (table pipes, spacing, "..." joins). Numbers inside quotes: 256 of 266 (96%) occur in the cited file. Rounded or derived values (0.8824 -> 0.882, 1122/1829 -> 61.35%) account for several misses.
- Not found in the cited file: Spearman 0.6912 attributed to `01_Project_Constitution.md`; the statements "D2 (20 RPM), D4 (40 RPM)" and "D02 was mapped to 40 RPM instead of 20 RPM" attributed to `01_Project_Constitution.md` and `claim_boundary.md`. Open the file before using these.
- The DISAGREES flag is applied to nearly every row (all 12 quantities), so it carries no information. Use the value lists, not the flags.
- New and useful: several camera-intrinsics families exist (WTT bag values fx 20,327.9; a static-test file with fx 36,498.25; ChArUco-based 56,874 and 37,916; a placeholder fx 2108; plumb-bob 789.4). The static bags may not share the WTT intrinsics: check before pooling them.
Verdict: usable as a lead list for locating files; every value still needs the cited file open.
