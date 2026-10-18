"""A1 phases 1-3 (docs/gates/A1_audit.md): read-only inventory of all drive roots. Writes results/audit/inventory_*.csv only."""
import csv, os, sys, time
from pathlib import Path
ROOTS = {"phd_data": "/mnt/phd_data", "phd-legacy": "/mnt/phd-legacy", "phd": "/mnt/phd", "data": "/mnt/data", "archive": "/mnt/archive", "career-legacy": "/mnt/career-legacy",
         "career": "/mnt/career", "wdc_phd": "/mnt/wdc_phd", "wdc_career": "/mnt/wdc_career", "space": "/mnt/space", "home": "/home/ammar"}
PRUNE = {".git", "__pycache__", ".venv", "node_modules", "build", "devel", "install", "site-packages", ".cache", ".local", ".npm", ".cargo", "venv310", ".ollama", "snap"}
KEYS = ("paper2", "p02", "omrpr", "apriltag", "tesol", "sensors", "measurement", "laser", "rosbag", "structural_vision", "bridgedeck", "shm-displacement", "wind", "windtunnel", "ldv")
EXTS = {".py", ".m", ".sh", ".md", ".txt", ".yaml", ".yml", ".json", ".csv", ".tex", ".ipynb", ".bib", ".cfg", ".launch"}
OUT = Path("/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/results/audit"); OUT.mkdir(parents=True, exist_ok=True)
log = open(OUT / "inventory_log.txt", "w")
only = sys.argv[1:] or list(ROOTS)
for name in only:
    root = ROOTS[name]; t0 = time.time(); n = 0; err = []
    if not os.path.isdir(root) or not os.listdir(root): log.write(f"{name}\tEMPTY_OR_UNMOUNTED\n"); log.flush(); continue
    dev = os.stat(root).st_dev
    with open(OUT / f"inventory_{name}.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["root", "path", "size", "mtime", "ext", "candidate"])
        for dp, dn, fn in os.walk(root, onerror=lambda e: err.append(str(e)[:120])):
            if name == "space" and "bridgedeck-vision-pipeline" in dp: dn[:] = []; continue
            dn[:] = [d for d in dn if d not in PRUNE and not d.startswith("venv") and not d.startswith(".venv")]
            try:
                if os.stat(dp).st_dev != dev: dn[:] = []; continue
            except OSError as e: err.append(str(e)[:120]); continue
            for f in fn:
                p = os.path.join(dp, f)
                try: st = os.lstat(p)
                except OSError as e: err.append(str(e)[:120]); continue
                ext = os.path.splitext(f)[1].lower(); low = p.lower()
                cand = int(ext in EXTS and st.st_size < 2_000_000 and any(k in low for k in KEYS))
                w.writerow([name, p, st.st_size, int(st.st_mtime), ext, cand]); n += 1
    log.write(f"{name}\tfiles={n}\tseconds={time.time()-t0:.0f}\terrors={len(err)}\t{'; '.join(err[:3])}\n"); log.flush()
log.write("DONE\n"); log.close()
