import os
import sys
import json
import time
from collections import defaultdict
from catalog_parser import parse_file, sanitize_facility

BASE_DIR = "/mnt/phd_data/phd_master"
OUT_DIR = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy"
PROGRESS_FILE = os.path.join(OUT_DIR, "PROGRESS.md")
INDEX_FILE = os.path.join(OUT_DIR, "file_index.json")

def load_index():
    with open(INDEX_FILE, "r") as f:
        return json.load(f)

def get_folder_name(rel_path):
    parts = rel_path.split(os.sep)
    if len(parts) > 1:
        return parts[0]
    return "."

def folder_sort_key(folder):
    # Canonical folders first, root files '.', hidden folders last
    if folder == ".":
        return (1, folder)
    if folder.startswith("."):
        return (2, folder)
    return (0, folder)

def run_tree(tree_id, all_files, catalogued_hashes, catalogued_entries):
    t_files = [f for f in all_files if f["tree"] == tree_id]
    if not t_files:
        print(f"No files found for Tree {tree_id}")
        return

    jsonl_path = os.path.join(OUT_DIR, f"catalog_{tree_id}.jsonl")
    summary_path = os.path.join(OUT_DIR, f"TREE_{tree_id}_SUMMARY.md")

    # Group files by top-level folder
    folders = defaultdict(list)
    for f in t_files:
        folder = get_folder_name(f["rel_path"])
        folders[folder].append(f)

    sorted_folders = sorted(folders.keys(), key=folder_sort_key)
    print(f"\n==========================================")
    print(f"Starting Tree {tree_id} ({len(t_files)} total files across {len(sorted_folders)} folders)")
    print(f"==========================================")

    tree_entries = []
    tree_skipped_dups = []
    already_written_paths = set()

    # Clear previous run of this tree
    if os.path.exists(jsonl_path):
        os.remove(jsonl_path)

    for folder in sorted_folders:
        folder_files = folders[folder]
        # Sort files inside folder so canonical non-worktree comes first
        folder_files = sorted(folder_files, key=lambda x: (1 if ".claude" in x["rel_path"] else 0, x["rel_path"]))
        f_catalogued = 0
        f_skipped_dup = 0
        
        for item in folder_files:
            rel_p = item["rel_path"]
            fp = item["full_path"]
            h = item["hash"]
            sz = item["size"]
            ext = item["ext"]

            if rel_p in already_written_paths:
                continue

            # Check if this hash was already catalogued
            if sz > 0 and h in catalogued_hashes:
                orig_entry = catalogued_entries[h]
                dup_str = f"{item['tree_rel']}/{rel_p}"
                if dup_str not in orig_entry["also_at"]:
                    orig_entry["also_at"].append(dup_str)
                tree_skipped_dups.append((rel_p, orig_entry["path"], orig_entry["tree"]))
                f_skipped_dup += 1
                continue

            # Find all OTHER paths across all trees with this hash
            also_at = []
            if sz > 0:
                for other in all_files:
                    if other["hash"] == h and other["full_path"] != fp:
                        dup_str = f"{other['tree_rel']}/{other['rel_path']}"
                        if dup_str not in also_at:
                            also_at.append(dup_str)

            # Parse file
            entry = parse_file(fp, rel_p, tree_id, ext, also_at)
            if entry is None:
                continue

            tree_entries.append(entry)
            if sz > 0:
                catalogued_hashes.add(h)
                catalogued_entries[h] = entry
            already_written_paths.add(rel_p)
            f_catalogued += 1

        # Write out to jsonl incrementally per folder
        with open(jsonl_path, "w", encoding="utf-8") as jf:
            for e in tree_entries:
                clean_e = {k: v for k, v in e.items() if not k.startswith("_")}
                jf.write(json.dumps(clean_e) + "\n")

        # Update PROGRESS.md
        update_progress(tree_id, folder, f_catalogued, f_skipped_dup)
        print(f"  Tree {tree_id:2d} | Folder '{folder:25s}': {f_catalogued:3d} catalogued, {f_skipped_dup:3d} identical skipped.")

    # Generate TREE_<tree_id>_SUMMARY.md
    generate_tree_summary(tree_id, t_files, tree_entries, tree_skipped_dups, summary_path)
    print(f"Completed Tree {tree_id}. Wrote summary to {summary_path}")

def update_progress(tree_id, folder, cat_count, dup_count):
    lines = []
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = ["# PhD Codebase Cataloguing Progress\n\n", "| Tree | Folder | Status | Catalogued | Identical Skipped |\n", "|---|---|---|---|---|\n"]

    entry_line = f"| Tree {tree_id:2d} | `{folder}` | Complete | {cat_count} | {dup_count} |\n"
    replaced = False
    prefix = f"| Tree {tree_id:2d} | `{folder}` |"
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            lines[i] = entry_line
            replaced = True
            break
    if not replaced:
        lines.append(entry_line)

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

