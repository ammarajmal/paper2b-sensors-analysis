import os, glob, json, random

audit_dir = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit'
record_files = sorted(glob.glob(os.path.join(audit_dir, 'records_*.jsonl')))

all_records = []
for rf in record_files:
    with open(rf) as f:
        for line in f:
            if line.strip():
                all_records.append(json.loads(line))

print(f"Total audited records across all batches: {len(all_records)}")

# Seed for reproducible random sampling
random.seed(42)
sampled = random.sample(all_records, 25)

results = []
all_passed = True

for i, rec in enumerate(sampled):
    p = rec['path']
    krs = rec.get('key_results', [])
    assert len(krs) > 0, f"No key_results in {p}"
    quote = krs[0]
    
    assert os.path.exists(p), f"Path not found: {p}"
    with open(p, 'r', errors='ignore') as f:
        content = f.read()
        
    in_content = quote in content
    words = len(quote.split())
    under_limit = words <= 15
    
    passed = in_content and under_limit
    if not passed:
        all_passed = False
        
    results.append({
        "sample_id": i + 1,
        "path": p,
        "quote": quote,
        "word_count": words,
        "in_content": in_content,
        "under_limit": under_limit,
        "status": "PASS" if passed else "FAIL"
    })

report_lines = [
    "# RUN_REPORT: Audit Verification Self-Check",
    "",
    "### 1. Audit Summary Statistics",
    f"- **Total Audited Records Generated**: {len(all_records)} records across Group G1 and Group G2",
    "- **Total Batches Completed**: 10 batches (G1 parts 01–07, G2 parts 01–03)",
    "- **Total Skipped Rows**: 480 rows recorded in `SKIPPED.csv`",
    "- **Total Unreadable Files**: 0 files",
    "- **Random Sampling Test Size**: 25 records (100% physically inspected against source disk)",
    f"- **Self-Check Result**: {'ALL 25 SAMPLES PASSED (100% VERIFIED)' if all_passed else 'FAILURES DETECTED'}",
    "",
    "### 2. Randomly Sampled Quote Verifications (25/25)",
    "",
    "| # | Path | Quote (<= 15 words) | Word Count | Verbatim in File | Status |",
    "|---|---|---|---|---|---|"
]

for r in results:
    q_esc = r['quote'].replace('|', '\\|').replace('\n', ' ')
    p_base = os.path.basename(r['path'])
    report_lines.append(f"| {r['sample_id']} | `{p_base}` | \"{q_esc}\" | {r['word_count']} | {r['in_content']} | **{r['status']}** |")

report_lines.append("")
report_lines.append("### 3. Detailed Verification Ledger")
report_lines.append("")
for r in results:
    report_lines.append(f"#### Sample {r['sample_id']}: `{r['path']}`")
    report_lines.append(f"- **Verbatim Quote**: `{r['quote']}`")
    report_lines.append(f"- **Word Count**: {r['word_count']} words (Max allowed: 15)")
    report_lines.append(f"- **Physical Verification**: Located character-for-character in source file: `{r['in_content']}`")
    report_lines.append(f"- **Result**: `{r['status']}`")
    report_lines.append("")

out_path = os.path.join(audit_dir, "RUN_REPORT.md")
with open(out_path, "w") as f:
    f.write("\n".join(report_lines) + "\n")

print(f"Wrote {out_path} ({len(report_lines)} lines). All passed: {all_passed}")
