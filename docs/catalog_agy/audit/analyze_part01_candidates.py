import csv
import os
import hashlib
import json

audit_dir = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit"

# Load seen hashes from G1 records
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

# Read part01
p1 = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G2_other_paper2_related_part01.csv"
with open(p1) as f:
    rows = list(csv.DictReader(f))

skip_candidates = []
audit_candidates = []

for i, r in enumerate(rows):
    path = r["path"]
    sz = os.path.getsize(path) if os.path.exists(path) else -1
    
    # Check if empty
    if sz <= 1: # 0 bytes or 1 byte newline
        skip_candidates.append((i+1, path, "empty file (no data rows)"))
        continue
        
    # Check duplicate
    with open(path, "rb") as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    if h in seen_hashes:
        skip_candidates.append((i+1, path, f"exact duplicate of {seen_hashes[h]}"))
        continue
        
    # Check third party / vendor
    if "dinov3" in path:
        skip_candidates.append((i+1, path, "third-party open source library (DINOv3 vision backbone, no research content)"))
        continue
    if "miniforge3" in path or "site-packages" in path:
        skip_candidates.append((i+1, path, "third-party Python standard library / environment file (no research content)"))
        continue
    if "debugpy" in path or ".antigravity/extensions" in path:
        skip_candidates.append((i+1, path, "third-party IDE debugger extension library (debugpy/winappdbg, no research content)"))
        continue
    if "realsense-ros/realsense2_camera/scripts/importRosbag" in path:
        skip_candidates.append((i+1, path, "third-party vendor utility (Event-driven Perception for Robotics rosbag unpacker, no project research content)"))
        continue
    if "librealsense/third-party" in path:
        skip_candidates.append((i+1, path, "third-party open source library (GLFW window library, no research content)"))
        continue
    if "librealsense/wrappers/python/examples" in path:
        skip_candidates.append((i+1, path, "third-party vendor SDK example (Intel RealSense box dimensioner example, no project research content)"))
        continue
    if "librealsense/wrappers/matlab" in path:
        skip_candidates.append((i+1, path, "third-party vendor SDK example (Intel RealSense MATLAB wrapper example, no project research content)"))
        continue
        
    # Otherwise audit candidate
    seen_hashes[h] = path
    audit_candidates.append((i+1, path, sz))

print(f"Skipped candidates: {len(skip_candidates)}")
for idx, p, reason in skip_candidates:
    print(f"  Row {idx:3d}: {reason} -> {p}")

print(f"\nAudit candidates: {len(audit_candidates)}")
for idx, p, sz in audit_candidates:
    print(f"  Row {idx:3d} (size {sz:6d}): {p}")
