# INBOX_PAPER2_REVIEW_INGESTION_REPORT

**Audited Directory**: `/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06`  
**Date**: 2026-10-19  
**Audit Scope**: Research artifacts, reconciliation reports, defect ledgers, and final synthesis candidates generated during the intensive 2026-09-06 through 2026-09-09 pre-submission review of Paper 2 (*Sensors*).  
**Catalog Status**: 100% Ingested and Verified.

---

## 1. Executive Summary & Inventory Accounting

The folder `/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06` contains the final pre-submission audit, defect remediation, and candidate synthesis trail for Paper 2. A comprehensive audit of all files in this directory was conducted with read-only integrity preserved on the source tree.

| Category | Count | Accounting / Destination |
|---|---|---|
| **Total files present in directory** | **155** | `/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/` |
| Audited in earlier G1/G2 batches | 102 | Recorded in `records_G1_paper2_core_part01..07.jsonl` & `records_G2_*.jsonl` |
| Skipped in earlier G1/G2 batches | 2 | Recorded in `audit/SKIPPED.csv` (exact SHA-256 duplicates) |
| Newly audited in this pass | 23 | Recorded in `audit/records_inbox_Paper2_Review_2026-09-06.jsonl` |
| Newly skipped in this pass | 28 | Recorded in `audit/skipped_inbox_Paper2_Review_2026-09-06.csv` and merged into `audit/SKIPPED.csv` |
| Unreadable files | 0 | 0 unreadable files (`audit/UNREADABLE.csv` remains 0 rows) |

The 28 newly skipped files comprise: 13 binary image files (`.png`, `.jpg`), 8 pre-rewrite backup files (`.bak`), 4 compilation logs (`.log`), 2 git diff patches (`.patch`), and 1 oversized binary asset (>400 KB). All 23 newly audited records have been verified against the underlying disk files with exact character-for-character quotation verification.

---

## 2. Breakthrough Findings & Reconciled Evidence

The ingestion of this directory resolves key technical questions and historical contradictions identified across older trees:

### 2.1 Physical Marker Identity & Encoded AprilTag IDs
- **Report**: [`12_TAG_ID_RECONCILIATION_REPORT.md`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/12_TAG_ID_RECONCILIATION_REPORT.md) (accompanied by `11_TAG_ID_RECONCILIATION.csv`).
- **Physical Targets**: Exactly two physical markers exist on the test specimen, not three.
  - *Marker A* (center / near-center marker) is viewed concurrently by `cam1` and `cam2`.
  - *Marker B* (off-center / side marker) is viewed by `cam3` alone.
  *Quote*: "Two physical markers exist, not three."
- **Encoded AprilTag IDs**: Both physical markers decode as AprilTag ID 0 (`tag36h11`). The handwritten paper labels visible in camera views ("ID 0" and "ID 1") are human-readable notations only.
  *Quote*: "Both physical markers decode as AprilTag ID 0."
- **Resolution of Historical Bug**: An early detection script hardcoded `expected_tag_id=1` for `cam3`, causing all 38,448 frames of `cam3` to report as undetected for ten days until corrected on 2026-08-12 (`Decision_Log.md` D0005). Camera identity (`cam1/cam2` vs `cam3`) is the sole valid physical marker discriminator.

