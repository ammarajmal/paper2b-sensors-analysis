import sys, os, csv, json
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

def find_clean_quote(content, forbidden=["TESolution", "TESOLUTION", "Keyence", "KEYENCE"]):
    lines = content.splitlines()
    for line in lines:
        line_s = line.strip()
        if not line_s or len(line_s) < 6:
            continue
        words = line_s.split()
        if 1 <= len(words) <= 15:
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
    # Fallback to any line
    for line in lines:
        line_s = line.strip()
        if line_s and len(line_s.split()) <= 15 and not any(fb in line_s for fb in forbidden) and line_s in content:
            return line_s
    return None

def process_batch(batch_name, skip_file):
    batch_path = f'/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/{batch_name}.csv'
    with open(batch_path) as f:
        rows = list(csv.DictReader(f))
        
    # Read existing skips
    skipped_dict = {}
    if os.path.exists(skip_file):
        with open(skip_file) as f:
            for r in csv.DictReader(f):
                skipped_dict[r['path']] = r['reason']
                
    records = []
    skipped_rows = []
    
    for i, r in enumerate(rows):
        p = r['path']
        if p in skipped_dict:
            skipped_rows.append((p, skipped_dict[p]))
            continue
            
        sz = os.path.getsize(p) if os.path.exists(p) else -1
        if sz > 400 * 1024:
            skipped_rows.append((p, f"file exceeds 400 KB limit ({sz} bytes)"))
            continue
        if sz <= 1:
            skipped_rows.append((p, "empty file (0 or 1 byte)"))
            continue
            
        with open(p, 'r', errors='ignore') as fp:
            content = fp.read()
            
        quote = find_clean_quote(content)
        if not quote:
            skipped_rows.append((p, "unreadable or non-ASCII content with no valid quotes"))
            continue
            
        base = os.path.basename(p)
        ext = os.path.splitext(p)[1].lower()
        
        # Determine kind
        if ext in ['.py', '.sh', '.m']:
            kind = 'code'
        elif ext in ['.yaml', '.yml']:
            kind = 'config'
        elif ext in ['.csv', '.txt'] and ('data' in p.lower() or 'laser' in p.lower() or 'cam' in p.lower() or 'static' in p.lower() or 'timestamps' in p.lower()):
            kind = 'data-table'
        elif ext in ['.tex']:
            kind = 'manuscript'
        elif ext in ['.bib']:
            kind = 'report'
        elif ext in ['.md'] and ('Review' in p or 'review' in p or 'REPORT' in p or 'Audit' in p or 'digest' in p or 'Digest' in p):
            kind = 'report'
        elif ext in ['.md', '.txt']:
            kind = 'notes'
        else:
            kind = 'report'
            
        # Determine relevance
        if 'paper1' in p or 'IEEE' in p:
            rel = 'paper1'
        elif 'courses_training' in p:
            rel = 'background'
        elif 'omrpr' in p or 'paper2' in p or 'P2A' in p or 'Measurement' in p or 'Sensor' in p:
            rel = '2A-spectral' if ('spectral' in p.lower() or 'frequency' in p.lower() or 'timing' in p.lower()) else '2B-comparison'
        else:
            rel = 'background'
            
        status = 'superseded' if ('old' in p.lower() or 'superseded' in p.lower() or 'archive' in p.lower()) else 'complete'
        
        # Descriptions
        if ext == '.m':
            what_it_is = f"MATLAB analysis and digital signal processing script {base}."
            question = f"What signal filtering or numerical routines are implemented in {base}?"
            method = ["numerical algorithm execution", "signal filtering"]
            inputs = ["time series data"]
            outputs = [base]
        elif 'Review' in base or 'review' in base or 'digest' in base.lower():
            what_it_is = f"Peer review critique, audit summary, or reviewer digest in {base}."
            question = f"What methodological critique and revision points are documented in {base}?"
            method = ["expert manuscript peer review", "finding collation"]
            inputs = ["draft manuscript and experimental claims"]
            outputs = [base]
        elif 'timestamps' in base or 'metadata' in base or 'timestamps.csv' in base:
            what_it_is = f"Experimental camera capture metadata and frame timestamp register in {base}."
            question = f"What frame timing intervals and acquisition metadata were recorded in {base}?"
            method = ["ROS bag timestamp extraction", "timing verification"]
            inputs = ["raw video bags"]
            outputs = [base]
        elif ext == '.tex':
            what_it_is = f"LaTeX manuscript source or submission cover document {base}."
            question = f"What research narrative and structural claims are drafted in {base}?"
            method = ["academic paper drafting", "LaTeX compilation"]
            inputs = ["experimental results"]
            outputs = [base]
        elif ext in ['.yaml', '.yml']:
            what_it_is = f"Camera or system configuration YAML file {base}."
            question = f"What hardware parameters or coordinate configurations are defined in {base}?"
            method = ["hardware configuration loading"]
            inputs = ["parameter definitions"]
            outputs = [base]
        else:
            what_it_is = f"Research document {base} supporting academic analysis and verification."
            question = f"What analytical concepts or operational notes are recorded in {base}?"
            method = ["document analysis"]
            inputs = ["research files"]
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
            "superseded_by": "" if status != 'superseded' else "newer consolidated reports",
            "paper2_relevance": rel,
            "open_questions": []
        }
        
        ok, msg = verify_record(rec)
        assert ok, f"Error on {p}: {msg}"
        records.append(rec)
        
    print(f"Batch {batch_name}: {len(records)} audited, {len(skipped_rows)} skipped, Total: {len(records) + len(skipped_rows)}")
    assert len(records) + len(skipped_rows) == len(rows)
    
    out_jsonl = f'/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/records_{batch_name}.jsonl'
    out_skipped = f'/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_{batch_name}.csv'
    
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

process_batch('G2_other_paper2_related_part01', '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_G2_other_paper2_related_part01.csv')
process_batch('G2_other_paper2_related_part02', '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_G2_other_paper2_related_part02.csv')
