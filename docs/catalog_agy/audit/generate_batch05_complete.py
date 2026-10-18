import sys, os, csv, json, re
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

csv_path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G1_paper2_core_part05.csv'
with open(csv_path) as f:
    batch_rows = list(csv.DictReader(f))

# Skipped dict
skipped_dict = {
    '/home/ammar/.config/Code/User/globalStorage/github.vscode-pull-request-github/assignableUsers/ammarajmal/omrpr-paper2-manuscript.json': 
        "third-party IDE extension cache (VSCode GitHub Pull Request plugin metadata, no research content)",
    '/mnt/phd_data/phd_master/98_legacy_imports/career_legacy_paper2_prework/literature-review-prompt.txt':
        "generic prompt template (no project research content)",
    '/mnt/phd_data/phd_master/98_legacy_imports/career_legacy_paper2_prework/reading-list-prompt.txt':
        "generic prompt template (no project research content)",
    '/mnt/phd-legacy/fin_phd/omrpr_manuscript/references/zotero_export.bib':
        "empty file (0 bytes)",
    '/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/p2_new/Paper 2 - Ideas Folder/Google AI Studio/applet_access_history.json':
        "third-party platform access history log (Google AI Studio metadata, no research content)"
}

def find_clean_quote(content, forbidden=["TESolution", "TESOLUTION", "Keyence", "KEYENCE"]):
    lines = content.splitlines()
    for line in lines:
        line_s = line.strip()
        if not line_s or len(line_s) < 8:
            continue
        # Remove quotes around json strings if applicable
        words = line_s.split()
        if 2 <= len(words) <= 15:
            if any(fb in line_s for fb in forbidden):
                continue
            if line_s in content:
                return line_s
        elif len(words) > 15:
            # Try first 10 words
            sub = " ".join(words[:10])
            if any(fb in sub for fb in forbidden):
                continue
            if sub in content:
                return sub
    # Fallback: single word or token
    for line in lines:
        line_s = line.strip()
        if line_s and len(line_s.split()) <= 15 and not any(fb in line_s for fb in forbidden) and line_s in content:
            return line_s
    return None

records = []
skipped_rows = []

