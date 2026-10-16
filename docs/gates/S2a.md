Stage: S2a (build the official AprilTag detector)   Date written: 2026-10-16 (BEFORE the build)
Why: the frozen detections and the Sensors-line analysis used AprilRobotics v3.4.5 through its own Python wrapper `apriltag` (tag36h11, threads=1, maxhamming=0, decimate=1.0, blur=0.0, refine_edges=True). pupil-apriltags is a different binding with an unverified bundled library version.
Inputs: https://github.com/AprilRobotics/apriltag tag v3.4.5; project venv (Python 3.12.13, numpy 2.5.4); gcc, cmake, ninja.
Install location (outside the repo, outside ~/.local): /mnt/space/adev/toolchains/apriltag/{src,3.4.5}. The earlier build at ~/.local/opt/apriltag/3.4.5 is not touched.
Pass criteria:
 1. The checked-out commit starts with 94be783 (the commit the tag v3.4.5 resolved to on 2026-10-16: 94be783968e5091bcc9972c72c84fd63efce2935).
 2. Configure, build and install exit 0; libapriltag.so.3.4.5 and the Python module apriltag.cpython-312-*.so exist.
 3. In the project venv, without LD_LIBRARY_PATH: `from apriltag import apriltag` works, and apriltag('tag36h11', threads=1, maxhamming=0, decimate=1.0, blur=0.0, refine_edges=True) constructs.
 4. Independent-generator test: OpenCV's DICT_APRILTAG_36h11 marker for id 0, drawn at 300 px with a white border, is detected as id 0 with hamming 0 and corner positions within 0.5 px of the drawn square; ids 1, 7, 35 are detected as their own ids; an image with no tag returns no detection.
 5. Determinism: the same image detected twice with fresh detector instances gives bit-identical corners.
 6. Real-frame sanity (informational, not part of pass/fail): decode frame 0 of e0_0rpm cam1 from the bag, detect, report corner differences against the frozen detections row (condition e0_0rpm, camera cam1, frame_idx 0). S2 sets the real tolerance.
 7. Provenance file written: commit, source-archive sha256, library sha256, compiler, cmake, python, date. Library sha256 is compared with the earlier build (informational; an RPATH difference is expected to make them differ).
Failure means: the detector cannot be reproduced; do not run S2 with pupil-apriltags as a silent substitute.
Result (2026-10-16): PASS on criteria 1-5 and 7.
 1. commit 94be783968e5091bcc9972c72c84fd63efce2935 (tag v3.4.5).
 2. build + install exit 0 in 10 s (scripts/build_apriltag.sh, log outputs/build_apriltag.log); library /mnt/space/adev/toolchains/apriltag/3.4.5/lib/libapriltag.so.3.4.5, module apriltag.cpython-312-x86_64-linux-gnu.so.
 3. `from apriltag import apriltag` works in the venv with no LD_LIBRARY_PATH (module found through a .pth file; library through RPATH).
 4. tests/test_apriltag_build.py: 8 passed. OpenCV-generated ids 0, 1, 7, 35 detected as their own ids, hamming 0, corners within 0.5 px of the drawn border, centre within 0.05 px (id 0: 5e-5 px); blank image gives no detection.
 5. determinism: bit-identical corners on repeat with fresh detectors.
 6. (informational) real frames, e0_0rpm cam1 frames 0-2: id 0, hamming 0; max corner difference to the frozen detections 0.0125-0.0152 px, centre 0.001-0.008 px; decision margin 69.71/69.80/70.30 vs frozen 69.37/69.63/70.23. Decoding the same JPEG with IMREAD_COLOR->grey vs IMREAD_GRAYSCALE differs by up to 2 grey levels (frame 0) but gives corners within 1e-4 px of each other. Conclusion for S2: pixels are not bit-identical to whatever produced the frozen file, so the S2 'not identical' tolerance branch applies (median <= 0.02 px, 99th percentile <= 0.1 px); the decode path is pinned in S2 Step 0.
 7. provenance: config/apriltag_build.json. Library sha256 differs from the earlier ~/.local build (different RPATH/path, as expected); same source commit.
Not tested: speed on full frames, other tag families.
