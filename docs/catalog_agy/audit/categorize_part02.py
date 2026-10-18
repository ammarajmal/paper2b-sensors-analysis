import csv
import os
import hashlib
import json

audit_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit"

# Load seen hashes from G1
g1_records = [
    "records_G1_paper2_core_part01.jsonl",
    "records_G1_paper2_core_part02.jsonl",
    "records_G1_paper2_core_part03.jsonl"
]
seen_hashes = {}
for g1 in g1_records:
    p = os.path.join(audit_dir, g1)
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                rec = json.loads(line)
                path = rec["path"]
                if os.path.exists(path) and os.path.isfile(path):
                    with open(path, "rb") as fp:
                        h = hashlib.sha256(fp.read()).hexdigest()
                    if h not in seen_hashes:
                        seen_hashes[h] = path

# Add part01 files to seen_hashes
p1 = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G2_other_paper2_related_part01.csv"
with open(p1) as f:
    for r in csv.DictReader(f):
        path = r["path"]
        if os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) > 0:
            with open(path, "rb") as fp:
                h = hashlib.sha256(fp.read()).hexdigest()
            if h not in seen_hashes:
                seen_hashes[h] = path

p2 = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G2_other_paper2_related_part02.csv"
with open(p2) as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in G2 part02: {len(rows)}")
for i, r in enumerate(rows):
    path = r["path"]
    sz = os.path.getsize(path) if os.path.exists(path) else -1
    dup = ""
    if os.path.exists(path) and os.path.isfile(path) and sz > 0:
        with open(path, "rb") as fp:
            h = hashlib.sha256(fp.read()).hexdigest()
        if h in seen_hashes:
            dup = f"DUP of {seen_hashes[h]}"
        else:
            seen_hashes[h] = path
    print(f"{i+1:3d} | sz={sz:6d} | {dup[:35]:35s} | {path}")
