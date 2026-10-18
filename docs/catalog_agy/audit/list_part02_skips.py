import csv

with open("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/skipped_G2_other_paper2_related_part02.csv") as f:
    for i, r in enumerate(csv.DictReader(f)):
        print(f"{i+1:2d}: {r['reason'][:35]:35s} | {r['path']}")
