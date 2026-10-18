import csv
import os
import hashlib
import json

audit_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit"

# Load seen hashes from G1
g1_records = [
    "records_G1_paper2_core_part01.jsonl",
    "records_G1_paper2_core_part02.jsonl",
    "records_G1_paper2_core_part03.jsonl"
]
seen_hashes = {}
for g1 in g1_records:
    p = os.path.join(audit_dir, g1)
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                rec = json.loads(line)
                path = rec["path"]
                if os.path.exists(path) and os.path.isfile(path):
                    with open(path, "rb") as fp:
                        h = hashlib.sha256(fp.read()).hexdigest()
                    if h not in seen_hashes:
                        seen_hashes[h] = path

# Add part01 files to seen_hashes
p1 = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G2_other_paper2_related_part01.csv"
with open(p1) as f:
    for r in csv.DictReader(f):
        path = r["path"]
        if os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) > 0:
            with open(path, "rb") as fp:
                h = hashlib.sha256(fp.read()).hexdigest()
            if h not in seen_hashes:
                seen_hashes[h] = path

p2 = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G2_other_paper2_related_part02.csv"
with open(p2) as f:
    rows = list(csv.DictReader(f))

skip_candidates = []
audit_candidates = []

for i, r in enumerate(rows):
    path = r["path"]
    sz = os.path.getsize(path) if os.path.exists(path) else -1
    
    # Check if empty / header only
    if sz <= 22 and path.endswith(".csv"):
        # Let check if it has data rows
        with open(path, "r", errors="ignore") as fp:
            lines = [l.strip() for l in fp.readlines() if l.strip()]
        if len(lines) <= 1:
            skip_candidates.append((i+1, path, "empty register template (header only, no data rows)"))
            continue

    if sz <= 1:
        skip_candidates.append((i+1, path, "empty file (0 bytes)"))
        continue

    with open(path, "rb") as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    if h in seen_hashes:
        skip_candidates.append((i+1, path, f"exact duplicate of {seen_hashes[h]}"))
        continue

    # Third party / vendor / irrelevant configs
    if "Adobe Photoshop" in path:
        skip_candidates.append((i+1, path, "third-party commercial software installation package (Adobe Photoshop, no research content)"))
        continue
    if "librealsense/doc" in path:
        skip_candidates.append((i+1, path, "third-party vendor SDK documentation (Intel RealSense Windows docs, no research content)"))
        continue
    if ".antigravity/extensions" in path or "walkthrough/install-python-windows" in path:
        skip_candidates.append((i+1, path, "third-party IDE walkthrough documentation (Python VSCode extension, no research content)"))
        continue
    if "FastLZ-master/.github" in path:
        skip_candidates.append((i+1, path, "third-party open source library CI configuration (FastLZ workflows, no research content)"))
        continue
    if "window-state.json" in path or "window_state.yml" in path:
        skip_candidates.append((i+1, path, "third-party editor GUI state cache (window-state, no research content)"))
        continue
    if "github.vscode-pull-request-github" in path:
        skip_candidates.append((i+1, path, "third-party editor extension cache (VSCode GitHub PR cache, no research content)"))
        continue
    if "suspend-repair" in path:
        skip_candidates.append((i+1, path, "operating system debug log (Linux system suspend failure log, no research content)"))
        continue
    if "Anum Saeed_visa" in path:
        skip_candidates.append((i+1, path, "administrative personal document (visa photograph dimensions, no research content)"))
        continue
    if ".aider/caches" in path:
        skip_candidates.append((i+1, path, "third-party tool cache (aider model pricing cache, no research content)"))
        continue
    if "gstack/.github" in path or ".agents/skills/gstack" in path:
        skip_candidates.append((i+1, path, "third-party developer tool CI workflow (gstack GitHub Actions, no research content)"))
        continue
    if path.endswith("SDKinstallation.txt"):
        skip_candidates.append((i+1, path, "coursework administrative note (course hardware installation notice, no research content)"))
        continue
    if path.endswith("Setting up Arduino IDE for Sensor.txt"):
        skip_candidates.append((i+1, path, "coursework setup URLs (external links to Arduino setup, no research content)"))
        continue

    seen_hashes[h] = path
    audit_candidates.append((i+1, path, sz))

print(f"Skipped candidates in part02: {len(skip_candidates)}")
for idx, p, reason in skip_candidates:
    print(f"  Row {idx:3d}: {reason} -> {p}")

print(f"\nAudit candidates in part02: {len(audit_candidates)}")
for idx, p, sz in audit_candidates:
    print(f"  Row {idx:3d} (size {sz:6d}): {p}")
