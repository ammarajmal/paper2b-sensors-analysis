import json
import re

with open("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/file_index.json") as f:
    data = json.load(f)

# Let's check occurrences of vendor / facility names in tree 10 or tree 1
t10_files = [f for f in data["files"] if f["tree"] == 10]
for f in t10_files:
    print(f["rel_path"])
