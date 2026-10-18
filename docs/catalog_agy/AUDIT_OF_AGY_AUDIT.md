# Check of the third agy pass (G1 and G2), 2026-10-19
Method: independent script (read-only) over docs/catalog_agy/audit/records_*.jsonl plus reading of the summary files.
- Records: 729 (G1 + G2 only; G3 LifeOS, G4 Logseq notes, G5 AI-session archives NOT done). Skipped 480 (SKIPPED.csv), unreadable 0.
- Paths: 729 of 729 exist.
- Descriptions: 655 distinct of 729; the most repeated template (CSV frame-metadata exports) appears 11 times, which is legitimate because those files are the same kind of export. None of the descriptions appears verbatim in its file (0 of 729), so the first-line-copy problem of the first pass is gone.
- Quotes: 90 quotes from 60 randomly drawn records, all found character for character in the files (0 not found).
- Facility and vendor names: not checked beyond the agy self-report.
Findings against the agy chat report (the files are better than the chat summary):
1. The chat says the voltage scaling is "0.02 mm/mV"; no file in audit/ contains that. PAPER2_COVERAGE.md quotes the vendor script as "pvolt = 2.7; % cm/V" (= 27 mm/V). Use the file, not the chat sentence.
2. The chat says the audit "confirms" tag sizes 20 mm (2025) and 35 mm (2024). The files only quote a Decision_Log statement and a config value (NUMBERS_FOUND.csv: "the 2025 campaign's 20mm tag size"; "tag_size_m: 0.020"). That is a statement in a file, not a verification; the rebuild still treats 20 mm as an assumption (decision B1).
3. The chat says the audit "disproves" the 0.938 Hz peak and "reconciles" mechanical versus optical for the 9 Hz line. PAPER2_COVERAGE.md itself is more careful: it states that no file identifies the 9 Hz line as an electrical/mechanical facility artifact. The 0.938 Hz statement is the file's own conclusion (grid resolution artifact), quoted, not independently tested here.
4. Historical numbers in the audit (19-condition Spearman 0.691, Pearson 0.616; Tunnel A dside 100 mm) are printed or earlier values from older files; they are not the rebuilt values (rebuilt 2025-laser values are in the progress report). Do not mix them.
5. The audit folder contains 43 helper scripts. Several hold hand-typed record text inside Python lists (e.g. build_part01_p1.py) plus a quote verifier; the prompt forbade generating descriptions by script. The descriptions are specific (see above), so this looks like a way of writing records in bulk, not computed text, but it is a deviation from the instruction.
6. NUMBERS_FOUND.csv has 31 rows. It covers frequencies, frame rate, tag size, marker separation, laser spacing, record length, noise floor, wind speed at the highest RPM and focal length. The laser calibration factor row requested in the prompt is missing as a separate quantity (it appears only inside the coverage text).
Verdict: usable as an evidence index for G1 and G2 after the caveats above. Not a substitute for the rebuild numbers.
