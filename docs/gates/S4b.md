Stage: S4b (marker-plane rectified estimators H1, H2)   Date written: 2026-10-17 (BEFORE any H1/H2 calculation)
Question (owner, after reading Paper 1): cameras 1 and 2 view the same marker from different places; would expressing motion in a common marker frame make their translation and rotation agree better? Paper 1 anchors a world frame at the tag pose at t = 0 but validates only in-plane X-Y translation; PnP angles are unreliable here (S4: ambiguity in 58/61 streams), so we do NOT invert PnP poses. No extrinsics exist, so no camera-to-camera transform is used.
Estimators (undistorted corners; reference = per-stream median corners, because frame 0 of a wind-on run is already moving; Paper 1 uses the first M frames):
 H_ref = 4-point homography from the tag-plane square (20 mm, corners lb, rb, rt, lt) to the reference corners.
 H1_x, H1_y (mm) = centroid of the four corners of each frame mapped back through H_ref^-1 into the reference tag plane, minus the median. This removes the tilt and foreshortening of the reference view for motion in the tag plane.
 H2_roll (rad) = unwrapped angle of the mean horizontal edge vector of the four mapped corners, minus the median.
Pass criteria:
 1. Synthetic: a 20 mm square viewed with a 20 degree tilt about the vertical axis (real K, D), with a known 0.5 mm vertical motion and a 0.02 rad in-plane rotation: H1 and H2 recover them within 1% (the unrectified P1 and P5 are also reported: P1 should show a foreshortening error of the order 1 - cos(20 deg) in the horizontal direction only).
 2. Real data, same marker: for cam1 versus cam2 (both view the offset marker), the amplitude ratio cam2/cam1 for (a) roll at the torsion line, (b) vertical displacement at the torsion line, (c) vertical displacement at the bending line, over all conditions where cam1 has amplitude > 5x its e0 noise floor at that line. Compare the median |ratio - 1| of (P5, P1) with (H2, H1).
 3. Adoption rule: H replaces P in the summary tables only if the median |ratio - 1| falls by at least 25% (relative) for each of (a), (b), (c) and none of the three worsens by more than 10%. Otherwise both are kept and P stays the default. Either way all columns are stored.
Failure means: the rectified estimators do not improve agreement; the 1-2% cam1/cam2 difference is then treated as measurement noise plus small geometry, and reported as such.
RESULT (2026-10-17; src/bridgedeck/pose.py rectified_channels, tests/test_pose.py, scripts/run_s4.py rerun; columns H1_x_mm, H1_y_mm, H2_roll_rad added to results/s4_pose_by_stream.csv and the per-frame parquet):
 1. PASS: with a 20 degree tilt, H1 and H2 recover the 0.5 mm / 0.02 rad motion within 1%. (17 tests pass in the repo.)
 2. Real data, cam2/cam1 amplitude ratio on the same marker, median |ratio - 1|:
    (a) roll at the torsion line, 16 conditions: P5 1.62%  ->  H2 0.80%  (-51%)
    (b) vertical at the torsion line, 17 conditions: P1 0.29%  ->  H1 0.23%  (-19%)
    (c) vertical at the bending line, 19 conditions: P1 0.45%  ->  H1 0.32%  (-29%)
 3. Adoption rule: NOT met as written (it needs every one of (a), (b), (c) to improve by >= 25%; (b) improved by 19%). No metric worsened. So P stays the default in the summary tables, and H1/H2 are stored and carried into S6 as additional candidate channels (owner decision: compute all, choose later).
Reading: rectification halves the camera-to-camera disagreement in rotation and trims the vertical disagreement a little, but all the disagreements were already small (under 2% for rotation, under 0.5% for vertical), so the effect on the final comparison with the laser will be small compared with the 2.5% tag-size scale uncertainty. Inverting the PnP pose was not done (ambiguous angles, S4).
