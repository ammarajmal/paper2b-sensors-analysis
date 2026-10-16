# How to use the repository catalogue (2026-10-16)
What it is: a read-only scan of 15 older trees (3,197 files; 1,564 unique code/doc files) with a local model (qwen3:8b on your GPU). Nothing was sent off the machine.
Quality: mean evidence-trust 0.85; 88% of summaries score >= 0.5 (share of the model's quoted evidence found in the file). 4 files failed to parse and 46 have trust 0 (listed by `bvp scan status` and in catalog.csv, mostly vendor C/C++ sources). Where the local summary and agy's catalogue disagree most, agy's "purpose" is usually a junk copied line (e.g. "=== Config ==="), so the local one is the primary. Both are machine-generated: open the file before relying on anything.

Files here
- `INDEX.md`, `CATALOG_<tree>.md`: per-tree tables (purpose, status (model guess), tags, reuse (only where WE decided it, see `config/reuse_overrides.csv`), flags, trust) and folder summaries.
- `catalog.csv`: everything in one sheet (filter by `label`, `tags`, `trust`).
- `results_index.csv`: 1,122 result folders (file counts, sizes, dates, CSV headers, JSON keys, scripts that name the files).
- `cross_check_low_agreement.json`: 60 files where local and agy descriptions differ most.
- `../catalog_agy/`: agy's catalogue and our audit of it (`AUDIT_OF_AGY_OUTPUT.md`).

Ask questions (cites catalogue entries and prints source paths; verify the answer in the files)
```
cd /mnt/space/adev/projects/active/bridgedeck-vision-pipeline
uv run bvp scan ask "what spectral estimators were tried?"
uv run bvp scan status
```
Re-run or extend: `scripts/run_full_scan.sh` (resumable; `MODEL=qwen3:14b` for a slower, slightly better pass; add roots in `config/scan_roots.yaml`).
Known answer limits: retrieval may return a plan instead of the results file (static-noise-floor question), and the answer text can overstate (a 9 Hz answer said "not an artifact"; the source only says it cannot be assigned to camera or deck). The SOURCES list is the useful part.
