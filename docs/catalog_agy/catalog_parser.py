import os
import re
import sys
import json
import csv
import time
from datetime import datetime
from collections import defaultdict

BASE_DIR = "/mnt/phd_data/phd_master"
OUT_DIR = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy"
PROGRESS_FILE = os.path.join(OUT_DIR, "PROGRESS.md")

FACILITY_PATTERNS = [
    re.compile(r"TE\s*Solution", re.IGNORECASE),
    re.compile(r"TESolution", re.IGNORECASE),
    re.compile(r"Chonbuk", re.IGNORECASE),
    re.compile(r"Jeonbuk", re.IGNORECASE),
    re.compile(r"K-ECo", re.IGNORECASE),
    re.compile(r"KOCED", re.IGNORECASE),
]

def sanitize_facility(text):
    if not text:
        return text
    res = text
    for pat in FACILITY_PATTERNS:
        res = pat.sub("the facility", res)
    return res

def clean_extract_quotes(text, max_words=12):
    quotes = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in lines:
        if l.startswith("```") or l.startswith("|") or l.startswith("===") or l.startswith("---"):
            continue
        # Split on sentence boundaries, preserving decimals
        candidates = re.split(r'(?<!\d)\.(?!\d)|\;|\n', l)
        for c in candidates:
            c_str = c.strip()
            c_clean = re.sub(r'^[#\-\*\>\s\d\.\:]+', '', c_str).strip()
            if not c_clean:
                continue
            words = c_clean.split()
            if 3 <= len(words) <= max_words:
                if c_clean in text and c_clean not in quotes:
                    quotes.append(c_clean)
                    if len(quotes) >= 3:
                        return quotes
    return quotes[:3]

def extract_dates(content, filename):
    # Search for YYYY-MM-DD or YYYY-MM
    dates = []
    fn_matches = re.findall(r'(202[0-9]-[01][0-9]-[0-3][0-9])', filename)
    dates.extend(fn_matches)
    text_matches = re.findall(r'(202[0-9]-[01][0-9]-[0-3][0-9])', content[:2000])
    dates.extend(text_matches)
    return list(dict.fromkeys(dates))

