import os

BASE_DIR = "/mnt/phd_data/phd_master"

cd = os.path.join(BASE_DIR, "02_research_projects/P00_shm-displacement-project/context_data")
for sub in ["papers", "literature review"]:
    p = os.path.join(cd, sub)
    if os.path.exists(p):
        for root, dirs, files in os.walk(p):
            print(f"{os.path.relpath(root, cd)}: {len(files)} files")
            for f in files[:3]:
                print(f"   {f}")
