import os

BASE_DIR = "/mnt/phd_data/phd_master"

t10 = os.path.join(BASE_DIR, "02_research_projects/P00_shm-displacement-project/context_data/TESolution")
for root, dirs, files in os.walk(t10):
    rel = os.path.relpath(root, t10)
    print(f"Dir: {rel} -> {len(files)} files, {len(dirs)} dirs")
    for f in files[:5]:
        print(f"   {f}")
