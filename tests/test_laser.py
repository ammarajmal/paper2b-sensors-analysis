import numpy as np

from bridgedeck import laser


def test_channel_algebra_and_vendor_halving():
    s = laser.SESSIONS["y2025"]
    b = np.zeros(2)
    v = np.column_stack(
        [np.zeros(100), np.full(100, 1.0), np.zeros(100)]
    )  # side reads 1 V, centre 0 V
    ch = laser.channels(v, b, s)
    assert np.allclose(ch["torsion_diff_mm"], 27.0)  # 1 V * 2.7 cm/V * 10 mm/cm
    assert np.allclose(ch["bending_avg_mm"], 13.5)
    assert np.allclose(ch["torsion_proxy_mm"], 27.0 * 20 / 13)
    assert np.allclose(
        laser.vendor_2025_torsion_mm(v, b, s), ch["torsion_proxy_mm"] / 2.0
    )  # vendor formula is exactly half
    assert np.allclose(ch["pitch_rad"], 27.0 / 130.0)


def test_stats_ddof1_and_peak():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    m, rms, pk = laser.stats(x)
    assert m == 2.5 and abs(rms - np.std(x, ddof=1)) < 1e-12 and pk == 1.5


def test_free_vibration_fit_recovers_known_values():
    fs, f, zeta = laser.FS, 1.4358, 0.004
    t = np.arange(0, 60, 1 / fs)
    x = 3.0 * np.exp(-zeta * 2 * np.pi * f * t) * np.cos(2 * np.pi * f * t + 0.3)
    x = x + np.random.default_rng(1).normal(0, 0.02, len(t))
    r = laser.fit_damped(x, fs, n_boot=60)
    assert abs(r["f_fit_hz"] - f) < 1e-3 and abs(r["zeta"] - zeta) / zeta < 0.05
