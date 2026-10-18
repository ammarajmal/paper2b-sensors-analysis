import os
import glob

base = "/mnt/space/data on Computer/~~ DATA TO MOVE/~~~ moST IMPORTANT PERSONAL DATA ~~~/adev/datasets/omrpr/interim/condition-matched/laser_tunnel_a_2024_timeseries"
files = sorted(glob.glob(f"{base}/D*.csv"), key=lambda x: int(os.path.basename(x)[1:-4]))
print(f"Total D*.csv files: {len(files)}")
for f in files[:5]:
    sz = os.path.getsize(f)
    with open(f) as fp:
        lines = [fp.readline().strip() for _ in range(4)]
    print(os.path.basename(f), sz, lines)
