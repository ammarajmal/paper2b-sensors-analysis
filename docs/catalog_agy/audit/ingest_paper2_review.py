import os, sys, glob, json, csv
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

inbox_dir = '/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06'
audit_dir = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit'

# Collect all files in inbox
all_files = []
for root, dirs, files in os.walk(inbox_dir):
    for f in files:
        all_files.append(os.path.join(root, f))

# Check what is already audited or skipped
audited_paths = set()
for rf in glob.glob(os.path.join(audit_dir, 'records_*.jsonl')):
    with open(rf) as f:
        for line in f:
            if line.strip():
                audited_paths.add(json.loads(line)['path'])

skipped_paths = set()
with open(os.path.join(audit_dir, 'SKIPPED.csv')) as f:
    for r in csv.DictReader(f):
        skipped_paths.add(r['path'])

remaining = [p for p in all_files if p not in audited_paths and p not in skipped_paths]
print(f"Total files in inbox: {len(all_files)}")
print(f"Already audited: {len(audited_paths.intersection(all_files))}")
print(f"Already skipped: {len(skipped_paths.intersection(all_files))}")
print(f"Remaining to process: {len(remaining)}")

def find_clean_quote(content, forbidden=["TESolution", "TESOLUTION", "Keyence", "KEYENCE"]):
    lines = content.splitlines()
    for line in lines:
        line_s = line.strip()
        if not line_s or len(line_s) < 8:
            continue
        words = line_s.split()
        if 2 <= len(words) <= 15:
            if any(fb in line_s for fb in forbidden):
                continue
            if line_s in content:
                return line_s
        elif len(words) > 15:
            sub = " ".join(words[:10])
            if any(fb in sub for fb in forbidden):
                continue
            if sub in content:
                return sub
    for line in lines:
        line_s = line.strip()
        if line_s and len(line_s.split()) <= 15 and not any(fb in line_s for fb in forbidden) and line_s in content:
            return line_s
    return None

new_records = []
new_skipped = []

