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

# Load all paths from part01 (both audited and skipped)
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

skipped = []
for i, r in enumerate(rows):
    path = r["path"]
    sz = os.path.getsize(path) if os.path.exists(path) else -1
    if sz <= 1:
        skipped.append((path, "empty file (0 bytes)"))
        continue
    if sz <= 22 and path.endswith(".csv"):
        with open(path, "r", errors="ignore") as fp:
            lines = [l.strip() for l in fp.readlines() if l.strip()]
        if len(lines) <= 1:
            skipped.append((path, "empty register template (header only, no data rows)"))
            continue
    with open(path, "rb") as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    if h in seen_hashes:
        skipped.append((path, f"exact duplicate of {seen_hashes[h]}"))
        continue
    if "Adobe Photoshop" in path:
        skipped.append((path, "third-party commercial software installation package (Adobe Photoshop, no research content)"))
        continue
    if "librealsense/doc" in path:
        skipped.append((path, "third-party vendor SDK documentation (Intel RealSense Windows docs, no research content)"))
        continue
    if ".antigravity/extensions" in path or "walkthrough/install-python-windows" in path:
        skipped.append((path, "third-party IDE walkthrough documentation (Python VSCode extension, no research content)"))
        continue
    if "FastLZ-master/.github" in path:
        skipped.append((path, "third-party open source library CI configuration (FastLZ workflows, no research content)"))
        continue
    if "window-state.json" in path or "window_state.yml" in path:
        skipped.append((path, "third-party editor GUI state cache (window-state, no research content)"))
        continue
    if "github.vscode-pull-request-github" in path:
        skipped.append((path, "third-party editor extension cache (VSCode GitHub PR cache, no research content)"))
        continue
    if "suspend-repair" in path:
        skipped.append((path, "operating system debug log (Linux system suspend failure log, no research content)"))
        continue
    if "Anum Saeed_visa" in path:
        skipped.append((path, "administrative personal document (visa photograph dimensions, no research content)"))
        continue
    if ".aider/caches" in path:
        skipped.append((path, "third-party tool cache (aider model pricing cache, no research content)"))
        continue
    if "gstack/.github" in path or ".agents/skills/gstack" in path:
        skipped.append((path, "third-party developer tool CI workflow (gstack GitHub Actions, no research content)"))
        continue
    if path.endswith("SDKinstallation.txt"):
        skipped.append((path, "coursework administrative note (course hardware installation notice, no research content)"))
        continue
    if path.endswith("Setting up Arduino IDE for Sensor.txt"):
        skipped.append((path, "coursework setup URLs (external links to Arduino setup, no research content)"))
        continue
    seen_hashes[h] = path

out_path = os.path.join(audit_dir, "skipped_G2_other_paper2_related_part02.csv")
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["path", "reason"])
    for path, reason in skipped:
        writer.writerow([path, reason])

print(f"Wrote {len(skipped)} skipped rows to {out_path}")
