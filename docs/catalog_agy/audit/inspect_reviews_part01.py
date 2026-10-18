import os

files = [
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/external_review_revision_report.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/copilot_review.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/chatgpt_review.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/consolidated_findings.md",
    "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/prompts/03_results_figures_lock.md",
    "/mnt/phd-legacy/fin_phd/omrpr_review_reports/chatgpt_omrpr_review_report.md",
    "/mnt/phd-legacy/fin_phd/OMRPR_Logseq_Revision_Bundle/OMRPR Critical Audit and Revision Plan.md",
    "/mnt/space/data on Computer/~~ DATA TO MOVE/~ SETUPS/ai-state/omrpr-analysis-state.md",
    "/mnt/phd-legacy/dump/OMRPR Research Recovery, Consolidation, Reproducibility, and Publication Master Audit Prompt.md"
]

for p in files:
    print("="*60)
    print("PATH:", p)
    with open(p, "r", errors="ignore") as f:
        print(f.read(1000))
