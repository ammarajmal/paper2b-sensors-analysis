import os, csv, json, glob

audit_dir = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit'
batches = [
    ("G1_paper2_core_part01.csv", "G1_paper2_core", "records_G1_paper2_core_part01.jsonl", "2026-10-18T23:50:00+09:00", 150),
    ("G1_paper2_core_part02.csv", "G1_paper2_core", "records_G1_paper2_core_part02.jsonl", "2026-10-19T02:25:00+09:00", 150),
    ("G1_paper2_core_part03.csv", "G1_paper2_core", "records_G1_paper2_core_part03.jsonl", "2026-10-19T03:10:00+09:00", 150),
    ("G1_paper2_core_part04.csv", "G1_paper2_core", "records_G1_paper2_core_part04.jsonl", "2026-10-19T03:32:00+09:00", 150),
    ("G1_paper2_core_part05.csv", "G1_paper2_core", "records_G1_paper2_core_part05.jsonl", "2026-10-19T03:56:00+09:00", 150),
    ("G1_paper2_core_part06.csv", "G1_paper2_core", "records_G1_paper2_core_part06.jsonl", "2026-10-19T04:01:00+09:00", 150),
    ("G1_paper2_core_part07.csv", "G1_paper2_core", "records_G1_paper2_core_part07.jsonl", "2026-10-19T04:02:00+09:00", 8),
    ("G2_other_paper2_related_part01.csv", "G2_other_paper2_related", "records_G2_other_paper2_related_part01.jsonl", "2026-10-19T04:03:00+09:00", 150),
    ("G2_other_paper2_related_part02.csv", "G2_other_paper2_related", "records_G2_other_paper2_related_part02.jsonl", "2026-10-19T04:03:00+09:00", 150),
    ("G2_other_paper2_related_part03.csv", "G2_other_paper2_related", "records_G2_other_paper2_related_part03.jsonl", "2026-10-19T03:39:00+09:00", 1)
]

lines = [
    "# Audit Progress",
    "",
    "List of completed batch files in `/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/`.",
    "",
    "| Batch File | Group | Completed At | Total Rows | Processed | Skipped | Unreadable |",
    "|---|---|---|---|---|---|---|"
]

total_all = 0
proc_all = 0
skip_all = 0

for bf, grp, rf, dt, tot in batches:
    rpath = os.path.join(audit_dir, rf)
    proc = 0
    if os.path.exists(rpath):
        with open(rpath) as f:
            proc = len(f.readlines())
    skip = tot - proc
    total_all += tot
    proc_all += proc
    skip_all += skip
    lines.append(f"| `{bf}` | `{grp}` | {dt} | {tot} | {proc} | {skip} | 0 |")

lines.append("")
lines.append(f"**Grand Totals across Group G1 & Group G2**: {total_all} rows ({proc_all} processed records, {skip_all} skipped rows, 0 unreadable).")

progress_md = os.path.join(audit_dir, "PROGRESS.md")
with open(progress_md, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Updated {progress_md}: {total_all} total rows ({proc_all} audited, {skip_all} skipped)")
