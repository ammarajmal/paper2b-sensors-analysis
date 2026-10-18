import sys, os, csv, json
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

def build_all_p05():
    records = []
    
    # 0..20: Group 1
    # 0
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/reviewed_text/A_reviewed_Oct12.txt",
        "kind": "manuscript",
        "what_it_is": "Consolidated draft manuscript of Paper 2B submitted to Measurement on multi-camera optical displacement and pose reconstruction reviewed on October 12.",
        "question": "How accurately does the multi-camera optical tracking framework reconstruct dynamic bridge-deck displacements and pose compared to laser references?",
        "method": ["AprilTag fiducial detection", "system clock synchronization", "detection completeness gating", "rigid-body pose reconstruction", "laser sensor displacement comparison"],
        "inputs": ["multi-camera video frames across 21 wind-tunnel fan speeds", "reference laser displacement sensor logs"],
        "outputs": ["A_reviewed_Oct12.txt"],
        "key_results": ["the bending channel achieved r = 0.9711"],
        "date": "2026-10-12",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })
    # 1
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B04_experimental_conditions_p1.json",
        "kind": "report",
        "what_it_is": "Cluster register grouping review findings and presentation issues for experimental conditions in Section 3.2.",
        "question": "What structural and narrative defects exist in the presentation of wind-tunnel experimental conditions in Section 3.2?",
        "method": ["clustering multi-AI review findings", "synthesizing editorial recommendations", "validating cluster completeness against source findings"],
        "inputs": ["AI reviewer findings for experimental conditions"],
        "outputs": ["B04_experimental_conditions_p1.json"],
        "key_results": ["Section 3.2 repeats the DCG derivation and threshold from Section 2.4.1"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 2
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/logs/B03_methods_pipeline_p4.last.txt",
        "kind": "notes",
        "what_it_is": "Validation log recording the successful clustering and verification of 30 review findings for methods pipeline bucket 4.",
        "question": "Did the automated review clustering pipeline pass validation for methods bucket 4 without omissions or invented clusters?",
        "method": ["running cluster register validator", "verifying finding count consistency (30 findings clustered)"],
        "inputs": ["B03_methods_pipeline_p4.json"],
        "outputs": ["B03_methods_pipeline_p4.last.txt"],
        "key_results": ["findings=30 clustered=30 missing=0 duplicated=0 invented=0 empty/blank clusters=0"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 3
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B03_methods_pipeline_p4.json",
        "kind": "report",
        "what_it_is": "Cluster register grouping 30 review findings on RPM spacing and baseline definitions in the methods pipeline.",
        "question": "What specific methodology omissions regarding RPM set points and reference baselines were identified by reviewers?",
        "method": ["clustering review findings for methods bucket 4", "formulating actionable drafting remedies"],
        "inputs": ["review finding extraction lists"],
        "outputs": ["B03_methods_pipeline_p4.json"],
        "key_results": ["The Methods omit the 21 RPM set points"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 4
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/logs/B03_methods_pipeline_p3.last.txt",
        "kind": "notes",
        "what_it_is": "Validation execution log confirming zero missing or duplicated findings across 70 items in methods pipeline bucket 3.",
        "question": "Did cluster register B03_methods_pipeline_p3.json satisfy all automated schema and completeness checks?",
        "method": ["executing validator script on methods pipeline bucket 3", "checking finding counts and bijection constraints"],
        "inputs": ["B03_methods_pipeline_p3.json"],
        "outputs": ["B03_methods_pipeline_p3.last.txt"],
        "key_results": ["findings=70 clustered=70 missing=0 duplicated=0 invented=0 empty/blank clusters=0"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 5
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B03_methods_pipeline_p3.json",
        "kind": "report",
        "what_it_is": "Structured cluster register consolidating 70 review findings concerning diagnostic checks and pipeline internal status reporting.",
        "question": "Which internal pipeline diagnostics and intermediate status checks need restructuring or removal from the manuscript?",
        "method": ["categorizing 70 review critique points", "identifying unused diagnostic claims in Methods"],
        "inputs": ["raw AI review extractions"],
        "outputs": ["B03_methods_pipeline_p3.json"],
        "key_results": ["The Methods describe unused diagnostic checks in process or internal-status language"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 6
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B03_methods_pipeline_p2.json",
        "kind": "report",
        "what_it_is": "Synthesized review findings register analyzing statistical significance and prominence of spectral peaks in the Methods section.",
        "question": "How should spectral peak detection criteria be formalized to ensure rigorous statistical standing in the manuscript?",
        "method": ["grouping reviewer critiques on periodogram peak significance", "formulating recommendations for spectral thresholding"],
        "inputs": ["peer review commentary on spectral methods"],
        "outputs": ["B03_methods_pipeline_p2.json"],
        "key_results": ["The Methods do not give spectral peaks adequate statistical standing"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 7
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B03_methods_pipeline_p1.json",
        "kind": "report",
        "what_it_is": "Register of clustered review points on software architecture bloat and detection completeness gating in Section 2.",
        "question": "What excessive software implementation details and coordinate centering descriptions in Section 2 should be condensed?",
        "method": ["aggregating editorial critiques on pipeline description", "clustering overdeveloped software architecture issues"],
        "inputs": ["reviewer evaluations of Section 2"],
        "outputs": ["B03_methods_pipeline_p1.json"],
        "key_results": ["Section 2 overdevelops software-architecture and implementation-pipeline material"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 8
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B02_introduction_p2.json",
        "kind": "report",
        "what_it_is": "Review cluster inventory categorizing rhetorical style, conclusion claims, and defensive framing in the Introduction.",
        "question": "Which rhetorical expressions and premature conclusion statements in the Introduction require editorial neutralization?",
        "method": ["identifying defensive phrasing and rhetoric in Introduction text", "clustering findings into actionable revision items"],
        "inputs": ["introduction section review feedback"],
        "outputs": ["B02_introduction_p2.json"],
        "key_results": ["The Introduction describes the conclusion as directly demonstrating pipeline success"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 9
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/clusters_A/B02_introduction_p1.json",
        "kind": "report",
        "what_it_is": "Clustered editorial assessment evaluating literature review coverage and contribution claims in the manuscript Introduction.",
        "question": "How can the Introduction's literature review and contribution claims be revised to better separate vision and vibration literature?",
        "method": ["cataloguing reviewer objections to literature survey depth", "clustering critique points on contribution delineation"],
        "inputs": ["reviewer critiques of Introduction"],
        "outputs": ["B02_introduction_p1.json"],
        "key_results": ["The contribution list in the Introduction presents software features as scientific contributions"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 10
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/scripts/run_stage1.sh",
        "kind": "code",
        "what_it_is": "Bash automation script executing Stage 1 review finding clustering with LLM assistance across JSONL buckets for paper A or B.",
        "question": "How is the automated bucket-by-bucket review finding clustering and validation pipeline executed?",
        "method": ["parsing command-line paper target parameter (A or B)", "iterating over JSONL finding buckets", "invoking Codex clustering tool and running output validator"],
        "inputs": ["work/buckets_$P/*.jsonl"],
        "outputs": ["work/clusters_$P/*.json", "work/logs/*.last.txt"],
        "key_results": ["Stage 1: cluster each bucket with Codex. Resumable: skips buckets whose output validates"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })
    # 11
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/B_findings_tails.json",
        "kind": "report",
        "what_it_is": "Analysis document detailing reviewer self-contradictions and edge cases in the Paper B (Sensor) AI reviews.",
        "question": "What factual contradictions exist between different sections of the AI peer reviews for Paper B?",
        "method": ["identifying discrepancies between reviewer prompt instructions and responses", "evaluating reviewer consistency on background band frequency boundaries"],
        "inputs": ["raw review transcripts for Paper B"],
        "outputs": ["B_findings_tails.json"],
        "key_results": ["4. 7–10 Hz vs. 7–11 Hz Background Band: Response 1 (§6, §7.1, §7.4) repeatedly analyzes"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 12
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/A_findings_tails.json",
        "kind": "report",
        "what_it_is": "Analysis document detailing reviewer self-contradictions regarding section length and target word counts in Paper A reviews.",
        "question": "What conflicting target word counts and structural recommendations were given across the Paper A reviews?",
        "method": ["extracting word count targets across review sections", "documenting contradictory reviewer targets for Section 2"],
        "inputs": ["Paper A review transcripts"],
        "outputs": ["A_findings_tails.json"],
        "key_results": ["1. Main-article target word count for Section 2 (Materials and Methods):"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })
    # 13
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/Paper A Measurement (three AI reviews).txt",
        "kind": "report",
        "what_it_is": "Tabulated compendium of peer review findings from ChatGPT, Claude, and Gemini on Paper A submitted to Measurement.",
        "question": "What common validity, presentation, and methodological concerns were raised by independent AI reviewers of Paper A?",
        "method": ["tabulating reviewer comments with ID, type, location, severity, and verbatim quote", "aggregating critiques across three independent AI reviews"],
        "inputs": ["manuscript draft of Paper A"],
        "outputs": ["Paper A Measurement (three AI reviews).txt"],
        "key_results": ["Direct optical-versus-LDS displacement accuracy is not demonstrated"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })
    # 14
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/consolidation/work/Paper B Sensor (three AI reviews).txt",
        "kind": "report",
        "what_it_is": "Tabulated compendium of peer review findings from ChatGPT, Claude, and Gemini on Paper B submitted to Sensors.",
        "question": "What methodological and numerical criticisms were identified across multiple AI reviews of the Sensors paper?",
        "method": ["tabulating reviewer critiques with finding ID, type, location, and verbatim quotes", "evaluating consensus on timestamp jitter and resampling"],
        "inputs": ["manuscript draft of Paper B"],
        "outputs": ["Paper B Sensor (three AI reviews).txt"],
        "key_results": ["Timestamp jitter of 0.7–1.4 ms SD is stamp noise rather than true sampling jitter"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 15
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/TEXT/Paper B Sensor - Claude.txt",
        "kind": "report",
        "what_it_is": "Full verbatim peer review report generated by Claude assessing Paper B against MDPI Sensors standards.",
        "question": "How does Paper B perform against journal peer review criteria regarding spectral recovery and camera timing?",
        "method": ["evaluating spectral analysis rigor and timestamp handling", "identifying methodological vulnerabilities in dominant frequency claims"],
        "inputs": ["manuscript draft for Sensors"],
        "outputs": ["Paper B Sensor - Claude.txt"],
        "key_results": ["ROLE: You are simultaneously (1) a senior research supervisor"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 16
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/TEXT/Paper A Measurement - ChatGPT.txt",
        "kind": "report",
        "what_it_is": "Full verbatim peer review report generated by ChatGPT evaluating Paper A against Elsevier Measurement standards.",
        "question": "What technical and structural flaws are highlighted by ChatGPT regarding Paper A's displacement reconstruction claims?",
        "method": ["reviewing optical tracking methodology", "critiquing displacement proxy claims against reference laser data"],
        "inputs": ["manuscript draft for Measurement"],
        "outputs": ["Paper A Measurement - ChatGPT.txt"],
        "key_results": ["ROLE: You are simultaneously (1) a senior research supervisor"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })
    # 17
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/TEXT/Paper A Measurement - Claude.txt",
        "kind": "report",
        "what_it_is": "Comprehensive peer review evaluation by Claude critiquing Paper A's experimental rigor and multi-camera synchronization.",
        "question": "What critical weaknesses does Claude identify in Paper A's synchronization and comparison methodologies?",
        "method": ["analyzing camera synchronization and pose estimation claims", "evaluating empirical evidence supporting cross-camera agreement"],
        "inputs": ["Paper A manuscript"],
        "outputs": ["Paper A Measurement - Claude.txt"],
        "key_results": ["ROLE: You are simultaneously (1) a senior research supervisor"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })
    # 18
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/TEXT/Paper A Measurement - Gemini.txt",
        "kind": "report",
        "what_it_is": "Independent peer review report by Gemini analyzing Paper A's multi-camera displacement reconstruction.",
        "question": "What specific presentation and validation concerns are raised by Gemini regarding Paper A's methodology?",
        "method": ["reviewing multi-camera displacement claims", "assessing adequacy of laser sensor comparison data"],
        "inputs": ["Paper A manuscript"],
        "outputs": ["Paper A Measurement - Gemini.txt"],
        "key_results": ["ROLE: You are simultaneously (1) a senior research supervisor"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })
    # 19
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/TEXT/Paper B Sensor - Gemini.txt",
        "kind": "report",
        "what_it_is": "Independent peer review critique by Gemini evaluating Paper B's spectral analysis and timestamp characterization.",
        "question": "How does Gemini evaluate the defensibility of reference-blind spectral feature extraction on native timestamps?",
        "method": ["assessing native timestamp periodograms", "scrutinizing dominant frequency recovery claims across 21 conditions"],
        "inputs": ["Paper B manuscript"],
        "outputs": ["Paper B Sensor - Gemini.txt"],
        "key_results": ["ROLE: You are simultaneously (1) a senior research supervisor"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    # 20
    records.append({
        "path": "/mnt/space/adev/research/publications/final review of paper 2 (Measurement, Sensor)/TEXT/Paper B Sensor - ChatGPT.txt",
        "kind": "report",
        "what_it_is": "Full text peer review report generated by ChatGPT for the MDPI Sensors manuscript on native-timestamp spectral analysis.",
        "question": "What critical recommendations does ChatGPT provide regarding Paper B's claims on non-uniform sampling?",
        "method": ["evaluating spectral methods under non-uniform sampling", "recommending defensible boundaries for dominant frequency claims"],
        "inputs": ["Paper B draft manuscript"],
        "outputs": ["Paper B Sensor - ChatGPT.txt"],
        "key_results": ["ROLE: You are simultaneously (1) a senior research supervisor"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })
    
    # 21..23: Group 2
    # 21
    records.append({
        "path": "/mnt/phd_data/phd_master/04_code_software/paper2-rebuild-2026-10_snapshot/config/paths.yaml",
        "kind": "config",
        "what_it_is": "Root filesystem path specification mapping input dataset directories, bag stores, and frozen detection outputs for Paper 2 rebuild.",
        "question": "Where are the primary read-only raw rosbags and static camera datasets located on the filesystem?",
        "method": ["defining filesystem mappings for raw bags", "setting input directories for wtt_main, wtt_5sec, and static tests"],
        "inputs": ["local filesystem directory layout"],
        "outputs": ["paths.yaml"],
        "key_results": ["Inputs are read-only; outputs never overwrite older results."],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })
    # 22
    records.append({
        "path": "/mnt/phd_data/phd_master/04_code_software/paper2-rebuild-2026-10_snapshot/config/requirements.lock.txt",
        "kind": "config",
        "what_it_is": "Pinned Python package environment lockfile specifying exact library versions for reproducible Paper 2 execution.",
        "question": "What exact Python package versions are required for reproducible pipeline execution in the rebuild environment?",
        "method": ["pinning Python dependency versions", "locking scientific computing and ROS bag handling libraries"],
        "inputs": ["python environment dependencies"],
        "outputs": ["requirements.lock.txt"],
        "key_results": ["numpy==2.5.4"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })
    # 23
    records.append({
        "path": "/mnt/phd_data/phd_master/05_publications/p02_sensors_windtunnel/scripts/table_2025_ldv_primary.csv",
        "kind": "data-table",
        "what_it_is": "Benchmark comparison table tabulating camera versus laser sensor RMS displacements and ratios across wind-tunnel RPM conditions.",
        "question": "What are the bending and torsion RMS displacement values and camera-to-laser ratios across wind-tunnel test conditions?",
        "method": ["computing bending and torsion RMS from camera time histories", "calculating reference laser RMS from paired D-series files", "deriving scaling ratios and peak displacements"],
        "inputs": ["camera displacement time series", "laser sensor D01-D20 recordings"],
        "outputs": ["table_2025_ldv_primary.csv"],
        "key_results": ["20,,D01,0.0178,0.1120,0.1589,0.0342,0.2660,0.1286,0.0665,0.2800,30.50,1831,7200"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2B-comparison",
        "open_questions": []
    })

    return records

if __name__ == '__main__':
    recs = build_all_p05()
    print(f"Verifying {len(recs)} records...")
    for i, r in enumerate(recs):
        ok, msg = verify_record(r)
        if not ok:
            print(f"Error in {i} ({r['path']}): {msg}")
            sys.exit(1)
    print("All records 0-23 passed successfully!")
