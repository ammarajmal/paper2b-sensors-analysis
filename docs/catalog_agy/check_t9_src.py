import os

BASE_DIR = "/mnt/phd_data/phd_master"
t9_src = os.path.join(BASE_DIR, "98_legacy_imports/old_ros_workspaces_2025/tesol_ws/src")

for d in sorted(os.listdir(t9_src)):
    p = os.path.join(t9_src, d)
    if os.path.isdir(p):
        cnt = sum(len(f) for _, _, f in os.walk(p))
        print(f"Tree 9 src/{d}: {cnt} files")
    else:
        print(f"Tree 9 src file: {d}")
