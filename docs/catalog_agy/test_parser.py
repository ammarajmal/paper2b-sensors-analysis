import os
import re
import json

from catalog_engine_helpers import sanitize_facility, get_exact_quote

def parse_file(full_path, rel_path, tree_num, ext, also_at):
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    lines = content.splitlines()
    num_lines = len(lines)
    
    # 1. Determine kind
    kind = "notes"
    if ext in {".py", ".m", ".sh", ".cpp", ".h", ".launch"}:
        kind = "code"
    elif ext in {".yaml", ".yml", ".toml"} or (ext == ".json" and "config" in rel_path.lower()):
        kind = "config"
    elif ext in {".md", ".txt"}:
        lower_rel = rel_path.lower()
        if any(w in lower_rel for w in ["report", "evidence", "result", "freeze", "audit", "review", "ledger"]):
            kind = "report"
        elif any(w in lower_rel for w in ["plan", "charter", "roadmap", "todo", "task"]):
            kind = "plan"
        elif any(w in lower_rel for w in ["config", "manifest", "setting"]):
            kind = "config"
        else:
            kind = "notes"

    # 2. Purpose
    purpose = "unclear"
    if ext == ".py":
        # Extract docstring
        doc_match = re.search(r'^(?:[ \t]*\n)*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')', content, re.DOTALL)
        if doc_match:
            doc = (doc_match.group(1) or doc_match.group(2)).strip()
            # first 1-2 sentences
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', doc) if s.strip()]
            purpose = " ".join(sents[:2])
        else:
            # check leading comments
            comment_lines = []
            for l in lines[:15]:
                l_s = l.strip()
                if l_s.startswith("#") and not l_s.startswith("#!"):
                    comment_lines.append(l_s.lstrip("# \t"))
                elif comment_lines and not l_s.startswith("#"):
                    break
            if comment_lines:
                purpose = " ".join(comment_lines[:2])
            else:
                purpose = f"Python script for {os.path.basename(rel_path)}."
    elif ext in {".md", ".txt"}:
        # Extract first non-header paragraph or header
        header = ""
        first_para = []
        for l in lines[:30]:
            l_s = l.strip()
            if not l_s:
                if first_para:
                    break
                continue
            if l_s.startswith("#"):
                if not header:
                    header = l_s.lstrip("# \t")
            else:
                first_para.append(l_s)
        if first_para:
            p_text = " ".join(first_para)
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p_text) if s.strip()]
            purpose = " ".join(sents[:2])
            if header and header not in purpose:
                purpose = f"{header}: {purpose}"
        elif header:
            purpose = header
    elif ext in {".yaml", ".yml", ".toml", ".json"}:
        purpose = f"Configuration file specifying settings for {os.path.basename(rel_path)}."
    elif ext == ".m":
        m_comments = []
        for l in lines[:20]:
            l_s = l.strip()
            if l_s.startswith("%"):
                m_comments.append(l_s.lstrip("% \t"))
            elif m_comments:
                break
        if m_comments:
            purpose = " ".join(m_comments[:2])
        else:
            purpose = f"MATLAB processing routine in {os.path.basename(rel_path)}."
    elif ext == ".sh":
        sh_comments = []
        for l in lines[:15]:
            l_s = l.strip()
            if l_s.startswith("#") and not l_s.startswith("#!"):
                sh_comments.append(l_s.lstrip("# \t"))
            elif sh_comments:
                break
        if sh_comments:
            purpose = " ".join(sh_comments[:2])
        else:
            purpose = f"Shell script executing workflow for {os.path.basename(rel_path)}."

    purpose = sanitize_facility(purpose)
    if not purpose or len(purpose.strip()) < 3:
        purpose = "unclear"

    # 3. Method (max 6)
    methods = []
    # Identify key functions or markdown headings
    if ext == ".py":
        funcs = re.findall(r'def\s+([a-zA-Z0-9_]+)\s*\(', content)
        classes = re.findall(r'class\s+([a-zA-Z0-9_]+)\s*[:\(]', content)
        for c in classes[:2]:
            methods.append(f"class {c}")
        for fn in funcs:
            if not fn.startswith("_") and fn not in methods and len(methods) < 6:
                methods.append(fn)
    elif ext in {".md", ".txt"}:
        sec_headers = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
        for h in sec_headers:
            clean_h = h.strip()
            if clean_h and clean_h not in methods:
                methods.append(clean_h)
            if len(methods) >= 6:
                break
    elif ext == ".m":
        funcs = re.findall(r'function\s+.*=([a-zA-Z0-9_]+)\(', content)
        for fn in funcs[:6]:
            methods.append(fn)
            
    # 4. Inputs
    inputs = []
    # Search for paths / extensions read
    path_matches = re.findall(r'["\']([^"\']+\.(?:csv|bag|json|yaml|yml|txt|mat|png|npz|npy|h5))["\']', content)
    for p in path_matches:
        if p not in inputs and len(inputs) < 6:
            inputs.append(p)
    # pd.read_csv, np.load, open
    read_matches = re.findall(r'(?:open|read_csv|load|read_table|Path)\s*\(\s*["\']([^"\']+)["\']', content)
    for rm in read_matches:
        if rm not in inputs and len(inputs) < 6:
            inputs.append(rm)

    # 5. Outputs
    outputs = []
    out_matches = re.findall(r'(?:to_csv|savefig|dump|imwrite)\s*\(\s*["\']([^"\']+)["\']', content)
    for om in out_matches:
        if om not in outputs and len(outputs) < 6:
            outputs.append(om)
    # open with 'w'
    w_matches = re.findall(r'open\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']w', content)
    for wm in w_matches:
        if wm not in outputs and len(outputs) < 6:
            outputs.append(wm)

    # 6. Parameters (NAME=value, max 8)
    parameters = []
    param_matches = re.findall(r'\b([A-Z][A-Z0-9_]{1,20})\s*=\s*([0-9\.]+|"[^"\']{1,30}"|\'[^\'\"]{1,30}\')', content)
    for name, val in param_matches:
        param_str = f"{name}={val}"
        if param_str not in parameters:
            parameters.append(param_str)
        if len(parameters) >= 8:
            break

    # 7. Key Results (numbers or findings stated with exact words in quotes)
    key_results = []
    if kind == "report" or ext in {".md", ".txt"}:
        # Look for findings with numbers in markdown lines
        # Look for patterns like "RMSE ... 0.05 mm" or "f = 3.65 Hz" or percentage
        res_lines = []
        for l in lines:
            l_s = l.strip()
            # check if line has numbers and units or metric keywords
            if any(k in l_s.lower() for k in ["rmse", "error", "accuracy", "frequency", "hz", "mm", "noise floor", "threshold", "percent", "%", "std", "margin"]):
                # check if there is a number
                if re.search(r'\d+(?:\.\d+)?', l_s):
                    # extract a concise clause or sentence
                    clauses = re.split(r'[\;\:\*]', l_s)
                    for cl in clauses:
                        cl_s = cl.strip().strip("-| ")
                        if re.search(r'\d+(?:\.\d+)?', cl_s) and len(cl_s.split()) <= 15:
                            # Verify all numbers in cl_s appear in file
                            nums = re.findall(r'\d+(?:\.\d+)?', cl_s)
                            if all(num in content for num in nums):
                                if cl_s not in key_results:
                                    key_results.append(f'"{cl_s}"')
                                    if len(key_results) >= 4:
                                        break
            if len(key_results) >= 4:
                break

    # 8. Status
    status = "complete"
    lower_content = content.lower()
    if "superseded" in lower_content or "superseded by" in lower_content or "deprecated" in lower_content:
        status = "superseded"
    elif any(k in lower_content for k in ["todo", "wip", "work in progress", "draft"]):
        status = "partial"
    elif num_lines < 15 and kind == "code":
        status = "stub"
    elif "debug" in rel_path.lower() or "test" in rel_path.lower():
        status = "complete"
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

    # 11. Open questions
    open_questions = []
    oq_matches = re.findall(r'(?:TODO|FIXME|NOTE|Assumption|Question)[:\s]+([^\n\.\;]{5,80})', content, re.IGNORECASE)
    for oq in oq_matches:
        clean_oq = oq.strip()
        if clean_oq and clean_oq not in open_questions:
            open_questions.append(clean_oq)
            if len(open_questions) >= 3:
                break

    # 12. Evidence quotes (2-3 exact quotes of at most 12 words copied character for character)
    evidence = get_exact_quote(content, max_words=12)

    entry = {
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
        "also_at": also_at
    }
    return entry

# Test parse on sample files
t1_base = "/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research"
samples = [
    "00_READ_FIRST/START_HERE.md",
    "scripts/calibration_sensitivity.py",
    ".claude/worktrees/snug-swinging-aurora/evidence/S09_3_FREEZE_RESULTS_2026-08-14.md"
]
for s in samples:
    fp = os.path.join(t1_base, s)
    if os.path.exists(fp):
        res = parse_file(fp, s, 1, os.path.splitext(s)[1].lower(), [])
        print(f"=== {s} ===")
        print(json.dumps(res, indent=2))
