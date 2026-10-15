import os

BASE_DIR = "/mnt/phd_data/phd_master"

t4 = os.path.join(BASE_DIR, "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin")
for d in sorted(os.listdir(t4)):
    p = os.path.join(t4, d)
    if os.path.isdir(p):
        cnt = sum(len(f) for _, _, f in os.walk(p))
        print(f"Tree 4 dir {d}: {cnt} files")
