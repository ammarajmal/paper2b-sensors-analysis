import os
import hashlib

t1 = "/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research"

def get_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

main_hashes = {}
for root, dirs, files in os.walk(t1):
    if ".git" in dirs: dirs.remove(".git")
    if ".claude" in dirs: dirs.remove(".claude")
    for f in files:
        fp = os.path.join(root, f)
        if os.path.isfile(fp):
            try:
                main_hashes[get_hash(fp)] = os.path.relpath(fp, t1)
            except:
                pass

wt = os.path.join(t1, ".claude/worktrees")
if os.path.exists(wt):
    for root, dirs, files in os.walk(wt):
        if ".git" in dirs: dirs.remove(".git")
        for f in files:
            fp = os.path.join(root, f)
            if os.path.isfile(fp):
                try:
                    h = get_hash(fp)
                    if h in main_hashes:
                        pass
                    else:
                        print("Unique in .claude/worktrees:", os.path.relpath(fp, t1))
                except:
                    pass
