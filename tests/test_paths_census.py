import numpy as np
import pytest

from bridgedeck import census, paths


def test_paths_resolve():
    cfg = paths.load()
    assert "${phd_root}" not in str(cfg)
    assert cfg["bags"]["wtt_main"].endswith("raw/wtt-main")


def test_write_guard():
    with pytest.raises(PermissionError):
        paths.assert_not_input(paths.load()["bags"]["wtt_main"] + "/x.txt")


def test_summarize_detects_duplicate_and_rate():
    n = 600
    h = (np.arange(n) * 16_683_333).astype(np.int64) + 10**18
    k = np.arange(n, dtype=np.uint32)
    k[300] = k[299]
    d = dict(h=h, r=h + 9_000_000, s=np.arange(n), n=np.full(n, 100), k=k)
    r = census.summarize("t", "b", "cam", d)
    assert abs(r["rate_mean_hz"] - 59.94) < 0.01
    assert r["dup_consecutive_payload"] == 1 and r["seq_missing"] == 0
    assert abs(r["lat_mean_ms"] - 9.0) < 1e-6
