import csv
import os
import hashlib

audit_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit"
batch_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches"

for b in ["G2_other_paper2_related_part01.csv", "G2_other_paper2_related_part02.csv", "G2_other_paper2_related_part03.csv"]:
    p = os.path.join(batch_dir, b)
    with open(p) as f:
        rows = list(csv.DictReader(f))
    print(f"=== {b} ({len(rows)} rows) ===")
    for i, r in enumerate(rows):
        path = r["path"]
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else -1
        if i < 35 or i >= len(rows) - 5:
            print(f"{i+1:3d}: exists={exists} size={size:8d} {path}")
