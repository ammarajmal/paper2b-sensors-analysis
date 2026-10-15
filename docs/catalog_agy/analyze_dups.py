import json
from collections import defaultdict

with open("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/file_index.json") as f:
    data = json.load(f)

files = data["files"]
hash_map = defaultdict(list)

for item in files:
    hash_map[item["hash"]].append(item)

print(f"Total files: {len(files)}")
print(f"Total unique hashes: {len(hash_map)}")

dup_hashes = {h: items for h, items in hash_map.items() if len(items) > 1}
print(f"Hashes appearing > 1 time: {len(dup_hashes)}")

# Check duplicate occurrences across trees vs within same tree
cross_tree_dups = 0
within_tree_dups = 0
for h, items in dup_hashes.items():
    trees = set(x["tree"] for x in items)
    if len(trees) > 1:
        cross_tree_dups += 1
    else:
        within_tree_dups += 1

print(f"Hashes appearing in multiple trees: {cross_tree_dups}")
print(f"Hashes appearing multiple times within the same tree: {within_tree_dups}")

# If we only catalogue the first occurrence of each identical file:
first_seen_tree = {}
tree_catalog_counts = defaultdict(int)
tree_skipped_dup_counts = defaultdict(int)

seen_hashes = {} # hash -> item

for item in files:
    h = item["hash"]
    t = item["tree"]
    if h not in seen_hashes:
        seen_hashes[h] = item
        tree_catalog_counts[t] += 1
    else:
        tree_skipped_dup_counts[t] += 1

print("\nFiles catalogued per tree if cataloguing first occurrence:")
for t in range(1, 15):
    print(f"Tree {t:2d}: to catalogue = {tree_catalog_counts[t]:4d} | identical skipped = {tree_skipped_dup_counts[t]:4d} | total in tree = {tree_catalog_counts[t] + tree_skipped_dup_counts[t]:4d}")
