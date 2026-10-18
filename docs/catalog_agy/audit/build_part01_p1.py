import json
import os
import csv
from verifier_base import verify_record

audit_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit"

records = []

# --- Group 1A: Reports, plans, inventories, and reviews (Rows 2 to 28) ---

records.append({
    "path": "/mnt/phd_data/phd_master/00_inbox/incoming_2026-10-14_from_mnt_data/DEV_shm-displacement-project/docs/paper1_published/allied_data/Ajmal_IEEEAccess_documents/IEEE_Access_Submission_Package/Short_Cover_Summary.tex",
    "kind": "manuscript",
    "what_it_is": "Executive summary outlining the ROS-based multi-camera displacement tracking framework for the IEEE Access submission package.",
    "question": "How does the proposed ROS-based multi-camera displacement tracking framework compare in accuracy and cost to laser displacement sensors and shear building benchmarks?",
    "method": ["ROS-based distributed camera capture", "AprilTag-based 3D pose estimation", "software-only millisecond-level synchronization", "laser displacement sensor benchmarking", "five-story shear building modal validation"],
    "inputs": ["camera video streams", "laser displacement sensor reference data", "shake table vibration data"],
    "outputs": ["sub-millimeter 3D displacement records"],
    "key_results": ["measure structural displacements with sub-millimeter accuracy"],
    "date": "unclear",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "paper1",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/REPORT.md",
    "kind": "report",
    "what_it_is": "Comprehensive catalog and forensics report documenting rosbag files, analysis scripts, and experimental results across all mounted drives.",
    "question": "What rosbag data, scripts, and analytical outputs exist across all storage volumes for the wind-tunnel camera experiments?",
    "method": ["filesystem scan across mounted drives", "SHA-256 deduplication", "rosbag topic and duration indexing", "script and output inventory generation"],
    "inputs": ["mounted storage volumes", "rosbag archives", "analysis workspaces"],
    "outputs": ["bags_inventory.csv", "code_and_docs_inventory.csv", "results_inventory.csv", "ai_sessions_index.csv"],
    "key_results": ["Scope: every analysis, result and script that touches the rosbag data"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

records.append({
    "path": "/home/ammar/Desktop/P2A_Measurement_ChatGPT_Project_Kit_2026-10-14/P2A_Measurement_Project_Package/02_EVIDENCE/INPUT_CHECKLIST.md",
    "kind": "plan",
    "what_it_is": "Checklist specifying required inputs and canonical evidence artifacts for the pre-submission audit of Paper 2A.",
    "question": "What canonical manuscript files, data tables, code commits, and verification artifacts must be provided for independent scientific audit?",
    "method": ["inventory classification of essential and supporting documents", "provenance verification tracking", "reproducibility readiness check"],
    "inputs": ["manuscript source files", "data tables 2, 3, 4, 6, 7", "git commit history"],
    "outputs": ["completed audit checklist"],
    "key_results": ["Complete Table 2/3/4/6/7 exports; camera/LDS matched RPM mapping and analyzed population lists"],
    "date": "2026-10-14",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/home/ammar/Desktop/P2A_Measurement_ChatGPT_Project_Kit_2026-10-14/P2A_Measurement_Project_Package/02_EVIDENCE/EVIDENCE_POLICY.md",
    "kind": "plan",
    "what_it_is": "Guidelines and evidentiary standards defining verification statuses and citation requirements for the Measurement paper audit.",
    "question": "What standards of proof and evidence classification codes should be applied to verify manuscript claims?",
    "method": ["definition of evidence status tags", "source tracing rules", "reproducibility logging protocol"],
    "inputs": ["manuscript drafts", "data processing pipelines", "experimental logs"],
    "outputs": ["standardized evidence statuses"],
    "key_results": ["Use statuses VERIFIED-RAW (reproduced from documented raw inputs and code), VERIFIED-DOC (directly located in source"],
    "date": "2026-10-14",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/home/ammar/Desktop/P2A_Measurement_ChatGPT_Project_Kit_2026-10-14/P2A_Measurement_Project_Package/05_REVIEW_DIGEST/PRIOR_CHATGPT_AUDIT_DIGEST.md",
    "kind": "report",
    "what_it_is": "Digest synthesizing critical findings from a prior ChatGPT audit of the 58-page Measurement manuscript draft.",
    "question": "What high-priority numerical discrepancies, channel mixing errors, and methodological vulnerabilities exist in the Measurement paper draft?",
    "method": ["audit finding extraction", "cross-table numerical comparison", "channel mixing identification", "regression slope conflict analysis"],
    "inputs": ["main(7).pdf (58 pages)", "prior single-chat audit transcript"],
    "outputs": ["itemized priority issue list"],
    "key_results": ["Prose at 80 and 300 RPM reportedly mixes bending/torsion channel values and ratio calculations."],
    "date": "2026-10-14",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": ["Population and Bland-Altman bias mismatches"]
})

records.append({
    "path": "/home/ammar/Downloads/Reference-Blind_Per-Camera_Spectral_Analysis_of_a_Wind-Tunnel_Bridge-Deck_Model_ChatGPT-GPT6_Review.md",
    "kind": "report",
    "what_it_is": "Independent scientific and editorial critique of the Sensors Paper B manuscript by ChatGPT GPT-6 focusing on spectral recovery.",
    "question": "Does the reference-blind per-camera spectral analysis manuscript meet Sensors editorial and methodological standards?",
    "method": ["editorial review against MDPI standards", "spectral methodology critique", "per-camera frequency recovery assessment", "structure versus noise peak evaluation"],
    "inputs": ["paper2_sensors_synthesis.pdf (24 pages, 16 September 2026)"],
    "outputs": ["editorial recommendations", "minor and major revision points"],
    "key_results": ["no edits performed"],
    "date": "2026-10-14",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2A-spectral",
    "open_questions": []
})

records.append({
    "path": "/home/ammar/Downloads/OMRPR_PaperA_Supervisor-Reviewer-Editor-Report_Claude.md",
    "kind": "report",
    "what_it_is": "Pre-submission review report by Claude simulating supervisor, reviewer, and editor roles on Paper A for Measurement.",
    "question": "What structural, statistical, and narrative weaknesses must be rectified before submitting OMRPR Paper A to Measurement?",
    "method": ["adversarial peer-review simulation", "scope and contribution evaluation", "statistical significance testing critique", "laser benchmark validity analysis"],
    "inputs": ["OMRPR Paper A manuscript draft"],
    "outputs": ["editorial decision", "itemized reviewer comments"],
    "key_results": ["diagnosis only, no edits made to the manuscript"],
    "date": "2026-10-14",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/home/ammar/Downloads/Reference-Blind_Per-Camera_Spectral_Analysis_Wind-Tunnel_Bridge-Deck_Review_Claude.md",
    "kind": "report",
    "what_it_is": "Pre-submission review by Claude evaluating the Sensors draft on reference-blind spectral analysis.",
    "question": "How robust is the argument that native timestamp Lomb-Scargle periodograms extract bridge-deck modal frequencies without a displacement reference?",
    "method": ["methodological evaluation of Lomb-Scargle periodograms", "sampling jitter effect analysis", "per-camera peak validation critique", "journal scope compliance review"],
    "inputs": ["draft manuscript for Sensors"],
    "outputs": ["reframing suggestions", "detailed section-by-section comments"],
    "key_results": ["The template placeholders ([A/B], sibling line, page target) were unfilled."],
    "date": "2026-10-14",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2A-spectral",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/dump/OMRPR Research Recovery, Consolidation, Reproducibility, and Publication Master Audit Prompt.md",
    "kind": "plan",
    "what_it_is": "Comprehensive prompt defining the master audit role, objectives, and workflow for reconstructing the OMRPR project.",
    "question": "How can the complete scientific history and reproducible codebase of the OMRPR project be reconstructed across all legacy directories?",
    "method": ["scientific history reconstruction", "cross-generation codebase auditing", "reproducibility repository design", "manuscript and dissertation harmonization"],
    "inputs": ["all historical OMRPR repositories", "legacy data dumps", "manuscript drafts"],
    "outputs": ["clean reproducible research repository design"],
    "key_results": ["all reported scientific results can be reproduced"],
    "date": "unclear",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

records.append({
    "path": "/mnt/space/data on Computer/~~ DATA TO MOVE/~ SETUPS/ai-state/omrpr-analysis-state.md",
    "kind": "notes",
    "what_it_is": "Project state file capturing active repo status, hard constraints, and legacy bug analysis for the omrpr-analysis clean rebuild.",
    "question": "What hard constraints and verified bugs from legacy implementations govern the clean-room rebuild of omrpr-analysis?",
    "method": ["repository status tracking", "legacy defect logging", "architectural constraint definition"],
    "inputs": ["omrpr-analysis git repo", "LEGACY_ANALYSIS_REPORT.md", "AGENTS.md"],
    "outputs": ["project state record"],
    "key_results": ["Initial commit: clean-room rebuild scaffold after nuclear reset"],
    "date": "2026-07-22",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/OMRPR_Logseq_Revision_Bundle/OMRPR Critical Audit and Revision Plan.md",
    "kind": "plan",
    "what_it_is": "Structured Logseq revision plan providing itemized issue IDs and corrective actions for the 53-page OMRPR manuscript.",
    "question": "What specific revisions and issue remediations are required to bring the 53-page OMRPR manuscript to submission readiness?",
    "method": ["line-by-line manuscript audit", "equation and algorithm verification", "issue register compilation in Logseq format", "executive decision formulation"],
    "inputs": ["main(6).pdf (53 pages)"],
    "outputs": ["revision checklist", "stable issue IDs"],
    "key_results": ["**Recommendation:** Major Revision before submission."],
    "date": "2026-07-17",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_review_reports/chatgpt_omrpr_review_report.md",
    "kind": "report",
    "what_it_is": "Adversarial editorial review report recommending reject-and-resubmit for the OMRPR paper due to measurand and comparison flaws.",
    "question": "Are the principal claimed contributions of the OMRPR manuscript established at the standard required by Measurement?",
    "method": ["editorial critique", "measurand definition evaluation", "temporal synchronization review", "non-simultaneous laser comparison critique"],
    "inputs": ["OMRPR manuscript draft"],
    "outputs": ["provisional editorial recommendation", "required methodological repairs"],
    "key_results": ["Reject and Resubmit as a New Manuscript"],
    "date": "unclear",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": ["the absence of demonstrated temporal synchronization accuracy"]
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/prompts/03_results_figures_lock.md",
    "kind": "notes",
    "what_it_is": "Operational notes locking down numerical results, tables, and figures following resolution of geometric provenance.",
    "question": "How should results, figures, and tables in the OMRPR paper be finalized and protected against AI hallucination?",
    "method": ["geometry provenance resolution lock", "table formatting adjustment", "regression confidence interval correction", "guardrail enforcement"],
    "inputs": ["pipeline configuration", "experimental photos", "verified table data"],
    "outputs": ["locked figures and tables"],
    "key_results": ["Geometry provenance RESOLVED 2026-07-03"],
    "date": "2026-07-07",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/external_review_revision_report.md",
    "kind": "report",
    "what_it_is": "Revision report documenting fixes implemented in response to external adversarial reviews from ChatGPT and Copilot.",
    "question": "How were the critical issues raised by external AI reviewers resolved against ground-truth pipeline data?",
    "method": ["pipeline code and data verification", "anonymization cleanup", "recompilation and page count tracking", "claim boundary alignment"],
    "inputs": ["chatgpt_review.md", "copilot_review.md", "option_b_verified_table.csv"],
    "outputs": ["recompiled 38-page manuscript", "actioned critique responses"],
    "key_results": ["The manuscript recompiles clean (38 pages, was 35;"],
    "date": "2026-07-06",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/copilot_review.md",
    "kind": "report",
    "what_it_is": "Copilot peer-review critique arguing that non-simultaneous laser data cannot establish measurement accuracy.",
    "question": "Can condition-level correlation against laser data collected eleven months earlier validate vision measurement accuracy?",
    "method": ["methodological scrutiny of correlation metrics", "non-simultaneity impact analysis", "claim boundary evaluation"],
    "inputs": ["OMRPR manuscript draft"],
    "outputs": ["major issues critique", "revision requirements"],
    "key_results": ["Direct waveform-level or same-run validation is not possible and is not claimed."],
    "date": "unclear",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": ["The central LDV comparison cannot establish measurement accuracy, only trend consistency"]
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/chatgpt_review.md",
    "kind": "report",
    "what_it_is": "Detailed adversarial review report by ChatGPT flagging confidentiality breaches and avoidable tunnel identifiers in the manuscript.",
    "question": "What confidentiality violations, facility naming breaches, and unverified claims exist in the Measurement manuscript draft?",
    "method": ["facility and vendor anonymity audit", "manuscript text search", "data availability statement examination"],
    "inputs": ["OMRPR manuscript draft (page 33)"],
    "outputs": ["itemized major violations", "required redactions"],
    "key_results": ["Facility anonymization is breached. This is the clearest hard violation."],
    "date": "unclear",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/consolidated_findings.md",
    "kind": "report",
    "what_it_is": "Consolidated matrix tracking adversarial review findings across multiple review passes and checking resolution status.",
    "question": "What is the resolution status of all adversarial review findings against the current Option B manuscript text?",
    "method": ["consolidation of adversarial review passes", "triage against current LaTeX text", "evidence tracking in tabular format"],
    "inputs": ["DEEP_METHODS_REVIEW_adversarial.md", "discussion_critique_log.md", "current manuscript text"],
    "outputs": ["consolidated finding table"],
    "key_results": ["`config/pipeline_config.yaml` shows real calibrated values"],
    "date": "2026-07-06",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/2026-07-06_fresh_pass/reviewer_C_compliance_general.md",
    "kind": "report",
    "what_it_is": "Adversarial compliance review focusing on banned claims, facility confidentiality, and text-figure consistency.",
    "question": "Does the 32-page compiled manuscript comply with facility anonymity rules and internal figure consistency?",
    "method": ["sentence-by-sentence banned-phrase screening", "facility anonymity cross-check", "text-figure consistency inspection"],
    "inputs": ["compiled main.pdf (32 pages)", "claim_boundary.md"],
    "outputs": ["compliance audit findings", "required textual corrections"],
    "key_results": ["directly violating the facility-anonymity requirement."],
    "date": "2026-07-06",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": ["Figure 5 (fig03_ldv_scatter) appears to plot the 320 RPM (e20) data point that the text says is not reported."]
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/2026-07-06_fresh_pass/reviewer_B_novelty_significance.md",
    "kind": "report",
    "what_it_is": "Adversarial review analyzing the significance of claimed contributions, prior art differentiation, and the 11-month test gap.",
    "question": "Are the four claimed contributions sufficiently novel and rigorously supported given the non-simultaneous comparison?",
    "method": ["contribution stress-testing", "prior-art positioning review", "ratio decomposition critique"],
    "inputs": ["compiled main.pdf (32 pages)", "claim_boundary.md"],
    "outputs": ["novelty assessment", "stress-test findings"],
    "key_results": ["The centerpiece validation is a non-simultaneous, ~11-month-apart comparison"],
    "date": "2026-07-06",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": ["the paper openly admits the decomposition has NOT been done"]
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/2026-07-06_fresh_pass/reviewer_A_statistical_rigor.md",
    "kind": "report",
    "what_it_is": "Adversarial review evaluating the statistical rigor, sample size limits (N=19), and wide dynamic range confounds in the OMRPR paper.",
    "question": "Does a Pearson correlation of r=0.960 across N=19 wind speed conditions provide valid evidence of measurement capability?",
    "method": ["statistical rigor evaluation", "monotonicity confound analysis", "dynamic range sensitivity check", "confidence interval critique"],
    "inputs": ["compiled main.pdf (32 pages)", "Table 2 data"],
    "outputs": ["statistical critiques", "recommended methodological qualifications"],
    "key_results": ["M1. The headline validation metric is a condition-level aggregate correlation over N=19"],
    "date": "2026-07-06",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": ["This is not a sample of 19 independent structural states in any meaningful statistical sense"]
})

records.append({
    "path": "/mnt/phd-legacy/fin_phd/omrpr_outputs_review/reviewer_risk_reports/discussion_critique_log.md",
    "kind": "report",
    "what_it_is": "Adversarial critique log evaluating the discussion and conclusion sections for restatement versus interpretation issues.",
    "question": "Do the discussion and conclusion sections provide genuine physical and methodological interpretation rather than repeating results?",
    "method": ["section-by-section rhetoric audit", "finding formalization", "re-verification against revised text"],
    "inputs": ["05_discussion.tex", "FINALIZATION_PLAN.md"],
    "outputs": ["remediated paragraph openings", "audit log"],
    "key_results": ["Two restatement-not-interpretation paragraphs"],
    "date": "2026-07-06",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "2B-comparison",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/ai_sessions_index.csv",
    "kind": "data-table",
    "what_it_is": "Inventory indexing AI assistance chat transcripts and session logs related to the rosbag analysis.",
    "question": "What AI chat transcripts and LLM sessions exist in the project archives and what topics did they cover?",
    "method": ["metadata extraction from chat exports", "date and tool indexing", "inventory table generation"],
    "inputs": ["chat session archives", "Claude and ChatGPT conversation exports"],
    "outputs": ["ai_sessions_index.csv"],
    "key_results": ["last_modified,tool,mentions_omrpr_rosbag_apriltag,size_KB,cwd,path"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "background",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/not_on_phd_data.csv",
    "kind": "data-table",
    "what_it_is": "Inventory listing files and datasets located on external or mounted drives that are missing from the primary phd_data storage.",
    "question": "Which project files and data artifacts are stored only on external drives and need archiving to phd_data?",
    "method": ["cross-volume path comparison", "SHA-256 presence check", "delta inventory compilation"],
    "inputs": ["external drive catalogs", "phd_data filesystem index"],
    "outputs": ["not_on_phd_data.csv"],
    "key_results": ["size,mtime,path,other_copies"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "background",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/code_and_docs_inventory.csv",
    "kind": "data-table",
    "what_it_is": "Inventory cataloging all unique analysis code scripts and documentation files across all project drives.",
    "question": "What unique scripts, notebooks, configuration files, and documentation exist across all project directories?",
    "method": ["recursive file search", "SHA-256 deduplication", "path and metadata cataloging"],
    "inputs": ["mounted project filesystems"],
    "outputs": ["code_and_docs_inventory.csv"],
    "key_results": ["sha256_12,kind,size,newest_mtime,n_copies,primary_path,first_docstring_line,other_locations_count_by_root"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/results_inventory.csv",
    "kind": "data-table",
    "what_it_is": "Inventory cataloging experimental output files, computed tables, and figures generated from rosbag processing.",
    "question": "What analytical result files, summary tables, and generated figures exist across the project workspaces?",
    "method": ["result file indexing", "output type classification", "timestamp and size cataloging"],
    "inputs": ["output directories across drives"],
    "outputs": ["results_inventory.csv"],
    "key_results": ["path,files,size_MB,newest,oldest"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/bags_inventory.csv",
    "kind": "data-table",
    "what_it_is": "Comprehensive inventory listing all 767 rosbag files (.bag, .db3, .mcap) found across all mounted storage volumes.",
    "question": "What raw and processed rosbag files exist across all storage media for the vision experiments?",
    "method": ["recursive search for rosbag extensions", "SHA-256 hashing", "drive location tracking"],
    "inputs": ["all mounted storage volumes"],
    "outputs": ["bags_inventory.csv"],
    "key_results": ["drive_root,size_bytes,mtime,path"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

records.append({
    "path": "/mnt/phd_data/phd_master/_catalog/rosbag_analysis_inventory_2026-10-15/code_version_conflicts.csv",
    "kind": "data-table",
    "what_it_is": "Inventory tracking script filename collisions where different file versions exist across project worktrees.",
    "question": "Which analysis scripts have conflicting implementations or diverging versions across legacy worktrees?",
    "method": ["filename grouping", "hash comparison", "version divergence detection"],
    "inputs": ["code_and_docs_inventory.csv"],
    "outputs": ["code_version_conflicts.csv"],
    "key_results": ["basename,n_versions,version_newest_mtime,sha256_12,size,primary_path"],
    "date": "2026-10-15",
    "status": "complete",
    "superseded_by": "",
    "paper2_relevance": "both",
    "open_questions": []
})

# Verify all records added so far
for r in records:
    verify_record(r)

print(f"Group 1A verified: {len(records)} records valid.")
