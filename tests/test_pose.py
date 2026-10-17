import numpy as np

from bridgedeck import pose

K = np.array([[20300.0, 0, 960.0], [0, 20300.0, 540.0], [0, 0, 1.0]])
D = np.zeros(14)


def make_frames(n=600, noise=0.0, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / 60.0
    dy = 0.5 * np.sin(2 * np.pi * 1.4318 * t)  # mm
    roll = 0.02 * np.sin(2 * np.pi * 3.0982 * t)
    frames = []
    for i in range(n):
        R = np.array(
            [
                [np.cos(roll[i]), -np.sin(roll[i]), 0],
                [np.sin(roll[i]), np.cos(roll[i]), 0],
                [0, 0, 1],
            ]
        )
        rv = __import__("cv2").Rodrigues(R)[0]
        tv = np.array([[3.0], [dy[i]], [1600.0]])
        pts, _ = __import__("cv2").projectPoints(pose.obj_points("a"), rv, tv, K, D)
        frames.append(pts.reshape(4, 2) + rng.normal(0, noise, (4, 2)))
    return t, dy, roll, np.array(frames)


def test_estimators_recover_known_motion_noise_free():
    t, dy, roll, c = make_frames()
    g_amp = lambda y: pose.line_amplitude(t, y, 1.4318)[0]  # noqa: E731
    cu = pose.undistort(c, K, D)
    mm = pose.TAG_MM / np.median(pose.side_len(cu))
    y1 = (cu.mean(axis=1)[:, 1] - np.median(cu.mean(axis=1)[:, 1])) * mm
    assert abs(g_amp(y1) - 0.5) / 0.5 < 0.01
    p = pose.pnp_stream(c, K, D, "a")
    assert abs(g_amp(p["y"] - np.nanmedian(p["y"])) - 0.5) / 0.5 < 0.01
    assert abs(g_amp(p["y_it"] - np.nanmedian(p["y_it"])) - 0.5) / 0.5 < 0.01
    roll_est = pose.edge_angle(cu)
    assert (
        abs(pose.line_amplitude(t, roll_est - np.median(roll_est), 3.0982)[0] - 0.02) / 0.02 < 0.01
    )


def test_noise_tolerance():
    t, dy, roll, c = make_frames(noise=0.05, seed=2)
    cu = pose.undistort(c, K, D)
    mm = pose.TAG_MM / np.median(pose.side_len(cu))
    y1 = (cu.mean(axis=1)[:, 1] - np.median(cu.mean(axis=1)[:, 1])) * mm
    assert abs(pose.line_amplitude(t, y1, 1.4318)[0] - 0.5) / 0.5 < 0.05
