import json

with open("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/file_index.json") as f:
    data = json.load(f)

for t, stats in data["stats"].items():
    if stats["unreadable"]:
        print(f"Tree {t} unreadable:", stats["unreadable"])
