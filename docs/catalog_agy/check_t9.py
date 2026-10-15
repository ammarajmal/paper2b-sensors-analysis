import os

BASE_DIR = "/mnt/phd_data/phd_master"
t9 = os.path.join(BASE_DIR, "98_legacy_imports/old_ros_workspaces_2025/tesol_ws")

for d in sorted(os.listdir(t9)):
    p = os.path.join(t9, d)
    if os.path.isdir(p):
        cnt = sum(len(f) for _, _, f in os.walk(p))
        print(f"Tree 9 dir {d}: {cnt} files")