### 2.2 Campaign Geometry Non-Equivalence & Separation Retraction
- **Report**: [`14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md) (revised 2026-09-07, with `13_CAMPAIGN_GEOMETRY_RECONCILIATION.csv`).
- **Mechanical System Equivalence**: Confirmed identical bridge-deck model, spring suspension, and boundary conditions between the 2024 campaign and the 2025 multi-camera campaign.
  *Quote*: "mechanical_system_same_between_campaigns   = YES"
- **Marker Geometry & Operator Non-Equivalence**:
  *Quote*: "marker_geometry_same_between_campaigns     = NO"
  - The 2024 campaign used two symmetric markers with 35 mm AprilTags.
  - The 2025 campaign used a center + off-center layout with 20 mm AprilTags.
  - Spatial measurement operators are mathematically non-equivalent.
- **Marker Separation Retraction**: The historical candidate separation of 135.14 mm (derived from a 2024-11-05 photograph assuming 20 mm tags) is definitively retracted and confirmed invalid for the 2025 campaign.
- **External Reference Frequencies**: Because the mechanical suspension is identical, the facility-measured reference natural frequencies ($f_{\text{vertical}} = 1.4303\text{ Hz}$, $f_{\text{torsional}} = 3.1036\text{ Hz}$) remain valid external benchmark lines for spectral recovery evaluation.

### 2.3 Master Defect Ledger & Adjudicated Remediations
- **Ledger & Audit Reports**: [`52_FINAL_MANUSCRIPT_AUDIT_REPORT.md`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/52_FINAL_MANUSCRIPT_AUDIT_REPORT.md), [`53_FINAL_MANUSCRIPT_DEFECT_LEDGER.csv`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/53_FINAL_MANUSCRIPT_DEFECT_LEDGER.csv), [`58_TERRA_INDEPENDENT_FINAL_AUDIT.md`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/58_TERRA_INDEPENDENT_FINAL_AUDIT.md), and [`62_CROSS_MODEL_DEFECT_CONCORDANCE.csv`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/62_CROSS_MODEL_DEFECT_CONCORDANCE.csv).
- **Critical Defect C-01 (Submission Package Alignment)**: Retracted superseded claims from submission documents (VIV claims, KLT branch, condition join against 2024 LDS, and coarse FDD).
  *Quote*: "All five submission-package documents carry the superseded pre-Pass-3 lineage"
- **Critical Defect C-02 (Supplement Readiness)**: Closed missing in-text promises by creating the publication supplement package (Supplements S1–S12) governed by `SUPPLEMENT_MANIFEST.csv`.
- **Major Defects M-01 to M-07 (Methods Reproducibility & Rig Characterization)**:
  - *M-01*: Corrected nonstationarity narrative in Section 5.5 to accurately reflect windowed spectral trajectories (e.g., e0_0rpm cam3 dipping to 7.6417 Hz).
  - *M-02*: Corrected background band axis family matching (4 of 9 cross, 3 match y-family, 1 matches neither).
  - *M-03*: Disclosed running window parameters: 10 s window duration, 5 s hop, 5 windows per 30.5 s record (secondary: 15 s window, 7.5 s hop, 3 windows).
    *Quote*: "The windowed analysis is never defined."
  - *M-04 & M-05*: Clarified half-record persistence check: dominant frequency extracted independently in each half and compared within $2 \Delta f_R$ (2 full-record Rayleigh bins).
  - *M-06*: Documented hardware apparatus in Materials: Sony sensor, 1920×1080 resolution, effective frame rate ~59.94 Hz, and nominal commanded RPM.
  - *M-07*: Retitled manuscript to accurately reflect same-marker cross-view agreement (`cam1`/`cam2`) and condition-dependent differences at a distinct location (`cam3`).

---

## 3. Authoritative Submission Candidate: `synthesis_v2`

The synthesis of independent model audit passes (Terra and Opus) is executed and compiled at:
`/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/final_candidates/synthesis_v2/`

- **Merge Plan & Execution**: Governed by [`70_FINAL_SYNTHESIS_CANDIDATE_REPORT.md`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/70_FINAL_SYNTHESIS_CANDIDATE_REPORT.md) and [`71_FINAL_SYNTHESIS_MERGE_EXECUTION.csv`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/71_FINAL_SYNTHESIS_MERGE_EXECUTION.csv) under strategy `OPUS_BASE_WITH_TERRA_IMPORTS`.
  *Quote*: "This report records the *execution* of an already-adjudicated merge plan."
- **Pre-Submission Compliance**: Certified by [`72_FINAL_SYNTHESIS_PRE_SUBMISSION_CHECKLIST.md`](file:///mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/72_FINAL_SYNTHESIS_PRE_SUBMISSION_CHECKLIST.md).
  *Quote*: "Every status below states what actually holds, verified\nagainst the built artifacts"
- **Compiled Deliverables**:
  1. **Manuscript**: `paper2_sensors_synthesis.tex` (`41fc2df9...`) compiling to `paper2_sensors_synthesis.pdf` (24 pages A4, 0 errors, 0 undefined citations, MDPI *Sensors* class).
  2. **Supplement**: `supplement/paper2_supplement_synthesis.tex` (`d7f78777...`) compiling to `paper2_supplement_synthesis.pdf` (4 pages A4, exit 0), packaging Supplements S1 through S12.
  3. **Data Artifacts**: Shipped with exact source assertions, including `build_table_s1.py` generating Table S1 from frozen inputs.
  4. **Submission Package**: Cleanly aligned Cover Letter, Highlights, Novelty Statement, Short Cover Summary, and Submission Checklist.

---

## 4. Owner Action Items Before Journal Transmission

As documented in [`owner_pending/OWNER_PENDING_ITEMS.md`](file:///mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/final_candidates/synthesis_v2/owner_pending/OWNER_PENDING_ITEMS.md), there are no remaining scientific defects in the manuscript. The only open items are administrative decisions reserved for the project owner:

*Quote*: "Nothing in this list is a scientific defect in the manuscript."

1. **O-01 (Title Signoff)**: Confirm working title: *"Reference-Blind, Native-Timestamp Per-Camera Spectral Analysis of a Wind-Tunnel Bridge-Deck Model: Same-Marker Cross-View Agreement and Condition-Dependent Differences at a Distinct Observation Location"*.
2. **O-01b (Author List & CRediT)**: Confirm author list, ordering, and CRediT author statement.
3. **O-02 (Author Identifiers & Email)**: Provide four author ORCID iDs and missing author email address.
4. **O-03 (Sensors Topical Section)**: Select appropriate topical section on MDPI submission portal.
5. **O-04 (Plagiarism Check)**: Run pre-submission similarity check.
6. **O-05 (GenAI Disclosure)**: Confirm Acknowledgments wording for Claude Code and Codex disclosure.
7. **O-06 (Facility Acknowledgment)**: Confirm whether partner facility is named or acknowledged.
8. **O-07 (Derived Data Permission)**: Confirm authorization to publish derived spectral tables (Supplements S1–S7).

---

## 5. Conclusion & Downstream Impact

The ingestion of `/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06` establishes the single authoritative, scientifically vetted pre-submission package for Paper 2. All historical ambiguities surrounding AprilTag IDs, campaign geometry differences, marker separation values, and defect remediation have been systematically reconciled. The research material is fully organized to unblock the finalization of the doctoral dissertation and manuscript transmission.