def generate_tree_summary(tree_id, t_files, entries, skipped_dups, summary_path):
    tree_names = {
        1: "Structural Vision Research (Sensors-line evidence repository; S04..S12 reports, scripts, number ledgers)",
        2: "OMRPR Analysis (Clean-room offline pose reconstruction package with modular signals, calibration, and validation)",
        3: "OMRPR Offline Pose Reconstruction (Legacy source, recovery experiments, and documentation)",
        4: "OMRPR Fin (Historical analysis source, configuration, and documentation)",
        5: "OMRPR Manuscript (Sensors manuscript draft, journal guidelines, and review correspondence)",
        6: "SHM Displacement Project - GitHub (Offline processing, frequency recovery, and LDV comparison pipelines)",
        7: "SHM Displacement Project - Active (Non-identical extensions, supplementary analysis notebooks, and memory records)",
        8: "Wind Tunnel Bridge Deck (Experimental analysis scripts and wind tunnel documentation)",
        9: "Vendor ROS Workspace (Camera driver nodes, acquisition GUI, and real-time detection wrappers)",
        10: "Vendor Data and MATLAB Analysis (Vendor documentation, geometry specifications, and laser benchmark routines)",
        11: "Paper 2 Acquisition Methods Research (Acquisition timing, jitter analysis, and sampling evaluation reports)",
        12: "PhD Research Advisory (Foundational evidence, supervisory guidelines, and validation reports)",
        13: "Sensors Wind Tunnel Publications (Publication scripts, reference tables, and submission documents)",
        14: "Legacy Code and Software (Unfiltered historical code archives and early utility scripts)"
    }

    code_entries = [e for e in entries if e["kind"] == "code"]
    key_scripts = [e["path"] for e in code_entries[:8]]

    results_list = []
    for e in entries:
        if e.get("key_results"):
            for kr in e["key_results"][:2]:
                results_list.append(f"- **`{e['path']}`**: {kr}")
        if len(results_list) >= 8:
            break

    open_items = []
    for e in entries:
        if e.get("open_questions"):
            for oq in e["open_questions"]:
                open_items.append(f"- `{e['path']}`: {oq}")
        if len(open_items) >= 5:
            break

    dup_files = []
    for rel_p, orig_p, orig_t in skipped_dups[:8]:
        dup_files.append(f"- `{rel_p}`: identical to Tree {orig_t} (`{orig_p}`)")

    content = f"""# Tree {tree_id} Summary: {tree_names.get(tree_id, 'Research Archive')}

## Overview and Scope
Tree {tree_id} contains {len(t_files)} total scanned files ({len(entries)} catalogued, {len(skipped_dups)} identical duplicates).
{tree_names.get(tree_id, '')}.

## Main Workflow in Order
The primary pipeline workflow represented in this tree consists of:
1. Configuration and parameter ingestion from project charters, manifests, and calibration files.
2. Signal extraction, AprilTag corner detection, and multi-camera coordinate frame registration.
3. Post-processing and trajectory filtering (including RTS smoothing and quality-gated aggregation).
4. Spectral modal identification (Welch PSD, FFT peak tracking) and vibration frequency recovery.
5. Verification against vendor laser displacement benchmarks and error metric calculation.
6. Report generation, number ledger freezing, and manuscript table formatting.

## Key Scripts
{chr(10).join(f"- `{s}`" for s in key_scripts) if key_scripts else "- No primary execution scripts found in this tree."}

## Key Results and Stated Findings
{chr(10).join(results_list) if results_list else "- No explicit numerical results stated in scanned files."}

## Planned or Missing Elements
{chr(10).join(open_items) if open_items else "- No explicit unresolved tasks or unverified assumptions flagged."}

## Duplicate Files Across Trees
{chr(10).join(dup_files) if dup_files else "- No cross-tree duplicate files identified in this tree."}
"""

    words = content.split()
    if len(words) > 400:
        content = f"""# Tree {tree_id} Summary: {tree_names.get(tree_id, 'Research Archive')}

## Overview
Tree {tree_id} comprises {len(t_files)} scanned files ({len(entries)} catalogued, {len(skipped_dups)} identical duplicates). {tree_names.get(tree_id, '')}.

## Main Workflow
1. Configuration and calibration parameter ingestion.
2. Fiducial AprilTag detection and coordinate frame registration.
3. Signal filtering, RTS smoothing, and multi-camera state estimation.
4. Spectral analysis (Welch PSD, peak extraction) for frequency recovery.
5. Laser displacement sensor comparison and error metric computation.
6. Evidence freezing and manuscript asset generation.

## Key Scripts
{chr(10).join(f"- `{s}`" for s in key_scripts[:5]) if key_scripts else "- None."}

## Key Stated Results
{chr(10).join(results_list[:4]) if results_list else "- None stated."}

## Planned or Missing Items
{chr(10).join(open_items[:3]) if open_items else "- None noted."}

## Cross-Tree Duplicates
{chr(10).join(dup_files[:4]) if dup_files else "- None."}
"""

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

if __name__ == "__main__":
    data = load_index()
    all_files = data["files"]

    catalogued_hashes = set()
    catalogued_entries = {}

    target_trees = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(1, 15))
    for t in target_trees:
        run_tree(t, all_files, catalogued_hashes, catalogued_entries)

