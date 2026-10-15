import json

with open("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/file_index.json") as f:
    data = json.load(f)

files = data["files"]
hash_to_files = {}
for f in files:
    h = f["hash"]
    if h not in hash_to_files:
        hash_to_files[h] = []
    hash_to_files[h].append(f)

t13_files = [f for f in files if f["tree"] == 13]
print(f"Tree 13 total files in index: {len(t13_files)}")
for f in t13_files:
    matches = hash_to_files[f["hash"]]
    other_trees = [m for m in matches if m["tree"] != 13]
    print(f"Tree 13: {f['rel_path']}")
    for m in other_trees:
        print(f"   -> matches Tree {m['tree']}: {m['rel_path']}")
