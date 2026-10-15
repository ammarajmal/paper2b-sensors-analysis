import os
import fnmatch

BASE_DIR = "/mnt/phd_data/phd_master"

ALWAYS_SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "node_modules", "build", "devel", "install", "site-packages"
}

def is_always_skip_dir(name):
    if name in ALWAYS_SKIP_DIRS:
        return True
    if name.startswith("venv"):
        return True
    return False

ALLOWED_EXTENSIONS = {
    ".py", ".m", ".sh", ".cpp", ".h", ".launch", ".ipynb", ".md", ".txt", ".yaml", ".yml", ".toml", ".json"
}

tree_configs = {
    1: {
        "path": "02_research_projects/p02_ros_multicamera_shm/structural_vision_research",
        "custom_skip": lambda root, dirs, files: False,
    },
    2: {
        "path": "02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis",
        "custom_skip": lambda root, dirs, files: False,
    },
    3: {
        "path": "02_research_projects/p04_offline_pose_reconstruction",
        "custom_skip": lambda root, dirs, files: False,
    },
    4: {
        "path": "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin",
        "custom_skip": lambda root, dirs, files: False,
    },
    5: {
        "path": "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_manuscript",
        "custom_skip": lambda root, dirs, files: False,
    },
    6: {
        "path": "04_code_software/github/shm-displacement-project",
        "custom_skip": lambda root, dirs, files: False,
    },
    7: {
        "path": "02_research_projects/P00_shm-displacement-project",
        "custom_skip": lambda root, dirs, files: False,
    },
    8: {
        "path": "02_research_projects/p03_windtunnel_bridgedeck",
        "custom_skip": lambda root, dirs, files: False,
    },
    9: {
        "path": "98_legacy_imports/old_ros_workspaces_2025/tesol_ws",
        "custom_skip": lambda root, dirs, files: False,
    },
    10: {
        "path": "02_research_projects/P00_shm-displacement-project/context_data/TESolution",
        "custom_skip": lambda root, dirs, files: False,
    },
    11: {
        "path": "98_legacy_imports/space_adev_oct2026_analyses/paper2-acquisition-methods-research",
        "custom_skip": lambda root, dirs, files: False,
    },
    12: {
        "path": "98_legacy_imports/space_adev_oct2026_analyses/phd-research-advisory",
        "custom_skip": lambda root, dirs, files: False,
    },
    13: {
        "path": "05_publications/p02_sensors_windtunnel",
        "custom_skip": lambda root, dirs, files: False,
    },
    14: {
        "path": "04_code_software/legacy",
        "custom_skip": lambda root, dirs, files: False,
    },
}

def scan_tree(tree_id):
    cfg = tree_configs[tree_id]
    tree_root = os.path.join(BASE_DIR, cfg["path"])
    
    files_to_read = []
    skipped_ext = {}
    skipped_size = []
    skipped_dir = []
    
    for root, dirs, files in os.walk(tree_root):
        rel_root = os.path.relpath(root, tree_root)
        
        # Directory filters
        to_remove = []
        for d in dirs:
            rel_d = os.path.normpath(os.path.join(rel_root, d)) if rel_root != "." else d
            # Always skip
            if is_always_skip_dir(d):
                to_remove.append(d)
                skipped_dir.append((rel_d, "always_skip_dir"))
                continue
            
            # Tree-specific skip rules
            if tree_id == 2:
                # skip .claude/worktrees, outputs/*/scripts_used, graphify-out
                if d == "graphify-out":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree2_graphify-out"))
                    continue
                if rel_d == ".claude/worktrees" or rel_d.startswith(".claude/worktrees/"):
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree2_claude_worktrees"))
                    continue
                if d == "worktrees" and os.path.basename(rel_root) == ".claude":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree2_claude_worktrees"))
                    continue
                if d == "scripts_used" and "outputs" in rel_root.split(os.sep):
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree2_scripts_used"))
                    continue
            elif tree_id == 3:
                # skip omrpr_analysis
                if d == "omrpr_analysis":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree3_omrpr_analysis"))
                    continue
            elif tree_id == 4:
                # (src, docs, config; skip results*, data)
                if d.startswith("results") or d == "data":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree4_results_or_data"))
                    continue
            elif tree_id == 6:
                # (scripts, paper2, offline_processing, docs, memory; skip data, archive, context_data, ros_ws)
                if d in ("data", "archive", "context_data", "ros_ws"):
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree6_data_archive_context_ros_ws"))
                    continue
            elif tree_id == 7:
                # (same content as 6 in part: record only files NOT identical to tree 6; skip data, ros_ws, venv310)
                if d in ("data", "ros_ws", "venv310"):
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree7_data_ros_ws_venv310"))
                    continue
            elif tree_id == 8:
                # skip data
                if d == "data":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree8_data"))
                    continue
            elif tree_id == 10:
                # skip tesol_ws
                if d == "tesol_ws":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree10_tesol_ws"))
                    continue
            elif tree_id == 11:
                # skip env, outputs
                if d in ("env", "outputs"):
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree11_env_outputs"))
                    continue
            elif tree_id == 12:
                # skip 03_PACKAGES
                if d == "03_PACKAGES":
                    to_remove.append(d)
                    skipped_dir.append((rel_d, "tree12_03_PACKAGES"))
                    continue
                    
        for d in to_remove:
            dirs.remove(d)
            
        # File checks
        for f in files:
            file_path = os.path.join(root, f)
            rel_file = os.path.normpath(os.path.join(rel_root, f)) if rel_root != "." else f
            
            # Check Tree 13: scripts and docs only
            if tree_id == 13:
                # Let's inspect what top-level dirs exist in tree 13
                pass

            _, ext = os.path.splitext(f)
            ext = ext.lower()
            
            if ext not in ALLOWED_EXTENSIONS:
                skipped_ext[ext] = skipped_ext.get(ext, 0) + 1
                continue
                
            try:
                sz = os.path.getsize(file_path)
            except Exception as e:
                skipped_size.append((rel_file, f"error: {e}"))
                continue
                
            if ext == ".json" and sz > 200 * 1024:
                skipped_size.append((rel_file, f"json > 200KB ({sz} bytes)"))
                continue
            if sz > 400 * 1024:
                skipped_size.append((rel_file, f"file > 400KB ({sz} bytes)"))
                continue
                
            files_to_read.append((rel_file, sz, ext))
            
    return files_to_read, skipped_ext, skipped_size, skipped_dir

for t in range(1, 15):
    f_read, s_ext, s_sz, s_dir = scan_tree(t)
    print(f"Tree {t:2d}: to_read={len(f_read):4d} | skipped_ext={sum(s_ext.values()):4d} | skipped_sz={len(s_sz):3d} | skipped_dir_prunes={len(s_dir):3d}")
