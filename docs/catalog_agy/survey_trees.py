import os
import sys

BASE_DIR = "/mnt/phd_data/phd_master"

trees = [
    (1, "02_research_projects/p02_ros_multicamera_shm/structural_vision_research"),
    (2, "02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis"),
    (3, "02_research_projects/p04_offline_pose_reconstruction"),
    (4, "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin"),
    (5, "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_manuscript"),
    (6, "04_code_software/github/shm-displacement-project"),
    (7, "02_research_projects/P00_shm-displacement-project"),
    (8, "02_research_projects/p03_windtunnel_bridgedeck"),
    (9, "98_legacy_imports/old_ros_workspaces_2025/tesol_ws"),
    (10, "02_research_projects/P00_shm-displacement-project/context_data/TESolution"),
    (11, "98_legacy_imports/space_adev_oct2026_analyses/paper2-acquisition-methods-research"),
    (12, "98_legacy_imports/space_adev_oct2026_analyses/phd-research-advisory"),
    (13, "05_publications/p02_sensors_windtunnel"),
    (14, "04_code_software/legacy"),
]

for idx, rel_path in trees:
    full_path = os.path.join(BASE_DIR, rel_path)
    exists = os.path.exists(full_path)
    print(f"Tree {idx:2d}: exists={exists} | {full_path}")
