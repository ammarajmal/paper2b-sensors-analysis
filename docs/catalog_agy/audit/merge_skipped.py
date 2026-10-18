import os, glob, csv

audit_dir = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit'
skipped_files = sorted(glob.glob(os.path.join(audit_dir, 'skipped_*.csv')))
master_skipped = os.path.join(audit_dir, 'SKIPPED.csv')

seen = {}
# First read master_skipped if it exists
if os.path.exists(master_skipped):
    with open(master_skipped, 'r') as f:
        for r in csv.DictReader(f):
            seen[r['path']] = r['reason']

for sf in skipped_files:
    with open(sf, 'r') as f:
        for r in csv.DictReader(f):
            seen[r['path']] = r['reason']

with open(master_skipped, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['path', 'reason'])
    for p, r in sorted(seen.items()):
        writer.writerow([p, r])

print(f"Total unique skipped files merged into SKIPPED.csv: {len(seen)}")
