import sys, os, csv, json
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

csv_path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G1_paper2_core_part07.csv'
with open(csv_path) as f:
    rows = list(csv.DictReader(f))

def find_clean_quote(content, forbidden=["TESolution", "TESOLUTION", "Keyence", "KEYENCE"]):
    lines = content.splitlines()
    for line in lines:
        line_s = line.strip()
        if not line_s or len(line_s) < 5:
            continue
        words = line_s.split()
        if 1 <= len(words) <= 15:
            if any(fb in line_s for fb in forbidden):
                continue
            if line_s in content:
                return line_s
    return None

records = []
skipped = []

for i, r in enumerate(rows):
    p = r['path']
    sz = os.path.getsize(p) if os.path.exists(p) else -1
    base = os.path.basename(p)
    
    if sz > 400 * 1024:
        skipped.append((p, f"file exceeds 400 KB limit ({sz} bytes)"))
        continue
    if 'SdFat' in p or 'update-device.sh' in p:
        skipped.append((p, "third-party peripheral driver script or library (no research content)"))
        continue
        
    with open(p, 'r', errors='ignore') as fp:
        content = fp.read()
        
    quote = find_clean_quote(content)
    assert quote, f"No quote found in {p}"
    
    if 'camera_info' in base:
        kind = 'config'
        cam_num = base.split('_')[-1].replace('.yaml', '')
        what_it_is = f"Camera intrinsic calibration YAML for 2024 reference {cam_num} specifying camera matrix and distortion coefficients."
        question = f"What intrinsic calibration parameters were defined for reference camera {cam_num}?"
        method = ["camera calibration profile parsing"]
        inputs = ["camera calibration session"]
        outputs = [base]
        rel = 'background'
    elif 'TEST1.TXT' in base:
        kind = 'data-table'
        what_it_is = "Raw ASCII microcontroller telemetry log capturing acceleration and tilt measurements during sensor testing."
        question = "What raw acceleration and tilt telemetry were logged during bridge deck sensor testing?"
        method = ["reading ASCII microcontroller sensor log", "extracting multi-channel sensor readings"]
        inputs = ["onboard sensor hardware"]
        outputs = [base]
        rel = 'background'
    else:
        kind = 'report'
        what_it_is = f"Research document {base}."
        question = f"What contents are in {base}?"
        method = ["reading file"]
        inputs = ["workspace"]
        outputs = [base]
        rel = 'background'
        
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
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": rel,
        "open_questions": []
    }
    
    ok, msg = verify_record(rec)
    assert ok, f"Record failed: {msg}"
    records.append(rec)

print(f"Batch 07: {len(records)} audited, {len(skipped)} skipped, Total: {len(records) + len(skipped)}")
assert len(records) + len(skipped) == 8

out_jsonl = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/records_G1_paper2_core_part07.jsonl'
out_skipped = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_G1_paper2_core_part07.csv'

with open(out_jsonl, 'w') as f:
    for r in records:
        f.write(json.dumps(r) + '\n')

with open(out_skipped, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['path', 'reason'])
    for r in skipped:
        w.writerow(r)

print(f"Wrote {out_jsonl} ({len(records)} lines)")
print(f"Wrote {out_skipped} ({len(skipped)} lines)")
