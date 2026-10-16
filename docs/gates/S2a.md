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
Result: (filled after the run)
