import os

base = "/mnt/phd_data/phd_master/09_courses_training/c02_fall_2022/3. Sensors"
files = [
    "MATLAB/untitled2.m",
    "MATLAB/experiment_m.m",
    "_experiment.m",
    "filterexample/experimen.m",
    "MATLAB/fftexample.m",
    "MATLAB/filtertest.m",
    "MATLAB/filterfast.m",
    "filterexample/hpfiltdesfast.m"
]

for f in files:
    p = os.path.join(base, f)
    print("=== FILE:", f)
    with open(p, "r", errors="ignore") as fp:
        lines = [fp.readline().strip() for _ in range(8)]
    print("\n".join(lines))
