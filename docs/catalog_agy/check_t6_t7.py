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

def scan_files(root_dir, skip_dirs_set):
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
            sz = os.path.getsize(fp)
            if ext == ".json" and sz > 200 * 1024:
                continue
            if sz > 400 * 1024:
                continue
            rel_f = os.path.normpath(os.path.join(rel_r, f)) if rel_r != "." else f
            res[rel_f] = (fp, sz, get_hash(fp))
    return res

t6_dir = os.path.join(BASE_DIR, "04_code_software/github/shm-displacement-project")
t7_dir = os.path.join(BASE_DIR, "02_research_projects/P00_shm-displacement-project")

t6_files = scan_files(t6_dir, {"data", "archive", "context_data", "ros_ws"})
t7_files = scan_files(t7_dir, {"data", "ros_ws", "venv310"})

print(f"Tree 6 valid files: {len(t6_files)}")
print(f"Tree 7 valid files: {len(t7_files)}")

identical_count = 0
diff_content_count = 0
only_in_7 = 0

for rel_f, (fp, sz, h) in t7_files.items():
    if rel_f in t6_files:
        if t6_files[rel_f][2] == h:
            identical_count += 1
        else:
            diff_content_count += 1
            print(f"Different content at same path: {rel_f}")
    else:
        only_in_7 += 1

print(f"Tree 7 identical to Tree 6 at same path: {identical_count}")
print(f"Tree 7 different content at same path: {diff_content_count}")
print(f"Tree 7 path not in Tree 6: {only_in_7}")
