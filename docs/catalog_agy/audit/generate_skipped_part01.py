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

p1 = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G2_other_paper2_related_part01.csv"
with open(p1) as f:
    rows = list(csv.DictReader(f))

skipped = []
for i, r in enumerate(rows):
    path = r["path"]
    sz = os.path.getsize(path) if os.path.exists(path) else -1
    if sz <= 1:
        skipped.append((path, "empty file (1 byte newline, no data)"))
        continue
    with open(path, "rb") as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    if h in seen_hashes:
        skipped.append((path, f"exact duplicate of {seen_hashes[h]}"))
        continue
    if "dinov3" in path:
        skipped.append((path, "third-party open source library (DINOv3 vision backbone, no research content)"))
        continue
    if "miniforge3" in path:
        skipped.append((path, "third-party Python standard library or environment file (no research content)"))
        continue
    if "debugpy" in path or ".antigravity/extensions" in path:
        skipped.append((path, "third-party IDE debugger extension library (debugpy/winappdbg, no research content)"))
        continue
    if "realsense-ros/realsense2_camera/scripts/importRosbag" in path:
        skipped.append((path, "third-party open source library (Event-driven Perception for Robotics rosbag unpacker, no project research content)"))
        continue
    if "librealsense/third-party" in path:
        skipped.append((path, "third-party open source library (GLFW window library, no research content)"))
        continue
    if "librealsense/wrappers/python/examples" in path:
        skipped.append((path, "third-party vendor SDK example (Intel RealSense box dimensioner example, no project research content)"))
        continue
    if "librealsense/wrappers/matlab" in path:
        skipped.append((path, "third-party vendor SDK example (Intel RealSense MATLAB wrapper example, no project research content)"))
        continue
    seen_hashes[h] = path

out_path = os.path.join(audit_dir, "skipped_G2_other_paper2_related_part01.csv")
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["path", "reason"])
    for path, reason in skipped:
        writer.writerow([path, reason])

print(f"Wrote {len(skipped)} skipped rows to {out_path}")
