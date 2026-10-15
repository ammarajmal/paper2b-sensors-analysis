# Tree 7 Summary: SHM Displacement Project - Active (Non-identical extensions, supplementary analysis notebooks, and memory records)

## Overview and Scope
Tree 7 contains 282 total scanned files (123 catalogued, 159 identical duplicates).
SHM Displacement Project - Active (Non-identical extensions, supplementary analysis notebooks, and memory records).

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
- `offline_processing/scripts/compare_ldv.py`
- `clear_outputs.py`
- `normalize_notebook.py`
- `output.ipynb`

## Key Results and Stated Findings
- **`context_data/literature review/deep-research-report.md`**: "(2) add a **measurement-uncertainty budget layer** that quantitatively links camera agreement, timing, floor effects, and bootstrap variability"
- **`context_data/literature review/deep-research-report.md`**: "(4) add a **frequency-estimator robustness cross-check** so the FFT-based characterization is more reviewer-resistant"
- **`docs/chatgpt_project_brief.md`**: "Camera timing is nominally 60 fps but not hardware-synchronized"
- **`docs/documentation_maintenance_checklist.md`**: "Confirm Step 04c direct common `60 Hz` remains the preferred final response basis"
- **`docs/frame_sync_academic_notes.md`**: "This means structural vibrations up to ~30 Hz can be safely captured without aliasing"
- **`docs/frame_sync_academic_notes.md`**: "This exceeds a target accuracy of 0.1 mm"
- **`docs/frame_sync_academic_notes_fixed.md`**: "This means structural vibrations up to ~30 Hz can be safely captured without aliasing"
- **`docs/frame_sync_academic_notes_fixed.md`**: "This exceeds a target accuracy of 0.1 mm"

## Planned or Missing Elements
- `context_data/literature review/deep-research-report.md`: mapping commit → figures/tables/reports |
- `context_data/literature review/deep-research-report.md`: | 4–6 |
- `docs/chatgpt_project_brief.md`: To Ask ChatGPT
- `docs/documentation_governance.md`: | result_discussion | generated_report | archive
- `docs/paper2_tesolution_style_torsion_plan.md`: to form the marker pair
- `docs/paper2_tesolution_style_torsion_plan.md`: - the direct proxy comparison uses `torsion_diff_y_mm` versus corrected LDV tors
- `docs/paper2_tesolution_style_torsion_plan.md`: - `marker_spacing_mm = 200`

## Duplicate Files Across Trees
- `docs/PROJECT_TRUTH_CONTEXT.md`: identical to Tree 6 (`docs/PROJECT_TRUTH_CONTEXT.md`)
- `docs/artifact_provenance_rules.md`: identical to Tree 6 (`docs/artifact_provenance_rules.md`)
- `docs/claim_language_rules.md`: identical to Tree 6 (`docs/claim_language_rules.md`)
- `docs/experimental_setup.md`: identical to Tree 6 (`memory/experimental_setup.md`)
- `docs/measurement_timing_limitations.md`: identical to Tree 6 (`docs/measurement_timing_limitations.md`)
- `docs/paper2_claim_boundary.md`: identical to Tree 6 (`docs/paper2_claim_boundary.md`)
- `docs/paper2_facility_anonymization_note.md`: identical to Tree 6 (`docs/paper2_facility_anonymization_note.md`)
- `docs/paper2_figure_table_index.md`: identical to Tree 6 (`docs/paper2_figure_table_index.md`)