def parse_file(full_path, rel_path, tree_num, ext, also_at):
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return None

    lines = content.splitlines()
    num_lines = len(lines)
    
    # 1. Determine kind
    kind = "notes"
    if ext in {".py", ".m", ".sh", ".cpp", ".h", ".launch"}:
        kind = "code"
    elif ext in {".yaml", ".yml", ".toml"} or (ext == ".json" and any(k in rel_path.lower() for k in ["config", "setting", "param", "manifest"])):
        kind = "config"
    elif ext in {".md", ".txt"}:
        lower_rel = rel_path.lower()
        if any(w in lower_rel for w in ["report", "evidence", "result", "freeze", "audit", "review", "ledger", "finding"]):
            kind = "report"
        elif any(w in lower_rel for w in ["plan", "charter", "roadmap", "todo", "task", "roadmap", "protocol"]):
            kind = "plan"
        elif any(w in lower_rel for w in ["config", "manifest", "setting", "registry"]):
            kind = "config"
        else:
            kind = "notes"
    elif ext == ".ipynb":
        kind = "code"

    # 2. Purpose
    purpose = "unclear"
    if ext == ".py":
        m = re.search(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', content, re.DOTALL)
        if m:
            doc = (m.group(1) or m.group(2)).strip()
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', doc) if s.strip()]
            if sents:
                purpose = " ".join(sents[:2])
        if purpose == "unclear":
            comms = []
            for l in lines[:25]:
                ls = l.strip()
                if ls.startswith("#") and not ls.startswith("#!"):
                    comms.append(ls.lstrip("# \t"))
                elif comms and not ls.startswith("#"):
                    break
            if comms:
                purpose = " ".join(comms[:2])
            else:
                purpose = f"Python script implementing functionality in {os.path.basename(rel_path)}."
    elif ext in {".md", ".txt"}:
        header = ""
        first_para = []
        for l in lines[:35]:
            ls = l.strip()
            if not ls:
                if first_para:
                    break
                continue
            if ls.startswith("#"):
                if not header:
                    header = ls.lstrip("# \t")
            else:
                if not ls.startswith("```") and not ls.startswith("|") and not ls.startswith("==="):
                    first_para.append(ls)
        if first_para:
            p_text = " ".join(first_para)
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p_text) if s.strip()]
            purpose = " ".join(sents[:2])
            if header and header.lower() not in purpose.lower() and len(purpose) < 120:
                purpose = f"{header}: {purpose}"
        elif header:
            purpose = header
    elif ext in {".yaml", ".yml", ".toml", ".json"}:
        purpose = f"Configuration file specifying parameters for {os.path.basename(rel_path)}."
    elif ext == ".m":
        comms = []
        for l in lines[:25]:
            ls = l.strip()
            if ls.startswith("%"):
                comms.append(ls.lstrip("% \t"))
            elif comms and not ls.startswith("%"):
                break
        if comms:
            purpose = " ".join(comms[:2])
        else:
            purpose = f"MATLAB processing routine in {os.path.basename(rel_path)}."
    elif ext == ".sh":
        comms = []
        for l in lines[:20]:
            ls = l.strip()
            if ls.startswith("#") and not ls.startswith("#!"):
                comms.append(ls.lstrip("# \t"))
            elif comms and not ls.startswith("#"):
                break
        if comms:
            purpose = " ".join(comms[:2])
        else:
            purpose = f"Shell execution script for {os.path.basename(rel_path)}."
    elif ext in {".cpp", ".h"}:
        comms = []
        for l in lines[:25]:
            ls = l.strip()
            if ls.startswith("//"):
                comms.append(ls.lstrip("/ \t"))
            elif ls.startswith("/*"):
                continue
        if comms:
            purpose = " ".join(comms[:2])
        else:
            purpose = f"C++ implementation for {os.path.basename(rel_path)}."
    elif ext == ".launch":
        purpose = f"ROS launch file configuring nodes and parameters for {os.path.basename(rel_path)}."
    elif ext == ".ipynb":
        purpose = f"Jupyter analysis notebook {os.path.basename(rel_path)}."

    purpose = sanitize_facility(purpose)
    if not purpose or len(purpose.strip()) < 3:
        purpose = "unclear"

    # 3. Method (max 6)
    methods = []
    if ext == ".py":
        classes = re.findall(r'class\s+([a-zA-Z0-9_]+)\s*[:\(]', content)
        for c in classes[:2]:
            methods.append(f"class {c}")
        funcs = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\(', content)
        for fn in funcs:
            if not fn.startswith("_") and fn not in methods and len(methods) < 6:
                methods.append(fn)
    elif ext in {".md", ".txt"}:
        sec_headers = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
        for h in sec_headers:
            clean_h = sanitize_facility(h.strip())
            if clean_h and clean_h not in methods:
                methods.append(clean_h)
            if len(methods) >= 6:
                break
    elif ext == ".m":
        funcs = re.findall(r'function\s+.*=([a-zA-Z0-9_]+)\(', content)
        for fn in funcs[:6]:
            methods.append(fn)
        if not methods:
            # check key MATLAB operations
            for op in ["fft", "welch", "detrend", "filter", "polyfit", "plot"]:
                if re.search(r'\b' + op + r'\b', content):
                    methods.append(op)
    elif ext in {".cpp", ".h"}:
        funcs = re.findall(r'(?:void|int|bool|double|float|cv::Mat)\s+([a-zA-Z0-9_]+)\s*\(', content)
        for fn in funcs[:6]:
            if fn not in methods:
                methods.append(fn)
    elif ext == ".launch":
        nodes = re.findall(r'<node\s+[^>]*pkg=["\']([^"\']+)["\'][^>]*type=["\']([^"\']+)["\']', content)
        for pkg, typ in nodes[:6]:
            methods.append(f"node:{pkg}/{typ}")

    # 4. Inputs
    inputs = []
    path_matches = re.findall(r'["\']([^"\']+\.(?:csv|bag|json|yaml|yml|txt|mat|png|npz|npy|h5))["\']', content)
    for p in path_matches:
        if not p.startswith("http") and not p.startswith("%") and p not in inputs and len(inputs) < 6:
            inputs.append(p)
    read_matches = re.findall(r'(?:open|read_csv|load|read_table|Path)\s*\(\s*["\']([^"\']+)["\']', content)
    for rm in read_matches:
        if not rm.startswith("http") and rm not in inputs and len(inputs) < 6:
            inputs.append(rm)

    # 5. Outputs
    outputs = []
    out_matches = re.findall(r'(?:to_csv|savefig|dump|imwrite)\s*\(\s*["\']([^"\']+)["\']', content)
    for om in out_matches:
        if om not in outputs and len(outputs) < 6:
            outputs.append(om)
    w_matches = re.findall(r'open\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']w', content)
    for wm in w_matches:
        if wm not in outputs and len(outputs) < 6:
            outputs.append(wm)

    # 6. Parameters (NAME=value, max 8)
    parameters = []
    param_matches = re.findall(r'\b([A-Z][A-Z0-9_]{1,24})\s*=\s*([0-9\.]+|"[^"\']{1,30}"|\'[^\'\"]{1,30}\')', content)
    for name, val in param_matches:
        param_str = f"{name}={val}"
        if param_str not in parameters:
            parameters.append(param_str)
        if len(parameters) >= 8:
            break

    # 7. Key Results
    key_results = []
    metric_pattern = re.compile(
        r'\b(?:rmse|mae|std|noise\s*floor|frequency|frequencies|modal|welch|psd|amplitude|dropout|discrepancy|agreement|threshold|snr|damping|drift)\b',
        re.IGNORECASE
    )
    unit_pattern = re.compile(r'\b(?:\d+(?:\.\d+)?)\s*(?:hz|mm|cm|m|deg|rad|db|%|fps|ms|s|rpm)\b', re.IGNORECASE)
    
    for l in lines:
        ls = l.strip()
        if not ls or ls.startswith("```") or ls.startswith("import ") or ls.startswith("from "):
            continue
        has_metric = metric_pattern.search(ls)
        has_unit = unit_pattern.search(ls)
        if (has_metric or has_unit) and re.search(r'\d+(?:\.\d+)?', ls):
            clean = sanitize_facility(ls.strip("| -*#").strip())
            parts = [p.strip() for p in re.split(r'(?<!\d)\.(?!\d)|;', clean) if p.strip()]
            for p in parts:
                if (metric_pattern.search(p) or unit_pattern.search(p)) and re.search(r'\d+(?:\.\d+)?', p):
                    words = p.split()
                    if 3 <= len(words) <= 18:
                        nums = re.findall(r'\d+(?:\.\d+)?', p)
                        if all(num in content for num in nums):
                            res_str = f'"{p}"'
                            if res_str not in key_results:
                                key_results.append(res_str)
                                if len(key_results) >= 5:
                                    break
            if len(key_results) >= 5:
                break

    # 8. Status
    status = "complete"
    lower_content = content.lower()
    if "superseded" in lower_content or "superseded by" in lower_content or "deprecated" in lower_content or "retired" in lower_content:
        status = "superseded"
    elif any(k in lower_content for k in ["todo", "wip", "work in progress", "draft"]):
        status = "partial"
    elif num_lines < 15 and kind == "code":
        status = "stub"
    elif "debug" in rel_path.lower():
        status = "debug"
    else:
        status = "complete"

    # 9. Topics
    topics = []
    topic_keywords = {
        "acquisition": ["camera", "driver", "gige", "sony", "grab", "acquisition", "frame_rate", "fps"],
        "timing": ["timestamp", "jitter", "dt", "clock", "sync", "time_sync", "delay"],
        "detection": ["apriltag", "tag", "corner", "quad", "detector", "hamming", "decision_margin"],
        "calibration": ["calibration", "intrinsics", "extrinsics", "charuco", "reprojection", "distortion", "camera_info"],
        "pose": ["pose", "solvepnp", "rvec", "tvec", "quaternion", "translation", "rotation", "6dof"],
        "fusion": ["fusion", "fuse", "rts", "kalman", "multi-camera", "consensus", "state_estimator"],
        "spectral": ["spectral", "psd", "fft", "welch", "frequency", "mode", "modal", "9 hz", "damping"],
        "laser": ["ldv", "lds", "laser", "keyence", "vibrometer"],
        "comparison": ["comparison", "ground_truth", "rmse", "discrepancy", "agreement", "versus"],
        "uncertainty": ["uncertainty", "covariance", "confidence", "noise_floor", "sensitivity", "budget", "variance"],
        "figures": ["figure", "plot", "matplotlib", "savefig", "chart"],
        "manuscript": ["manuscript", "paper", "latex", "reviewer", "journal", "sensors"],
        "governance": ["charter", "governance", "ledger", "manifest", "rules", "constitution", "registry"],
        "ros": ["ros", "rospy", "roscpp", "catkin", "bag", "subscriber", "publisher", "topic"],
        "utility": ["util", "utils", "helper", "common", "io", "tools"],
        "test": ["test", "pytest", "unittest", "assert", "mock"]
    }
    for top, kws in topic_keywords.items():
        if any(k in lower_content or k in rel_path.lower() for k in kws):
            topics.append(top)
    if not topics:
        topics = ["utility"]

    # 10. Relates to
    relates_to = "none"
    if any(k in lower_content for k in ["spectral", "welch", "psd", "frequency recovery", "9 hz", "paper 2a", "paper2a"]):
        relates_to = "paper2A-spectral"
    elif any(k in lower_content for k in ["ldv", "lds", "laser comparison", "paper 2b", "paper2b", "ground truth"]):
        relates_to = "paper2B-comparison"
    elif any(k in lower_content for k in ["paper 1", "paper1", "real-time ros", "multicamera"]):
        relates_to = "paper1"
    elif any(k in lower_content for k in ["dissertation", "thesis", "doctoral completion"]):
        relates_to = "dissertation"
    elif any(k in lower_content for k in ["background", "literature", "vendor"]):
        relates_to = "background"

    # 11. Open questions (max 3)
    open_questions = []
    if status == "superseded":
        # Check if newer file named
        sup_match = re.search(r'superseded\s+by\s+[`"\'\s]*([a-zA-Z0-9_\-\.\/]+)', content, re.IGNORECASE)
        if sup_match:
            open_questions.append(f"Superseded by {sup_match.group(1).strip('`\"\' ')}")
    oq_matches = re.findall(r'(?:TODO|FIXME|NOTE|Assumption|Question)[:\s]+([^\n\.\;]{5,80})', content, re.IGNORECASE)
    for oq in oq_matches:
        clean_oq = sanitize_facility(oq.strip())
        if clean_oq and clean_oq not in open_questions:
            open_questions.append(clean_oq)
            if len(open_questions) >= 3:
                break

    # 12. Evidence quotes (2-3 exact quotes of at most 12 words copied character for character)
    raw_quotes = clean_extract_quotes(content, max_words=12)
    # Ensure quotes are character-for-character in content
    evidence = []
    for q in raw_quotes:
        if q in content:
            evidence.append(sanitize_facility(q))
    if not evidence and lines:
        for l in lines[:20]:
            clean_l = l.strip().strip("#-* ")
            words = clean_l.split()
            if 3 <= len(words) <= 12 and clean_l in content:
                evidence.append(sanitize_facility(clean_l))
                if len(evidence) >= 2:
                    break

    dates = extract_dates(content, os.path.basename(rel_path))

    return {
        "tree": tree_num,
        "path": rel_path,
        "kind": kind,
        "purpose": purpose,
        "method": methods[:6],
        "inputs": inputs[:6],
        "outputs": outputs[:6],
        "parameters": parameters[:8],
        "key_results": key_results[:6],
        "status": status,
        "topic": topics[:4],
        "relates_to": relates_to,
        "open_questions": open_questions[:3],
        "evidence": evidence[:3],
        "also_at": also_at,
        "_dates": dates
    }

print("Catalog engine parser ready.")
