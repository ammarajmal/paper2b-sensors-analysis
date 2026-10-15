import os
import json
from refined_helpers import clean_extract_quotes, extract_purpose_py, extract_key_results

t1_base = "/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research"
samples = [
    "scripts/calibration_sensitivity.py",
    ".claude/worktrees/snug-swinging-aurora/evidence/S09_3_FREEZE_RESULTS_2026-08-14.md",
    ".claude/worktrees/snug-swinging-aurora/evidence/FINAL_NUMBER_LEDGER_2026-08-02.md"
]

for s in samples:
    fp = os.path.join(t1_base, s)
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        lines = content.splitlines()
        print(f"=== {s} ===")
        print("Purpose:", extract_purpose_py(content, lines) if s.endswith(".py") else "MD")
        print("Key results:", extract_key_results(content, lines, "report"))
        print("Quotes:", clean_extract_quotes(content, 12))
