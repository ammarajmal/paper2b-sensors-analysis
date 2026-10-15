import os

BASE_DIR = "/mnt/phd_data/phd_master"

def check_dirs(tree_rel):
    full = os.path.join(BASE_DIR, tree_rel)
    if not os.path.exists(full):
        print(f"MISSING: {full}")
        return
    print(f"=== {tree_rel} ===")
    entries = sorted(os.listdir(full))
    for e in entries:
        p = os.path.join(full, e)
        is_d = os.path.isdir(p)
        print(f"  {'[DIR]' if is_d else '[FILE]'} {e}")

check_dirs("02_research_projects/p04_offline_pose_reconstruction")
check_dirs("98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin")
check_dirs("04_code_software/github/shm-displacement-project")
check_dirs("02_research_projects/P00_shm-displacement-project")
check_dirs("02_research_projects/P00_shm-displacement-project/context_data/TESolution")
check_dirs("05_publications/p02_sensors_windtunnel")
