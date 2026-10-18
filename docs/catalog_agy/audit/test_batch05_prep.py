import sys, os, csv, json
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

csv_path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G1_paper2_core_part05.csv'
with open(csv_path) as f:
    batch_rows = list(csv.DictReader(f))

print(f"Loaded {len(batch_rows)} rows from batch part05")
