import os
from collections import Counter

BASE_DIR = "/mnt/phd_data/phd_master"
t1 = os.path.join(BASE_DIR, "02_research_projects/p02_ros_multicamera_shm/structural_vision_research")

files_by_folder = Counter()
exts = Counter()

for root, dirs, files in os.walk(t1):
    if ".git" in dirs: dirs.remove(".git")
    rel_root = os.path.relpath(root, t1)
    top_folder = rel_root.split(os.sep)[0] if rel_root != "." else "."
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        exts[ext] += 1
        if ext in {".py", ".m", ".sh", ".cpp", ".h", ".launch", ".ipynb", ".md", ".txt", ".yaml", ".yml", ".toml", ".json"}:
            files_by_folder[top_folder] += 1

print("Tree 1 folders (readable files):")
for fld, c in sorted(files_by_folder.items(), key=lambda x: -x[1]):
    print(f"  {fld:30s}: {c}")

print("\nExtensions:")
for ext, c in sorted(exts.items(), key=lambda x: -x[1]):
    print(f"  {ext:10s}: {c}")
