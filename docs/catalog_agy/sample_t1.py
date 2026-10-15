import os

BASE_DIR = "/mnt/phd_data/phd_master"
t1 = os.path.join(BASE_DIR, "02_research_projects/p02_ros_multicamera_shm/structural_vision_research")

files_to_sample = [
    "00_READ_FIRST/START_HERE.md",
    "01_PROJECT_FOUNDATION/00_Research_Charter.md",
    "scripts/calibration_sensitivity.py",
    ".claude/worktrees/snug-swinging-aurora/evidence/S09_3_FREEZE_RESULTS_2026-08-14.md"
]

for f in files_to_sample:
    p = os.path.join(t1, f)
    if os.path.exists(p):
        print(f"=== {f} ===")
        with open(p, "r", encoding="utf-8", errors="ignore") as fp:
            lines = [fp.readline() for _ in range(25)]
        print("".join(lines))
    else:
        print(f"NOT FOUND: {p}")
