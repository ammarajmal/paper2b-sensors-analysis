import os

prefix = "/mnt/phd_data/phd_master/"

def check_verbatim(rel_path, target_snippet):
    full_path = os.path.join(prefix, rel_path)
    with open(full_path, "r", errors="ignore") as f:
        content = f.read()
    if target_snippet in content:
        words = len(target_snippet.split())
        print(f"OK ({words} w): {repr(target_snippet[:40])}")
        return True
    else:
        print(f"FAIL: {repr(target_snippet)} NOT IN {rel_path}")
        return False

# Test line 168
check_verbatim("02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/sections/03_results.md",
               "1.4303 Hz (bending) and 3.1036 Hz (torsion) per the facility source")
