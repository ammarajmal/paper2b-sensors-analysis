import os

files_to_check = [
    "/mnt/space/data on Computer/~~ DATA TO MOVE/~~~ moST IMPORTANT PERSONAL DATA ~~~/adev/datasets/omrpr/interim/condition-matched/camera_tunnel_a_2024.csv",
    "/mnt/phd_data/phd_master/98_legacy_imports/old_ros_workspaces_2025/tesol_ws_backup/optimized_camera_params.yaml",
    "/mnt/phd_data/phd_master/98_legacy_imports/old_ros_workspaces_2025/tesol_ws/src/gsim_urdf_pkg/urdf/gsim_urdf_pkg.csv",
    "/mnt/phd_data/phd_master/98_legacy_imports/old_ros_workspaces_2025/ros_ws/src/gig_data_/csvfiles/old/LDV Data/LDV_ARUCO_15Hz.csv",
    "/mnt/phd_data/phd_master/98_legacy_imports/source_old_phd_master_cur/p2/shm-displacement-project-github/displacement_sony_cam1.csv",
    "/mnt/archive/00_inbox/adev/datasets/omrpr/raw/camera/rosbag/static_bags/cam2/old/capture_metadata.csv"
]

for p in files_to_check:
    print("="*60)
    print("PATH:", p)
    with open(p, "r", errors="ignore") as fp:
        lines = [fp.readline().strip() for _ in range(6)]
    print("\n".join(lines))
