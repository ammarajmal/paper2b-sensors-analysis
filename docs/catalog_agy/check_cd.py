import os

BASE_DIR = "/mnt/phd_data/phd_master"
cd_dir = os.path.join(BASE_DIR, "02_research_projects/P00_shm-displacement-project/context_data")
print("Entries in context_data:")
for e in os.listdir(cd_dir):
    print("  ", e)
