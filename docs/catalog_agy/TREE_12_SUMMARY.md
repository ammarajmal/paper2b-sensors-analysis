# Tree 12 Summary: PhD Research Advisory (Foundational evidence, supervisory guidelines, and validation reports)

## Overview and Scope
Tree 12 contains 894 total scanned files (221 catalogued, 673 identical duplicates).
PhD Research Advisory (Foundational evidence, supervisory guidelines, and validation reports).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `05_TARGETED_A_BLOCKERS/scripts/bag_timestamp_audit.py`
- `05_TARGETED_A_BLOCKERS/scripts/timestamp_sensitivity.py`
- `05_TARGETED_A_BLOCKERS/scripts/verify_s4_windowed.py`
- `05_TARGETED_A_BLOCKERS/scripts/verify_s5_background.py`
- `05_TARGETED_A_BLOCKERS/scripts/verify_sweep_independent.py`
- `06_CLAUDE_EVIDENCE_AUDIT_2026-10-11/scripts/audit_check.py`
- `06_CLAUDE_EVIDENCE_AUDIT_2026-10-11/scripts/audit_nominal.py`
- `_work/stage/CLAUDE_SCIENTIFIC_AUDIT/20_FIGURES/producers/49_pass3_tables_figures_build.py`

## Key Results and Stated Findings
- **`01_SOURCE_OF_TRUTH/CANONICAL_DOCUMENTS.md`**: "Abstract (working tree) claims a 10-day camera/LDS interval and "17 regime-interior conditions (70–300 RPM)" with r≈0.974."
- **`01_SOURCE_OF_TRUTH/CANONICAL_DOCUMENTS.md`**: "The DEC-02 rationale cites outcome-dependent benefits (300 RPM "now a valid, highly correlated interior condition")"
- **`01_SOURCE_OF_TRUTH/VERSION_CONFLICTS.md`**: "VC-03 | P2-V4 (2026-10-10): v3.1 headline numbers (r≈0.974, RMSE≈0.21 mm) not reproducible"
- **`01_SOURCE_OF_TRUTH/VERSION_CONFLICTS.md`**: ""17 interior conditions (70–300 RPM)" impossible (15 setpoints)"
- **`02_EVIDENCE/ANALYSIS_DEPENDENCY_MAP.md`**: "py  (AprilRobotics v3.4.5 tag36h11, 0.020 m)"
- **`02_EVIDENCE/ANALYSIS_DEPENDENCY_MAP.md`**: "csv  (reference freq 1.4303 / 3.1036 Hz from 2024 lineage)"
- **`02_EVIDENCE/CLAIM_EVIDENCE_GAPS.md`**: "py` was not executed, so peak frequencies, Rayleigh bins and the frozen-peak tables (22/25A) are not independently recomputed"
- **`02_EVIDENCE/CLAIM_EVIDENCE_GAPS.md`**: "5. **Post-hoc reference comparison (25B)**: depends on 2024 facility-derived frequencies 1.4303 / 3.1036 Hz"

## Planned or Missing Elements
- `00_DISCOVERY/BASELINE_REPORT.md`: `/mnt/phd-legacy/phd_master` does not exist: `phd_master` lives only on the new
- `00_DISCOVERY/BASELINE_REPORT.md`: that one plain `git status` may have refreshed
- `02_EVIDENCE/CLAIM_EVIDENCE_GAPS.md`: raw-difference range | 332/332 MATCH, 0 mismatches (`TABLE_CELL_CHECKS
- `02_EVIDENCE/COMMON_CONTEXT/PAPER_RELATIONSHIPS.md`: | which spectral features does each camera channel see
- `02_EVIDENCE/PACKAGE_DOCS/GEMINI_POLICY_QUESTIONS.md`: Paper 1 is published (IEEE Access, 11 May 2026, CC BY 4

## Duplicate Files Across Trees
- `_work/stage/CHATGPT_RESEARCH_MENTOR/10_SENSORS_REVIEW_TARGET/figures/SOURCE_SCRIPT_HASHES.txt`: identical to Tree 1 (`manuscript/final_candidates/synthesis/figures/producers/SOURCE_SCRIPT_HASHES.txt`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/10_SENSORS_REVIEW_TARGET/supplement/README_SUPPLEMENT_STATUS.md`: identical to Tree 1 (`manuscript/final_candidates/synthesis_v2/supplement/README_SUPPLEMENT_STATUS.md`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/12_SENSORS_SUBMISSION_MATERIALS/Highlights.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Highlights.md`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/12_SENSORS_SUBMISSION_MATERIALS/Novelty_Contribution_Statement.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Novelty_Contribution_Statement.md`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/12_SENSORS_SUBMISSION_MATERIALS/Short_Cover_Summary.md`: identical to Tree 1 (`manuscript/final_candidates/opus/submission_package/Short_Cover_Summary.md`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/30_DISSERTATION/DISSERTATION_CHAPTER_OUTLINE.md`: identical to Tree 12 (`02_EVIDENCE/PACKAGE_DOCS/DISSERTATION_CHAPTER_OUTLINE.md`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/40_MEASUREMENT_FAMILY_SCOPE/MEASUREMENT_SCOPE_SUMMARY.md`: identical to Tree 12 (`02_EVIDENCE/PACKAGE_DOCS/MEASUREMENT_SCOPE_SUMMARY.md`)
- `_work/stage/CHATGPT_RESEARCH_MENTOR/COMMON/DISSERTATION_IMPLEMENTATION_EVIDENCE.md`: identical to Tree 12 (`02_EVIDENCE/COMMON_CONTEXT/DISSERTATION_IMPLEMENTATION_EVIDENCE.md`)
