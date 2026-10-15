import json

with open("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/file_index.json") as f:
    data = json.load(f)

files = data["files"]
empty_files = [f for f in files if f["size"] == 0]
print(f"Total 0-byte files: {len(empty_files)}")
by_ext = {}
for f in empty_files:
    by_ext[f["ext"]] = by_ext.get(f["ext"], 0) + 1
print("By extension:", by_ext)