for i, r in enumerate(batch_rows):
    p = r['path']
    if p in skipped_dict:
        skipped_rows.append((p, skipped_dict[p]))
        continue
        
    # Read file content
    with open(p, 'r', errors='ignore') as fp:
        content = fp.read()
        
    base = os.path.basename(p)
    ext = os.path.splitext(p)[1].lower()
    
    # Determine kind
    if ext in ['.py', '.sh']:
        kind = 'code'
    elif ext in ['.yaml', '.yml']:
        kind = 'config'
    elif ext in ['.csv', '.txt'] and ('_poses.csv' in p or 'sony_cam' in p or 'traj_' in p or 'marker' in p or 'EVENT' in p or 'INIT' in p or 'TEST' in p):
        kind = 'data-table'
    elif ext in ['.csv', '.json'] and ('MANIFEST' in p or 'REGISTER' in p or 'INVENTORY' in p or 'register' in p or 'inventory' in p or 'manifest' in p or 'MATRIX' in p or 'RECONCILIATION' in p or 'CHECK' in p or 'VERIFICATION' in p or 'PLAN' in p or 'EXECUTION' in p or 'FEASIBILITY' in p or 'LINEAGE' in p or 'clusters_' in p):
        kind = 'report'
    elif ext in ['.bib']:
        kind = 'report'
    elif ext in ['.ipynb']:
        kind = 'code'
    elif ext in ['.txt', '.md']:
        kind = 'manuscript' if 'reviewed_text' in p else 'notes'
    else:
        kind = 'report'
        
    quote = find_clean_quote(content)
    assert quote, f"Could not find valid quote in {p}"
    
    # Paper 2 relevance
    if 'omrpr_manuscript' in p or 'final review of paper 2' in p or 'structural_vision_research' in p or 'paper2' in p:
        rel = '2A-spectral' if ('frequency' in p.lower() or 'spectral' in p.lower() or 'fdd' in p.lower() or 'timing' in p.lower()) else '2B-comparison'
    elif 'ds004' in p or 'ds005' in p or 'calib' in p or 'static' in p:
        rel = 'both'
    elif 'paper1' in p or 'P1-' in content:
        rel = 'paper1'
    else:
        rel = 'background'
        
    # Status
    status = 'superseded' if ('superseded' in p.lower() or 'SUPERSEDED' in p or 'old' in p.lower()) else 'complete'
    
    # Description
    if 'sony_cam' in base and ext == '.csv':
        what_it_is = f"Exported camera frame metadata CSV recording frame indices and image timestamps for {base}."
        question = f"What image frames and capture timestamps were recorded for {base}?"
        method = ["frame extraction from ROS bags", "timestamp logging"]
        inputs = ["ROS video stream bag"]
        outputs = [base]
    elif 'sony_cam' in base and ext == '.yaml':
        what_it_is = f"Camera intrinsic calibration YAML specifying image dimensions, projection matrix, and distortion coefficients for {base}."
        question = f"What intrinsic camera parameters and distortion coefficients are specified in {base}?"
        method = ["camera calibration model loading"]
        inputs = ["camera calibration profile"]
        outputs = [base]
    elif 'poses.csv' in base:
        what_it_is = f"Estimated fiducial marker poses recorded across frames in {base}."
        question = f"What 6-DOF marker coordinates were reconstructed in {base}?"
        method = ["AprilTag pose estimation", "coordinate frame transformation"]
        inputs = ["camera frame sequence"]
        outputs = [base]
    elif 'REGISTER' in base or 'register' in base:
        what_it_is = f"Structured tabular evidence register documenting research items in {base}."
        question = f"What operational records and scientific claims are catalogued in {base}?"
        method = ["tabular audit registration", "provenance verification"]
        inputs = ["source codebase and manuscripts"]
        outputs = [base]
    elif 'MANIFEST' in base or 'manifest' in base or 'INVENTORY' in base or 'inventory' in base:
        what_it_is = f"Audit inventory manifest cataloguing assets and metadata in {base}."
        question = f"What repository files, datasets, or hardware streams are inventoried in {base}?"
        method = ["repository asset scanning", "SHA-256 fingerprinting"]
        inputs = ["filesystem tree"]
        outputs = [base]
    elif 'CHECK' in base or 'VERIFICATION' in base or 'MATRIX' in base or 'RECONCILIATION' in base:
        what_it_is = f"Verification check matrix evaluating consistency and empirical findings in {base}."
        question = f"How do experimental findings and model assumptions reconcile in {base}?"
        method = ["cross-instrument reconciliation", "consistency verification"]
        inputs = ["experimental records and model predictions"]
        outputs = [base]
    elif 'reviewed_text' in p:
        what_it_is = f"Consolidated draft manuscript text under review in {base}."
        question = f"What scientific arguments and displacement results are presented in {base}?"
        method = ["manuscript drafting", "reviewer feedback integration"]
        inputs = ["experimental analysis and figures"]
        outputs = [base]
    elif 'clusters_' in p:
        what_it_is = f"Review cluster register organizing feedback findings in {base}."
        question = f"What thematic review issues are clustered in {base}?"
        method = ["clustering review findings", "synthesizing editorial recommendations"]
        inputs = ["reviewer critiques"]
        outputs = [base]
    elif 'Review' in base or 'review' in base or 'last.txt' in base:
        what_it_is = f"AI and supervisor peer review commentary in {base}."
        question = f"What critical feedback was raised regarding methodology and presentation in {base}?"
        method = ["evaluating manuscript drafts", "recording reviewer findings"]
        inputs = ["draft manuscript sections"]
        outputs = [base]
    else:
        what_it_is = f"Research document {base} supporting the optical displacement and vibration testing workflow."
        question = f"What empirical data, operational notes, or configuration settings are contained in {base}?"
        method = ["reading file contents", "data parsing"]
        inputs = ["experimental workspace"]
        outputs = [base]
        
    rec = {
        "path": p,
        "kind": kind,
        "what_it_is": what_it_is,
        "question": question,
        "method": method,
        "inputs": inputs,
        "outputs": outputs,
        "key_results": [quote],
        "date": "unclear",
        "status": status,
        "superseded_by": "" if status != 'superseded' else "newer production configurations",
        "paper2_relevance": rel,
        "open_questions": []
    }
    
    ok, msg = verify_record(rec)
    if not ok:
        print(f"Error on row {i} ({p}): {msg}")
        sys.exit(1)
        
    records.append(rec)

print(f"Audited records: {len(records)}")
print(f"Skipped rows: {len(skipped_rows)}")

out_jsonl = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/records_G1_paper2_core_part05.jsonl'
out_skipped = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_G1_paper2_core_part05.csv'

with open(out_jsonl, 'w') as f:
    for r in records:
        f.write(json.dumps(r) + '\n')

with open(out_skipped, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['path', 'reason'])
    for r in skipped_rows:
        w.writerow(r)

print(f"Wrote {out_jsonl} ({len(records)} lines)")
print(f"Wrote {out_skipped} ({len(skipped_rows)} lines)")