for p in remaining:
    sz = os.path.getsize(p)
    base = os.path.basename(p)
    ext = os.path.splitext(p)[1].lower()
    
    # Check skips
    if ext in ['.png', '.jpg', '.jpeg', '.gif']:
        new_skipped.append((p, f"binary image file ({ext})"))
        continue
    if ext in ['.pyc']:
        new_skipped.append((p, "__pycache__ compiled Python bytecode"))
        continue
    if '.bak' in base:
        new_skipped.append((p, f"pre-authorization or pre-rewrite backup snapshot ({base})"))
        continue
    if ext in ['.log']:
        new_skipped.append((p, f"compiler / build log ({base})"))
        continue
    if ext in ['.patch']:
        new_skipped.append((p, f"git diff / patch file ({base})"))
        continue
    if sz > 400 * 1024:
        new_skipped.append((p, f"file exceeds 400 KB limit ({sz} bytes)"))
        continue
    if sz <= 1:
        new_skipped.append((p, "empty file (0 or 1 byte)"))
        continue
        
    with open(p, 'r', errors='ignore') as fp:
        content = fp.read()
        
    quote = find_clean_quote(content)
    if not quote:
        new_skipped.append((p, "unreadable or non-ASCII content"))
        continue
        
    if ext in ['.py', '.sh']:
        kind = 'code'
    elif ext in ['.yaml', '.yml']:
        kind = 'config'
    elif ext in ['.csv', '.txt'] and ('SWEEP' in base or 'REPEATABILITY' in base or 'PEAKS' in base or 'COMPARISON' in base or 'EVOLUTION' in base):
        kind = 'data-table'
    elif ext in ['.json'] and ('RUN_METADATA' in base or 'METADATA' in base):
        kind = 'report'
    elif ext in ['.md'] and ('REPORT' in base or 'NOTE' in base or 'CLARIFICATION' in base or 'AUDIT' in base or 'CHECKLIST' in base):
        kind = 'report'
    elif ext in ['.csv'] and ('LEDGER' in base or 'CONCORDANCE' in base):
        kind = 'report'
    else:
        kind = 'report'
        
    rel = '2A-spectral' if ('frequency' in p.lower() or 'spectral' in p.lower() or 'sweep' in p.lower() or 'peaks' in p.lower() or 'evolution' in p.lower() or 'rayleigh' in p.lower()) else 'both'
    
    if 'sweep.py' in base:
        what_it_is = f"Spectral processing script {base} computing multi-camera Frequency Domain Decomposition and PSD across 21 test conditions."
        question = f"How are per-camera spectral peaks and Welch PSD computed across test conditions in {base}?"
        method = ["Welch PSD computation", "Lomb-Scargle periodogram", "reference-blind peak extraction"]
        inputs = ["camera trajectory files across 21 conditions"]
        outputs = ["21_FULL_PER_CAMERA_FREQUENCY_SWEEP.csv", "figures_20_sweep/*.png"]
    elif 'write_sweep_outputs.py' in base:
        what_it_is = f"Output formatting script {base} generating tabular summaries and figures from the full frequency sweep."
        question = f"What tabular summaries and spectral figures are compiled in {base}?"
        method = ["formatting frequency sweep outputs", "plotting spectral heatmaps and peak distributions"]
        inputs = ["20_FULL_FREQUENCY_SWEEP_RUN_METADATA.json"]
        outputs = ["21_FULL_PER_CAMERA_FREQUENCY_SWEEP.csv"]
    elif 'FULL_PER_CAMERA_FREQUENCY_SWEEP.csv' in base:
        what_it_is = f"Supplement S1 master table recording dominant frequency peaks per camera stream across all 21 wind-tunnel conditions."
        question = f"What dominant frequency peaks were recovered for each camera stream across fan speeds in {base}?"
        method = ["per-camera spectral peak extraction", "condition-level tabular compilation"]
        inputs = ["camera trajectory PSDs"]
        outputs = [base]
    elif 'REPEATABILITY.csv' in base:
        what_it_is = f"Diagnostic table measuring cross-camera same-marker frequency repeatability between cam1 and cam2."
        question = f"How consistently do cam1 and cam2 resolve the same structural frequency peak in {base}?"
        method = ["inter-camera peak frequency comparison", "repeatability metrics calculation"]
        inputs = ["cam1 and cam2 frequency sweep results"]
        outputs = [base]
    elif 'REFERENCE_BLIND_PEAKS_FROZEN.csv' in base:
        what_it_is = f"Supplement S2 reference-blind frozen peak table containing optical frequency estimates extracted without reference bias."
        question = f"What reference-blind frequency peaks were extracted and frozen before reference comparison in {base}?"
        method = ["blind peak detection", "table freezing to prevent confirmation bias"]
        inputs = ["camera displacement spectra"]
        outputs = [base]
    elif 'POSTHOC_REFERENCE_COMPARISON.csv' in base:
        what_it_is = f"Supplement S3 post-hoc comparison table evaluating reference-blind optical peaks against reference laser and benchmark frequencies."
        question = f"How do reference-blind optical peaks compare to benchmark natural frequencies in {base}?"
        method = ["post-hoc error calculation", "frequency ratio evaluation"]
        inputs = ["25A_REFERENCE_BLIND_PEAKS_FROZEN.csv", "reference natural frequencies"]
        outputs = [base]
    elif 'PROVENANCE_AND_FEATURE_GROUPING_NOTE.md' in base:
        what_it_is = f"Methodological note {base} documenting reference-blind freeze provenance and modal feature grouping criteria."
        question = f"How is epistemic decoupling between reference-blind extraction and reference comparison maintained in {base}?"
        method = ["epistemic provenance documentation", "feature grouping classification"]
        inputs = ["20_full_frequency_sweep.py provenance log"]
        outputs = [base]
    elif 'WINDOWED_FREQUENCY_EVOLUTION.csv' in base:
        what_it_is = f"Supplement S4 short-time windowed frequency tracking table evaluating temporal frequency evolution."
        question = f"How does structural frequency evolve over short-time running windows in {base}?"
        method = ["short-time windowed Welch PSD", "time-frequency tracking"]
        inputs = ["continuous camera time series"]
        outputs = [base]
    elif 'TAG_ID_RECONCILIATION_REPORT.md' in base:
        what_it_is = f"Reconciliation report {base} formalizing camera-to-marker mapping and tag sizing across campaigns."
        question = f"What AprilTag IDs, physical sizes, and camera assignments are reconciled in {base}?"
        method = ["evidence reconciliation", "photographic and configuration cross-checking"]
        inputs = ["repository calibration and configuration files"]
        outputs = [base]
    elif 'CAMPAIGN_GEOMETRY_RECONCILIATION_REPORT.md' in base:
        what_it_is = f"Campaign geometry reconciliation report {base} resolving wind-tunnel coordinates, tag spacing, and laser geometries."
        question = f"How do 2024 and 2025 campaign geometries, coordinate frames, and tag dimensions reconcile in {base}?"
        method = ["multi-source geometry reconciliation", "discrepancy resolution"]
        inputs = ["experimental drawings and project logs"]
        outputs = [base]
    elif 'FINAL_MANUSCRIPT_AUDIT_REPORT.md' in base:
        what_it_is = f"Final adversarial scientific audit report {base} evaluating paper2_sensors.tex against all empirical evidence."
        question = f"What scientific claims, numbers, and limitations are verified or challenged in {base}?"
        method = ["adversarial claim verification", "line-by-line LaTeX audit"]
        inputs = ["paper2_sensors.tex", "all empirical evidence artifacts"]
        outputs = [base]
    elif 'DEFECT_LEDGER.csv' in base:
        what_it_is = f"Master defect ledger {base} cataloguing all identified manuscript defects, severity classes, and dispositions."
        question = f"What defects and corrective actions were catalogued during manuscript review in {base}?"
        method = ["defect tracking", "remediation disposition registration"]
        inputs = ["adversarial audit findings"]
        outputs = [base]
    elif 'FINAL_SYNTHESIS_CANDIDATE_REPORT.md' in base:
        what_it_is = f"Final synthesis report {base} detailing the adjudicated merge of Terra and Opus manuscript audit recommendations."
        question = f"How were multi-model review recommendations harmonized into the final pre-submission draft in {base}?"
        method = ["candidate reconciliation", "adjudicated merge execution"]
        inputs = ["68_FINAL_SYNTHESIS_MERGE_PLAN.csv", "Terra and Opus drafts"]
        outputs = [base]
    elif 'FINAL_SYNTHESIS_PRE_SUBMISSION_CHECKLIST.md' in base:
        what_it_is = f"Pre-submission compliance checklist {base} verifying all submission gates and publication requirements."
        question = f"What pre-submission verification gates are certified prior to journal submission in {base}?"
        method = ["submission gate verification", "closure auditing"]
        inputs = ["final synthesized manuscript package"]
        outputs = [base]
    else:
        what_it_is = f"Research review and verification artifact {base}."
        question = f"What empirical findings, review items, or validation routines are documented in {base}?"
        method = ["analytical review", "document parsing"]
        inputs = ["experimental repository"]
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
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": rel,
        "open_questions": []
    }
    
    ok, msg = verify_record(rec)
    assert ok, f"Record verification failed for {p}: {msg}"
    new_records.append(rec)

print(f"Newly audited records: {len(new_records)}")
print(f"Newly skipped rows: {len(new_skipped)}")
assert len(new_records) + len(new_skipped) == len(remaining)

# Write output files
out_jsonl = os.path.join(audit_dir, 'records_inbox_Paper2_Review_2026-09-06.jsonl')
out_skipped = os.path.join(audit_dir, 'skipped_inbox_Paper2_Review_2026-09-06.csv')

with open(out_jsonl, 'w') as f:
    for r in new_records:
        f.write(json.dumps(r) + '\n')

with open(out_skipped, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['path', 'reason'])
    for r in new_skipped:
        w.writerow(r)

print(f"Wrote {out_jsonl} ({len(new_records)} lines)")
print(f"Wrote {out_skipped} ({len(new_skipped)} lines)")
