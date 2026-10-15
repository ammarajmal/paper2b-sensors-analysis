import os

t1 = "/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research/.claude"
for root, dirs, files in os.walk(t1):
    rel = os.path.relpath(root, t1)
    print(f".claude/{rel}: {len(files)} files, {len(dirs)} dirs")
    for f in files[:3]:
        print(f"   {f}")
