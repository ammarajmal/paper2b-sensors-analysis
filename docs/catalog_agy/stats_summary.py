import os
import json
from collections import Counter

OUT_DIR = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy"
INDEX_FILE = os.path.join(OUT_DIR, "file_index.json")

with open(INDEX_FILE, "r") as f:
    idx_data = json.load(f)

all_files = idx_data["files"]
stats = idx_data["stats"]

# Count catalogued per tree
cat_counts = Counter()
for t in range(1, 15):
    jp = os.path.join(OUT_DIR, f"catalog_{t}.jsonl")
    if os.path.exists(jp):
        with open(jp, "r", encoding="utf-8") as f:
            for l in f:
                if l.strip():
                    cat_counts[t] += 1

# Files in index per tree
index_counts = Counter(x["tree"] for x in all_files)

print("=== FINAL RECAP PER TREE ===")
total_cat = 0
total_skipped = 0
for t in range(1, 15):
    cat = cat_counts[t]
    total_cat += cat
    t_stat = stats[str(t)]
    ext_skipped = sum(t_stat["ext"].values())
    sz_skipped = t_stat["size"]
    unreadable = len(t_stat["unreadable"])
    dup_skipped = index_counts[t] - cat
    total_tree_skipped = ext_skipped + sz_skipped + unreadable + dup_skipped
    total_skipped += total_tree_skipped
    print(f"Tree {t:2d}: Catalogued = {cat:4d} | Skipped = {total_tree_skipped:6d} (Duplicates: {dup_skipped:4d}, Disallowed Ext: {ext_skipped:5d}, Size > limit: {sz_skipped:2d}, Unreadable: {unreadable:2d})")

print(f"\nTOTAL Catalogued: {total_cat}")
print(f"TOTAL Skipped: {total_skipped}")

print("\nFiles that could not be read:")
for t in range(1, 15):
    t_stat = stats[str(t)]
    for f, reason in t_stat["unreadable"]:
        print(f"  Tree {t}: {f} ({reason})")
