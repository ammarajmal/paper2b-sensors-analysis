import os
import hashlib
import json
import time

BASE_DIR = "/mnt/phd_data/phd_master"

ALWAYS_SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "node_modules", "build", "devel", "install", "site-packages"
}

ALLOWED_EXTENSIONS = {
    ".py", ".m", ".sh", ".cpp", ".h", ".launch", ".ipynb", ".md", ".txt", ".yaml", ".yml", ".toml", ".json"
}

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

def get_hash(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def scan_all_trees():
    start_time = time.time()
    all_files = [] # list of dicts: {tree, rel_path, full_path, size, hash, ext}
    skipped_stats = {} # per tree: {ext: count, size: count, dir: count, unreadable: []}
    
    for t_num, t_rel in trees:
        t_root = os.path.join(BASE_DIR, t_rel)
        t_stats = {"ext": {}, "size": 0, "unreadable": [], "dirs_pruned": 0}
        skipped_stats[t_num] = t_stats
        
        for root, dirs, files in os.walk(t_root):
            rel_root = os.path.relpath(root, t_root)
            
            # Directory pruning
            to_remove = []
            for d in dirs:
                rel_d = os.path.normpath(os.path.join(rel_root, d)) if rel_root != "." else d
                # Always skip
                if d in ALWAYS_SKIP_DIRS or d.startswith("venv"):
                    to_remove.append(d)
                    t_stats["dirs_pruned"] += 1
                    continue
                    
                # Tree-specific skip rules
                if t_num == 2:
                    if d == "graphify-out" or rel_d == ".claude/worktrees" or rel_d.startswith(".claude/worktrees/"):
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                    if d == "worktrees" and os.path.basename(rel_root) == ".claude":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                    if d == "scripts_used" and "outputs" in rel_root.split(os.sep):
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 3:
                    if d == "omrpr_analysis":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 4:
                    if d.startswith("results") or d == "data":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 6:
                    if d in ("data", "archive", "context_data", "ros_ws"):
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 7:
                    if d in ("data", "ros_ws", "venv310", "TESolution"):
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 8:
                    if d == "data":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 9:
                    if d == "apriltag-imgs":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 10:
                    if d == "tesol_ws":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 11:
                    if d in ("env", "outputs"):
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 12:
                    if d == "03_PACKAGES":
                        to_remove.append(d)
                        t_stats["dirs_pruned"] += 1
                        continue
                elif t_num == 13:
                    # Tree 13: scripts and docs only
                    if rel_root == ".":
                        if d not in ("scripts", "docs"):
                            to_remove.append(d)
                            t_stats["dirs_pruned"] += 1
                            continue
                            
            for d in to_remove:
                dirs.remove(d)
                
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                rel_f = os.path.normpath(os.path.join(rel_root, f)) if rel_root != "." else f
                
                # Check Tree 13 root files: if in root, allowed docs only or skip?
                # User prompt: "05_publications/p02_sensors_windtunnel (scripts and docs only)"
                # Let's allow root markdown/doc files (README.md, etc.) or check
                if t_num == 13 and rel_root == ".":
                    if ext not in {".md", ".txt"}:
                        t_stats["ext"][ext] = t_stats["ext"].get(ext, 0) + 1
                        continue

                if ext not in ALLOWED_EXTENSIONS:
                    t_stats["ext"][ext] = t_stats["ext"].get(ext, 0) + 1
                    continue
                    
                fp = os.path.join(root, f)
                try:
                    if os.path.islink(fp) and not os.path.exists(fp):
                        t_stats["unreadable"].append((rel_f, "broken symlink"))
                        continue
                    sz = os.path.getsize(fp)
                except Exception as e:
                    t_stats["unreadable"].append((rel_f, str(e)))
                    continue
                    
                if ext == ".json" and sz > 200 * 1024:
                    t_stats["size"] += 1
                    continue
                if sz > 400 * 1024:
                    t_stats["size"] += 1
                    continue
                    
                try:
                    h = get_hash(fp)
                except Exception as e:
                    t_stats["unreadable"].append((rel_f, f"hash error: {e}"))
                    continue
                    
                all_files.append({
                    "tree": t_num,
                    "tree_rel": t_rel,
                    "rel_path": rel_f,
                    "full_path": fp,
                    "size": sz,
                    "hash": h,
                    "ext": ext
                })
                
    elapsed = time.time() - start_time
    print(f"Scan completed in {elapsed:.2f}s. Total readable files found: {len(all_files)}")
    return all_files, skipped_stats

if __name__ == "__main__":
    files, stats = scan_all_trees()
    out_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy"
    with open(os.path.join(out_dir, "file_index.json"), "w") as f:
        json.dump({"files": files, "stats": stats}, f, indent=2)
    print("Saved file_index.json")
    
    # Print summary per tree
    from collections import Counter
    tree_counts = Counter(x["tree"] for x in files)
    for t in range(1, 15):
        print(f"Tree {t:2d}: {tree_counts[t]:4d} files | skipped_ext: {sum(stats[t]['ext'].values()):5d} | skipped_size: {stats[t]['size']:3d} | unreadable: {len(stats[t]['unreadable']):2d}")
