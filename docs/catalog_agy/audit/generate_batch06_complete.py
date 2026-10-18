import sys, os, csv, json
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

csv_path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G1_paper2_core_part06.csv'
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
        elif len(words) > 15:
            sub = " ".join(words[:10])
            if any(fb in sub for fb in forbidden):
                continue
            if sub in content:
                return sub
    return None

records = []
skipped = []

for i, r in enumerate(rows):
    p = r['path']
    sz = os.path.getsize(p) if os.path.exists(p) else -1
    base = os.path.basename(p)
    
    if sz <= 1:
        skipped.append((p, "empty file (0 or 1 byte)"))
        continue
    if sz > 400 * 1024:
        skipped.append((p, f"file exceeds 400 KB limit ({sz} bytes)"))
        continue
    if any(x in p for x in ['Unishox2', 'SdFat', 'Adafruit', 'uSDFS', 'FastLZ', 'STM32', 'E-Paper_code', 'SparkFun', 'rocketscream', 'SimpleDSP', 'InterpolationLib', 'TinyRTCLib', 'I2CScanner', 'TinyWireM', 'Streaming', 'WiFi101', 'MPU6050']):
        skipped.append((p, "third-party embedded library, hardware driver, or example (no research content)"))
        continue
        
    # Read content
    with open(p, 'r', errors='ignore') as fp:
        content = fp.read()
        
    quote = find_clean_quote(content)
    assert quote, f"No quote found in {p}"
    
    if base in ['T1.csv', 'B1.csv']:
        kind = 'data-table'
        mode = 'torsion' if 'T1' in base else 'bending'
        what_it_is = f"Free vibration {mode} raw displacement time series exported from facility laser reference measurement."
        question = f"What free vibration {mode} response was recorded in reference file {base}?"
        method = ["laser displacement sensor acquisition", "free-vibration transient logging"]
        inputs = ["laser sensor hardware"]
        outputs = [base]
        rel = '2B-comparison'
    elif 'names.txt' in base:
        kind = 'notes'
        what_it_is = "Reference notes listing researcher names associated with sensor research."
        question = "What researcher names are listed for attribution in names.txt?"
        method = ["reading reference notes"]
        inputs = ["project documentation"]
        outputs = [base]
        rel = 'background'
    elif '하드웨어' in base:
        kind = 'notes'
        what_it_is = "Hardware setup notes in Korean detailing nRF transceiver and I2C FRAM connections."
        question = "What hardware pinout and transceiver configuration is specified for the sensor rig?"
        method = ["microcontroller hardware wiring"]
        inputs = ["sensor hardware components"]
        outputs = [base]
        rel = 'background'
    elif 'UPDATES.txt' in base:
        kind = 'code'
        what_it_is = "Arduino source code implementation file managing sensor peripherals, I2C, SPI, and SD card logging."
        question = "How are sensor peripherals, memory modules, and displays initialized in microcontroller firmware?"
        method = ["embedded C++ programming", "sensor bus initialization"]
        inputs = ["microcontroller onboard sensors"]
        outputs = [base]
        rel = 'background'
    else:
        kind = 'report'
        what_it_is = f"Research document {base}."
        question = f"What findings are recorded in {base}?"
        method = ["reading document"]
        inputs = ["research workspace"]
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

print(f"Batch 06: {len(records)} audited, {len(skipped)} skipped, Total: {len(records) + len(skipped)}")
assert len(records) + len(skipped) == 150

out_jsonl = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/records_G1_paper2_core_part06.jsonl'
out_skipped = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_G1_paper2_core_part06.csv'

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
