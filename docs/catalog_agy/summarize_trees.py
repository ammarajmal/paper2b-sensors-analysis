import os

BASE_DIR = "/mnt/phd_data/phd_master"

def summarize_tree(tree_id, rel_path, skip_dirs=set(), only_dirs=None):
    root_dir = os.path.join(BASE_DIR, rel_path)
    entries = sorted(os.listdir(root_dir))
    print(f"=== Tree {tree_id}: {rel_path} ===")
    top_dirs = [e for e in entries if os.path.isdir(os.path.join(root_dir, e))]
    top_files = [e for e in entries if not os.path.isdir(os.path.join(root_dir, e))]
    print(f"  Top dirs: {top_dirs}")
    print(f"  Top files: {top_files[:10]} (total {len(top_files)})")

summarize_tree(1, "02_research_projects/p02_ros_multicamera_shm/structural_vision_research")
summarize_tree(2, "02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis")
summarize_tree(3, "02_research_projects/p04_offline_pose_reconstruction")
summarize_tree(8, "02_research_projects/p03_windtunnel_bridgedeck")
summarize_tree(9, "98_legacy_imports/old_ros_workspaces_2025/tesol_ws")
summarize_tree(11, "98_legacy_imports/space_adev_oct2026_analyses/paper2-acquisition-methods-research")
summarize_tree(12, "98_legacy_imports/space_adev_oct2026_analyses/phd-research-advisory")
summarize_tree(14, "04_code_software/legacy")
