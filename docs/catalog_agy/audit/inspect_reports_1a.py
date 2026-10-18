import os

files = [
    "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/REPORT.md",
    "/home/ammar/Desktop/P2A_Measurement_ChatGPT_Project_Kit_2026-10-14/P2A_Measurement_Project_Package/02_EVIDENCE/INPUT_CHECKLIST.md",
    "/home/ammar/Desktop/P2A_Measurement_ChatGPT_Project_Kit_2026-10-14/P2A_Measurement_Project_Package/02_EVIDENCE/EVIDENCE_POLICY.md",
    "/home/ammar/Desktop/P2A_Measurement_ChatGPT_Project_Kit_2026-10-14/P2A_Measurement_Project_Package/05_REVIEW_DIGEST/PRIOR_CHATGPT_AUDIT_DIGEST.md",
    "/home/ammar/Downloads/Reference-Blind_Per-Camera_Spectral_Analysis_of_a_Wind-Tunnel_Bridge-Deck_Model_ChatGPT-GPT6_Review.md",
    "/home/ammar/Downloads/OMRPR_PaperA_Supervisor-Reviewer-Editor-Report_Claude.md",
    "/home/ammar/Downloads/Reference-Blind_Per-Camera_Spectral_Analysis_Wind-Tunnel_Bridge-Deck_Review_Claude.md",
    "/mnt/phd-legacy/dump/OMRPR Research Recovery, Consolidation, Reproducibility, and Publication Master Audit Prompt.md",
    "/mnt/space/data on Computer/~~ DATA TO MOVE/~ SETUPS/ai-state/omrpr-analysis-state.md",
    "/mnt/phd-legacy/fin_phd/OMRPR_Logseq_Revision_Bundle/OMRPR Critical Audit and Revision Plan.md",
    "/mnt/phd-legacy/fin_phd/omrpr_review_reports/chatgpt_omrpr_review_report.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/prompts/03_results_figures_lock.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/external_review_revision_report.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/copilot_review.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/chatgpt_review.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/consolidated_findings.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/2026-07-06_fresh_pass/reviewer_C_compliance_general.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/2026-07-06_fresh_pass/reviewer_B_novelty_significance.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/2026-07-06_fresh_pass/reviewer_A_statistical_rigor.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/discussion_critique_log.md"
]

for p in files:
    print("="*60)
    print("PATH:", p)
    with open(p, "r", errors="ignore") as f:
        content = f.read(1500)
    print(content)
