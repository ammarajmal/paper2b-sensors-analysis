# Tree 5 Summary: OMRPR Manuscript (Sensors manuscript draft, journal guidelines, and review correspondence)

## Overview and Scope
Tree 5 contains 62 total scanned files (59 catalogued, 3 identical duplicates).
OMRPR Manuscript (Sensors manuscript draft, journal guidelines, and review correspondence).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `ai_review/estimate_marker_arms.py`
- `scripts/bootstrap_condition_level_ci.py`
- `scripts/build.sh`
- `scripts/clean.sh`
- `scripts/gen_fig03_ldv_scatter.py`
- `scripts/gen_fig08_bland_altman.py`
- `scripts/rebuild_option_b_corrected.py`
- `scripts/verify_option_b.py`

## Key Results and Stated Findings
- **`ai_review/CLAIM_EVIDENCE_MATRIX.md`**: "tex:25` | Registration residual diagnostic + bootstrap CIs + noise floor"
- **`ai_review/CLAIM_EVIDENCE_MATRIX.md`**: "C5 | Torsion-proxy condition-level agreement: r≈0.968, ratio≈0.785× | abstract"
- **`ai_review/CODE_REPRODUCIBILITY_AUDIT.md`**: "py` ("Only DCG (motion blur, 320 RPM) is excluded")"
- **`ai_review/FATAL_FLAW_REGISTER.md`**: "FF-03 | OMRPR expanded as **"Offline Multi-Modal Robust Pose Reconstruction"** — the system is single-modality (cameras only"
- **`ai_review/FATAL_FLAW_REGISTER.md`**: "tex:4` | "Multi-modal" is on the author's own avoid-list and is factually indefensible"
- **`ai_review/FIGURE_TABLE_AUDIT.md`**: "Confirm the cam3-only 320 RPM point (2.19 mm) — already fixed in a prior round"
- **`ai_review/FIGURE_TABLE_AUDIT.md`**: "5 (`fig05_uncertainty`) | Per-condition RMS with bootstrap CIs + noise floor bands | Yes | Keep"
- **`ai_review/MEASUREMENT_REVISION_ROADMAP.md`**: "8. **Address the 100 RPM outlier** (torsion 0.18×) explicitly in §4.5/§5.2 (FF-10)"
- **`ai_review/MEASUREMENT_REVISION_ROADMAP.md`**: "LOO torsion r without 100 RPM"

## Planned or Missing Elements
- `ai_review/CLAIM_EVIDENCE_MATRIX.md`: (FF-06)
- `ai_review/CLAIM_EVIDENCE_MATRIX.md`: a reviewer may ask what is "robust"
- `ai_review/CODE_REPRODUCIBILITY_AUDIT.md`: in deposit README that structural-property derivation requires proprietary vendo
- `ai_review/CODE_REPRODUCIBILITY_AUDIT.md`: explicitly
- `ai_review/FATAL_FLAW_REGISTER.md`: reprojection error 0
- `ai_review/FATAL_FLAW_REGISTER.md`: the derived element is specifically N

## Duplicate Files Across Trees
- `docs/source_of_truth/claim_boundary.md`: identical to Tree 4 (`docs/claim_boundary.md`)
- `docs/source_of_truth/pipeline_diagram.md`: identical to Tree 4 (`docs/pipeline_diagram.md`)
- `.vscode/settings.json`: identical to Tree 4 (`docs/_archive/stray_nested_manuscript_clone/.vscode/settings.json`)
