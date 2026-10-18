import os

base = "/mnt/archive/00_inbox/adev/datasets/omrpr/raw/camera/rosbag/static_bags"
cams = ["cam1", "cam2", "cam3", "cam2/old"]

for c in cams:
    cdir = os.path.join(base, c)
    for fname in sorted(os.listdir(cdir)):
        p = os.path.join(cdir, fname)
        if os.path.isfile(p):
            with open(p, "r", errors="ignore") as fp:
                l1 = fp.readline().strip()
                l2 = fp.readline().strip()
            print(f"{c}/{fname:35s} | L1: {l1[:40]} | L2: {l2[:40]}")
