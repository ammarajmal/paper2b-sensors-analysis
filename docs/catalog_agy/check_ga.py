import os

t9_ga = "/mnt/phd_data/phd_master/98_legacy_imports/old_ros_workspaces_2025/tesol_ws/src/gazebo_apriltag"
for d in os.listdir(t9_ga):
    p = os.path.join(t9_ga, d)
    if os.path.isdir(p):
        cnt = sum(len(f) for _, _, f in os.walk(p))
        print(f"gazebo_apriltag/{d}: {cnt} files")
    else:
        print(f"gazebo_apriltag file: {d}")
