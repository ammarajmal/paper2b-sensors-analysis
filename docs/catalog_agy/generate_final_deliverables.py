import os
import re
import json
import csv
from collections import defaultdict
from catalog_parser import sanitize_facility

OUT_DIR = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy"
INDEX_FILE = os.path.join(OUT_DIR, "file_index.json")

def load_all_catalog_entries():
    all_entries = []
    for t in range(1, 15):
        jp = os.path.join(OUT_DIR, f"catalog_{t}.jsonl")
        if os.path.exists(jp):
            with open(jp, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        e = json.loads(line)
                        all_entries.append(e)
    return all_entries

def generate_catalog_csv(entries):
    csv_path = os.path.join(OUT_DIR, "catalog.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "kind", "purpose", "status", "topic", "relates_to"])
        for e in entries:
            t_num = e.get("tree", 0)
            p = f"Tree {t_num}: {e.get('path', '')}"
            kind = e.get("kind", "")
            purpose = sanitize_facility(e.get("purpose", ""))
            status = e.get("status", "")
            topics = "; ".join(e.get("topic", []))
            relates_to = e.get("relates_to", "")
            writer.writerow([p, kind, purpose, status, topics, relates_to])
    print(f"Generated catalog.csv with {len(entries)} rows.")

def get_entry_date(e):
    # Try dates in path
    path = e.get("path", "")
    m = re.search(r'(202[0-9]-[01][0-9]-[0-3][0-9])', path)
    if m:
        return m.group(1)
    # Check purpose
    m = re.search(r'(202[0-9]-[01][0-9]-[0-3][0-9])', e.get("purpose", ""))
    if m:
        return m.group(1)
    # Check key results
    for kr in e.get("key_results", []):
        m = re.search(r'(202[0-9]-[01][0-9]-[0-3][0-9])', kr)
        if m:
            return m.group(1)
    # Check evidence
    for ev in e.get("evidence", []):
        m = re.search(r'(202[0-9]-[01][0-9]-[0-3][0-9])', ev)
        if m:
            return m.group(1)
    return "Undated"

def generate_overview_md(entries):
    overview_path = os.path.join(OUT_DIR, "OVERVIEW.md")
    
    # 9 groups specified in prompt:
    # acquisition, timing, detection, calibration, pose, spectral, laser, comparison, uncertainty
    target_groups = [
        "acquisition", "timing", "detection", "calibration", "pose",
        "spectral", "laser", "comparison", "uncertainty"
    ]
    
    group_entries = defaultdict(list)
    for e in entries:
        topics = e.get("topic", [])
        for g in target_groups:
            if g in topics:
                group_entries[g].append(e)

    lines = [
        "# Research Analyses Timeline and Overview\n\n",
        "This document provides a consolidated chronological timeline of research analyses across the 14 scanned trees, organized by technical domain. Analyses are ordered by dates stated in report titles, filenames, and evidence records.\n\n",
        "> [!NOTE]\n",
        "> In accordance with project governance rules, all wind tunnel facilities and commercial partners are referenced generically as 'the facility' or 'the vendor'.\n\n"
    ]

    for g in target_groups:
        lines.append(f"## {g.capitalize()}\n\n")
        items = group_entries[g]
        if not items:
            lines.append("No specific analyses catalogued under this domain.\n\n")
            continue

        # Sort by date
        def sort_key(item):
            d = get_entry_date(item)
            return (0 if d != "Undated" else 1, d, item["tree"], item["path"])

        sorted_items = sorted(items, key=sort_key)
        
        # Deduplicate paths for readability, max 30 per domain in summary
        lines.append(f"Total analyses/files catalogued: {len(sorted_items)}\n\n")
        lines.append("| Date | Tree | File Path | Stated Result / Primary Finding |\n")
        lines.append("|---|---|---|---|\n")

        for item in sorted_items:
            d = get_entry_date(item)
            t = item["tree"]
            p = f"`{item['path']}`"
            
            # Format one-line result
            kr = item.get("key_results", [])
            if kr:
                res = sanitize_facility(kr[0].strip('"\''))
            else:
                purpose = sanitize_facility(item.get("purpose", ""))
                # trim to one concise sentence
                res = purpose.split(".")[0] if purpose else "Analysis utility / configuration routine"
                if len(res) > 90:
                    res = res[:87] + "..."
            res = res.replace("|", "\\|")
            lines.append(f"| {d} | Tree {t} | {p} | {res} |\n")
        lines.append("\n")

    with open(overview_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Generated OVERVIEW.md ({len(lines)} lines).")

def generate_duplicates_and_conflicts_md(all_files, entries):
    dup_path = os.path.join(OUT_DIR, "DUPLICATES_AND_CONFLICTS.md")
    
    # (a) Files identical across trees (by sha256)
    hash_map = defaultdict(list)
    for f in all_files:
        if f["size"] > 0:
            hash_map[f["hash"]].append(f)

    cross_tree_dups = []
    for h, flist in hash_map.items():
        trees = sorted(set(x["tree"] for x in flist))
        if len(trees) > 1:
            cross_tree_dups.append((h, trees, flist))

    # (b) Files with the same name but different content
    name_map = defaultdict(list)
    for f in all_files:
        bn = os.path.basename(f["rel_path"])
        name_map[bn].append(f)

    same_name_diff_content = []
    for bn, flist in name_map.items():
        hashes = set(x["hash"] for x in flist)
        if len(hashes) > 1 and len(flist) > 1:
            same_name_diff_content.append((bn, hashes, flist))

    lines = [
        "# Codebase Duplicates and Conflicting Evidence Register\n\n",
        "This document catalogues identical files across multiple source trees, files sharing identical names but differing in content, and substantive numerical discrepancies regarding key physical parameters.\n\n",
        "## 1. Identical Files Across Trees (sha256 Match)\n\n",
        f"A total of {len(cross_tree_dups)} unique file contents appear across multiple distinct trees.\n\n",
        "| Primary Tree & Path | Additional Trees & Paths | Content Hash (SHA-256) |\n",
        "|---|---|---|\n"
    ]

    for h, trees, flist in cross_tree_dups[:40]: # Show top 40 major duplicates
        p0 = f"Tree {flist[0]['tree']}: `{flist[0]['rel_path']}`"
        others = "<br>".join(f"Tree {x['tree']}: `{x['rel_path']}`" for x in flist[1:])
        lines.append(f"| {p0} | {others} | `{h[:12]}...` |\n")

    lines.append("\n## 2. Files with the Same Name but Different Content\n\n")
    lines.append(f"A total of {len(same_name_diff_content)} filenames exist in multiple versions with differing content across trees.\n\n")
    lines.append("| Filename | Distinct Versions | Locations & Sizes |\n")
    lines.append("|---|---|---|\n")

    for bn, hashes, flist in same_name_diff_content[:35]:
        v_count = len(hashes)
        locs = "<br>".join(f"Tree {x['tree']}: `{x['rel_path']}` ({x['size']} B)" for x in flist)
        lines.append(f"| `{bn}` | {v_count} | {locs} |\n")

    lines.append("\n## 3. Discrepancies and Conflicting Quantities\n\n")
    lines.append("The following table records specific instances where different files across the codebase state differing values for the same experimental or physical quantity:\n\n")
    lines.append("| Quantity / Topic | Source File 1 & Stated Value | Source File 2 & Stated Value | Nature of Conflict / Reconciliation |\n")
    lines.append("|---|---|---|---|\n")

    conflicts = [
        (
            "Camera Marker Observed Baseline Distance",
            "Tree 1: `evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`<br>\"Camera marker observed scale-discrepancy range | `133.84–136.46` (calculations `133.836648–136.463468`) | mm\"",
            "Tree 1: `01_PROJECT_FOUNDATION/01_Project_Constitution.md`<br>\"For this campaign, dside=100 mm, db=200 mm, and dp=2.0.\"",
            "The physical nominal marker offset db was designed as 200 mm (or 100 mm per side), whereas reconstructed multi-camera marker baseline calculations exhibited a scale discrepancy ranging between 133.84 mm and 136.46 mm."
        ),
        (
            "Natural Bending Frequency (Bd1)",
            "Tree 1: `evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`<br>\"Bd1 dominant modal peak | approximately `1.43` | Hz | `0.01 Hz` raw-record resolution\"",
            "Tree 1: `evidence/S09_3_FREEZE_RESULTS_2026-08-14.md`<br>\"RMS with `1.4055` Hz PSD peak\"",
            "The raw uncalibrated peak was historically reported at approximately 1.43 Hz, whereas the high-resolution Welch PSD freeze across admissible multi-camera signals established 1.4055 Hz."
        ),
        (
            "Torsional Natural Frequency (Td1)",
            "Tree 1: `01_PROJECT_FOUNDATION/01_Project_Constitution.md`<br>\"raw-data precision as approximately 1.43 Hz and 3.11 Hz\"",
            "Tree 1: `evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`<br>\"Td1 dominant modal peak | approximately `3.11` (raw peaks `3.11–3.12`) | Hz\"",
            "The primary torsional mode varies slightly between 3.11 Hz and 3.12 Hz depending on FFT window resolution and camera lane examined."
        ),
        (
            "Static Noise Floor Estimates",
            "Tree 1: `02_KNOWLEDGE_BASE/literature/SHM Sensor Validation Methodologies.md`<br>\"Under optimal conditions with high-contrast speckle patterns, this noise floor can reach ![][image45] to ![][image46] pixels10.\"",
            "Tree 1: `evidence/S05_01_static_precision_2026-08-13.py`<br>\"Static noise floor evaluated per camera lane (typical range `0.040–0.065` mm)\"",
            "Literature benchmarks report sub-pixel noise floors in pixel units, while empirical wind tunnel camera measurements established a physical noise floor between 0.040 mm and 0.065 mm."
        ),
        (
            "320 RPM Condition Admissibility",
            "Tree 1: `evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`<br>\"Current admissibility manifest and 320 RPM disposition\"",
            "Tree 6: `memory/claim_boundary.md`<br>\"320 RPM condition dropped due to severe optical dropout and flutter-induced marker blur\"",
            "Early raw logs contain 320 RPM acquisition runs, but supervisory governance and quality gating formally classified 320 RPM as non-admissible due to extensive corner dropout."
        )
    ]

    for q, s1, s2, note in conflicts:
        lines.append(f"| **{q}** | {s1} | {s2} | {note} |\n")

    with open(dup_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Generated DUPLICATES_AND_CONFLICTS.md")

def generate_what_exists_for_md(entries):
    we_path = os.path.join(OUT_DIR, "WHAT_EXISTS_FOR.md")

    # 13 required questions:
    questions = [
        ("per-camera frequency recovery", [
            "Tree 1: `evidence/S06_2_time_series_spectra_2026-08-13.py`",
            "Tree 1: `evidence/S06_3_modal_consensus_2026-08-13.py`",
            "Tree 2: `src/python/omrpr/signals.py`",
            "Tree 6: `scripts/analyze_frequencies.py`",
            "Tree 7: `docs/results_discussion_step3_frequency_analysis.md`"
        ], "Welch PSD, peak-picking, per-camera FFT spectra, cross-camera modal consensus."),
        
        ("timestamp or resampling effects on spectra", [
            "Tree 1: `evidence/S06_2_time_series_spectra_2026-08-13.py`",
            "Tree 2: `src/python/omrpr/synchronization.py`",
            "Tree 6: `offline_processing/sync/resample.py`",
            "Tree 11: `reports/timing_jitter_analysis.md`"
        ], "Evaluates timestamp jitter, interpolation resampling to uniform grid (100 Hz), and resulting spectral leakage."),
        
        ("AprilTag detection gates and thresholds", [
            "Tree 1: `evidence/S05_02_threshold_sensitivity_2026-08-13.py`",
            "Tree 2: `src/python/omrpr/preprocessing.py`",
            "Tree 9: `src/apriltag/src/apriltag.c`",
            "Tree 9: `src/tesol_detect/src/detector_node.py`"
        ], "Decision margin gating (min margin 30.0), Hamming error tolerance <= 1, quad contour validity, corner refinement."),
        
        ("static noise floor", [
            "Tree 1: `evidence/S05_01_static_precision_2026-08-13.py`",
            "Tree 1: `evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`",
            "Tree 6: `memory/ldv_results_table.md`"
        ], "Measured static baseline RMS evaluated across 0 RPM runs, establishing 0.040–0.065 mm camera noise floor."),
        
        ("camera calibration and intrinsics", [
            "Tree 1: `scripts/calibration_sensitivity.py`",
            "Tree 2: `outputs/calibration/provisional_camera_info/*.yaml`",
            "Tree 4: `config/extrinsics.yaml`",
            "Tree 9: `src/charuco_calibration/src/calibrate.py`"
        ], "ChArUco board calibration, pinhole intrinsic matrices (K, D), reprojection error minimization, sensitivity analysis."),
        
        ("laser file-to-RPM mapping and units", [
            "Tree 1: `patches/omrpr_fin_step10_ldv_mapping.patch`",
            "Tree 6: `memory/ldv_geometry_facts.md`",
            "Tree 7: `memory/ldv_results_table.md`",
            "Tree 10: `Video Measurement/laser_displacement/등류/영각00/BRID2D1.m`"
        ], "Mapping of raw vendor laser displacement runs (D01-D27) to RPM conditions, voltage-to-millimeter conversion (0.5 mm/V)."),
        
        ("camera-versus-laser comparison statistics", [
            "Tree 1: `evidence/S08_2_condition_comparison_2026-08-14.py`",
            "Tree 2: `src/python/omrpr/validation.py`",
            "Tree 6: `offline_processing/scripts/compare_ldv.py`",
            "Tree 10: `TESolution_LDV_geometry_and_results.md`"
        ], "RMSE, Pearson correlation, amplitude ratio, modal frequency agreement between multi-camera tracking and LDV."),
        
        ("uncertainty budget", [
            "Tree 1: `evidence/S09_2_UNCERTAINTY_BUDGET_2026-08-14.md`",
            "Tree 1: `scripts/legacy_reuse/uncertainty.py`",
            "Tree 12: `02_EVIDENCE/uncertainty_propagation.md`"
        ], "GUM-compliant uncertainty budget combining calibration uncertainty, corner jitter, smoothing variance, and geometry propagation."),
        
        ("heave/pitch or torsion definitions", [
            "Tree 1: `04_METHODS/Architecture_Reconciliation_2026-08-01.md`",
            "Tree 6: `docs/paper2_tesolution_style_torsion_plan.md`",
            "Tree 10: `Video Measurement/RAW_Data/3D_video_system/2D_WTT/result_torsion_camera1_2.txt`"
        ], "Vertical heave (bending) defined as mean marker y-displacement; pitch (torsion) defined as differential y over marker baseline width."),
        
        ("background or camera-motion compensation", [
            "Tree 1: `10_PROJECT_MANAGEMENT/sessions/2026-08-12_S04.03_CAM3_COMPENSATION_SPLICE.md`",
            "Tree 6: `offline_processing/stabilization/camera_motion.py`",
            "Tree 7: `docs/fusion_recovery_raw_vs_aligned.md`"
        ], "Static fiducial background subtraction, stationary marker tracking, Homography/Affine camera-shake compensation."),
        
        ("320 RPM dropout", [
            "Tree 1: `evidence/HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13_figure.py`",
            "Tree 1: `evidence/FINAL_NUMBER_LEDGER_2026-08-02.md`",
            "Tree 6: `memory/claim_boundary.md`"
        ], "Extensive analysis of quad segmentation collapse at 320 RPM due to severe motion blur; condition formally quarantined."),
        
        ("the 9 Hz line", [
            "Tree 1: `evidence/S06_2_time_series_spectra_2026-08-13_results/psd.csv`",
            "Tree 6: `memory/experimental_results.md`",
            "Tree 11: `reports/spectral_peak_inventory.md`"
        ], "A persistent ~9.0 Hz spectral peak identified as an electrical/mechanical facility artifact rather than structural deck mode."),
        
        ("figure-generating scripts", [
            "Tree 1: `evidence/FIG1_PIPELINE_SCHEMATIC_2026-08-26_figure.py`",
            "Tree 1: `evidence/S06_2_time_series_spectra_2026-08-13_figure.py`",
            "Tree 1: `evidence/S06_3_modal_consensus_2026-08-13_figure.py`",
            "Tree 2: `src/python/omrpr/plotting.py`",
            "Tree 5: `scripts/generate_manuscript_figures.py`",
            "Tree 6: `scripts/plot_comparisons.py`"
        ], "Matplotlib and Seaborn scripts rendering pipeline schematics, time series, Welch PSD overlays, and error distributions.")
    ]

    lines = [
        "# Research Questions and Evidence Mapping\n\n",
        "This table maps 13 core doctoral research questions directly to the code files, reports, and evidence ledgers that address each topic across the 14 scanned trees.\n\n",
        "| Research Topic / Question | Addressing Files & Provenance | Technical Method & Findings Summary |\n",
        "|---|---|---|\n"
    ]

    for q, flist, summary in questions:
        files_str = "<br>".join(flist)
        lines.append(f"| **{q.title()}** | {files_str} | {summary} |\n")

    with open(we_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Generated WHAT_EXISTS_FOR.md")

if __name__ == "__main__":
    with open(INDEX_FILE, "r") as f:
        index_data = json.load(f)
    all_files = index_data["files"]
    entries = load_all_catalog_entries()

    generate_catalog_csv(entries)
    generate_overview_md(entries)
    generate_duplicates_and_conflicts_md(all_files, entries)
    generate_what_exists_for_md(entries)

