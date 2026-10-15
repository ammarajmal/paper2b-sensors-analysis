import os
import hashlib

BASE_DIR = "/mnt/phd_data/phd_master"

def get_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

ALWAYS_SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", "build", "devel", "install", "site-packages"}
def is_always_skip_dir(name):
    return name in ALWAYS_SKIP_DIRS or name.startswith("venv")

ALLOWED_EXTENSIONS = {".py", ".m", ".sh", ".cpp", ".h", ".launch", ".ipynb", ".md", ".txt", ".yaml", ".yml", ".toml", ".json"}

def scan_tree_files(root_dir, skip_dirs_set):
    res = {}
    for r, dirs, files in os.walk(root_dir):
        rel_r = os.path.relpath(r, root_dir)
        to_del = []
        for d in dirs:
            if is_always_skip_dir(d) or d in skip_dirs_set:
                to_del.append(d)
        for d in to_del:
            dirs.remove(d)
            
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                continue
            fp = os.path.join(r, f)
            try:
                if os.path.islink(fp) and not os.path.exists(fp):
                    continue
                sz = os.path.getsize(fp)
            except Exception:
                continue
            if ext == ".json" and sz > 200 * 1024:
                continue
            if sz > 400 * 1024:
                continue
            rel_f = os.path.normpath(os.path.join(rel_r, f)) if rel_r != "." else f
            try:
                h = get_hash(fp)
                res[rel_f] = (fp, sz, h)
            except Exception:
                pass
    return res

t6_dir = os.path.join(BASE_DIR, "04_code_software/github/shm-displacement-project")
t7_dir = os.path.join(BASE_DIR, "02_research_projects/P00_shm-displacement-project")

# Tree 6: scripts, paper2, offline_processing, docs, memory; skip data, archive, context_data, ros_ws
t6_files = scan_tree_files(t6_dir, {"data", "archive", "context_data", "ros_ws"})

# Tree 7: skip data, ros_ws, venv310. What if we also skip context_data/TESolution so it doesn't collide with Tree 10?
# Let's inspect both: with and without context_data
t7_files = scan_tree_files(t7_dir, {"data", "ros_ws", "venv310", "TESolution"})

print(f"Tree 6 valid files: {len(t6_files)}")
print(f"Tree 7 valid files (skipping TESolution): {len(t7_files)}")

identical = []
different = []
only_in_7 = []

for rel_f, (fp, sz, h) in t7_files.items():
    if rel_f in t6_files:
        if t6_files[rel_f][2] == h:
            identical.append(rel_f)
        else:
            different.append(rel_f)
    else:
        only_in_7.append(rel_f)

print(f"Identical at same path: {len(identical)}")
print(f"Different at same path: {len(different)}")
print(f"Only in Tree 7: {len(only_in_7)}")

print("\nDifferent files:")
for f in different:
    print("  ", f)

print("\nFiles only in Tree 7 (first 30):")
for f in only_in_7[:30]:
    print("  ", f)
