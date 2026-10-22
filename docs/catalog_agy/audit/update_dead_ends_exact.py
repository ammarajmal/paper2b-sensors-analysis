path = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/ATTEMPTS_AND_DEAD_ENDS.md"

# Read original base (sections 1 to 7)
with open(path, "r") as f:
    text = f.read()

# If sections 8-11 already exist, strip them and replace with exact verified versions
if "## 8. Hardcoded" in text:
    base_text = text.split("--- \n\n## 8. Hardcoded")[0].split("## 8. Hardcoded")[0].strip()
else:
    base_text = text.strip()

extra = """
---

## 8. Hardcoded "Expected Tag ID 1" Bug on Camera 3

- **Initial Attempt / Erroneous Implementation:**  
  Early detector post-processing scripts (`fresh_quality_scores/per_frame_detections.csv`) hardcoded `expected_tag_id = 1` for camera 3 under the assumption that Marker B carried encoded AprilTag ID 1.
- **Why Abandoned / Remediated:**  
  Both physical markers in the wind tunnel carry encoded AprilTag ID 0 (with human-readable handwritten labels "ID 0" and "ID 1"). The mismatch caused all 38,448 frames for cam3 to be silently marked as undetected until discovered on 2026-08-12.
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/12_TAG_ID_RECONCILIATION_REPORT.md`  
  *Quote:* "both physical WTT markers carry AprilTag ID 0"  
  *Quote:* "silently marking all 38,448 cam3 frames as `detected=False`"
- **Current Scientific Status:**  
  Detector expectations for all three cameras are locked to ID 0 (`EXPECTED_TAG = {"cam1": 0, "cam2": 0, "cam3": 0}`). Camera identity (cam1/cam2 vs cam3) distinguishes the physical locations.

---

## 9. Campaign Measurement Operator Inequivalence (2024 vs 2025)

- **Initial Attempt / Erroneous Assumption:**  
  Preliminary drafts assumed that torsional observables from the 2024 laser campaign and the 2025 camera campaign were directly equivalent spatial operators.
- **Why Abandoned / Clarified:**  
  While the mechanical structural system was identical between campaigns (`MECHANICAL_SYSTEM_EQUIVALENCE = TRUE`), the marker geometries differed: 2024 used symmetric 35 mm tags, whereas 2025 used center + off-center 20 mm tags. Consequently, the derived spatial observables are physically distinct operators (`MEASUREMENT_OPERATOR_EQUIVALENCE = FALSE`).
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/14_CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md`  
  *Quote:* "mechanical_system_same_between_campaigns   = YES"  
  *Quote:* "measurement_operator_same_between_campaigns = NO"
- **Current Scientific Status:**  
  2024 symmetric torsional displacement and 2025 center-plus-side differential displacement are treated as distinct operators and never equated without explicit geometric transformation.

---

## 10. Superseded Pre-Pass-3 Claims in Submission Packages (Defect C-01)

- **Initial Attempt / Retracted Claims:**  
  Early submission packages asserted claims that were later retracted during manuscript audit: "for Vortex-Induced Vibration Characterization", "explicit five-gate admissibility manifest", "KLT-based diagnostic branch", and "condition-level join against a non-concurrent 2024 laser-vibrometer campaign".
- **Why Abandoned / Remediated:**  
  Adversarial audit `52_FINAL_MANUSCRIPT_AUDIT_REPORT.md` flagged these claims as Critical Defect C-01 because the final manuscript focuses strictly on reference-blind spectral identification and same-marker cross-view agreement.
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/53_FINAL_MANUSCRIPT_DEFECT_LEDGER.csv`  
  *Quote:* "carry the superseded pre-Pass-3 lineage and assert claims the current manuscript retracts"
- **Current Scientific Status:**  
  Submission package documents (cover letter, highlights, novelty statement) are aligned to the synthesized manuscript in `synthesis_v2/` with no mention of VIV, condition joins, or KLT branches.

---

## 11. Undisclosed Running Window Settings (Defect M-03)

- **Initial Attempt / Undisclosed Parameters:**  
  Early drafts presented short-time windowed frequency tracking (Figure 3 and Section 5.5) without disclosing window length, hop size, or window counts.
- **Why Abandoned / Remediated:**  
  Flagged as Major Defect M-03; reproducibility required full specification of the windowing parameters.
- **Evidence / Source:**  
  `00_inbox/Paper2_Review_2026-09-06/53_FINAL_MANUSCRIPT_DEFECT_LEDGER.csv`  
  *Quote:* "10 s windows, 5 s hop, 5 windows per ~30.5 s record"
- **Current Scientific Status:**  
  Methods explicitly document: 10 s window length, 5 s hop, 5 windows per ~30.5 s record, with a secondary 15 s / 7.5 s setting reported in Supplement S4 (`28_WINDOWED_FREQUENCY_EVOLUTION.csv`).
"""

with open(path, "w") as f:
    f.write(base_text + "\n" + extra.strip() + "\n")

print(f"Updated {path} with exact quotes.")
