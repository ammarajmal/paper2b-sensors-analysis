import os

BASE_DIR = "/mnt/phd_data/phd_master"

t13 = os.path.join(BASE_DIR, "05_publications/p02_sensors_windtunnel")
for d in sorted(os.listdir(t13)):
    p = os.path.join(t13, d)
    if os.path.isdir(p):
        cnt = sum(len(f) for _, _, f in os.walk(p))
        print(f"Tree 13 dir {d}: {cnt} files")
    else:
        print(f"Tree 13 file {d}")
