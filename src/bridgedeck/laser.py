"""Stage S5a: laser records from raw, both sessions through ONE code path (gate: docs/gates/S5a.md).

Units: raw columns are volts; (volts - bias) * 2.7 gives centimetres; every output column is named with its unit.
center = column 1, side = column 2; the third column (wind-speed proxy) is never used.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from . import paths

FS = 360.0  # Hz, from the vendor scripts (fs = 360)
PVOLT = 2.7  # cm per volt, both channels, both sessions (vendor scripts)
FREE_CAL = 27.0  # mm per volt in the vendor free-vibration scripts (fq*.m)


@dataclass(frozen=True)
class Session:
    name: str
    dside_cm: float  # centre-to-side sensor spacing
    db_cm: float  # reference half-width used for the torsion proxy
    bias_file: str
    data_dir: str  # key in config laser.*
    sub: str  # sub-directory below data_dir
    map_xlsx: str  # workbook with the file -> RPM table (sheet 'etc')
    free_dir: str

    @property
    def dp(self) -> float:
        return self.db_cm / self.dside_cm


SESSIONS = {
    "y2025": Session(
        "y2025",
        13.0,
        20.0,
        "D00",
        "y2025_raw",
        "등류/영각00",
        "등류/영각00/영상계측_laser_등류_영각00.xlsx",
        "자유진동",
    ),
    "y2024": Session(
        "y2024", 10.0, 20.0, "D0", "y2024_raw", "", "Windspeed.xlsx", "../free_vibration"
    ),
}


def _root(s: Session) -> Path:
    return Path(paths.load()["laser"][s.data_dir]) / s.sub


def mapping(s: Session) -> pd.DataFrame:
    """File -> RPM table from the facility workbook (sheet with header row 'file'/'rpm')."""
    path = Path(paths.load()["laser"][s.data_dir]) / s.map_xlsx
    raw = pd.read_excel(path, sheet_name=0, header=None)
    rows = raw[raw[0].astype(str).str.fullmatch(r"D\d+")].iloc[:, :3]
    rows.columns = ["file", "rpm", "wind_measured_ms"]
    out = rows.reset_index(drop=True)
    out["rpm"] = out["rpm"].astype(float)
    return out


def disk_name(s: Session, label: str) -> str:
    """Workbook label (D01) -> file on disk. 2025 files are zero-padded (D01); 2024 files are not (D1), as loaded by
    the vendor loop `'D' + num2str(i)`. The label and the disk file are the same number (direct mapping)."""
    n = int(label[1:])
    return f"D{n:02d}" if s.name == "y2025" else f"D{n}"


def load_volts(s: Session, name: str) -> np.ndarray:
    return np.loadtxt(_root(s) / name)


def bias(s: Session) -> np.ndarray:
    return load_volts(s, s.bias_file).mean(axis=0)[:2]


def channels(volts: np.ndarray, b: np.ndarray, s: Session) -> dict[str, np.ndarray]:
    """All reported channels in mm (and radians for pitch) from raw volts."""
    cm = (volts[:, :2] - b) * PVOLT
    mm = cm * 10.0
    center, side = mm[:, 0], mm[:, 1]
    diff = side - center
    return {
        "center_mm": center,
        "side_mm": side,
        "bending_avg_mm": (center + side) / 2.0,
        "torsion_diff_mm": diff,
        "torsion_proxy_mm": diff * s.dp,
        "heave_mm": center,
        "pitch_rad": diff / (s.dside_cm * 10.0),
    }


def vendor_2025_torsion_mm(volts: np.ndarray, b: np.ndarray, s: Session) -> np.ndarray:
    """The 2025 vendor script overwrites column 1 with the average BEFORE computing the difference: (side - center)/2 * dp."""
    cm = (volts[:, :2] - b) * PVOLT
    avg = (cm[:, 0] + cm[:, 1]) / 2.0
    return (cm[:, 1] - avg) * s.dp * 10.0


def stats(x: np.ndarray) -> tuple[float, float, float]:
    """mean, RMS about the mean (ddof=1, as MATLAB std), peak = max|x - mean|."""
    m = float(np.mean(x))
    return m, float(np.std(x, ddof=1)), float(np.max(np.abs(x - m)))


def dominant_freq(
    x: np.ndarray, fs: float = FS, lo: float = 0.5, hi: float = 10.0, pad: int = 8
) -> float:
    x = x - np.mean(x)
    w = np.hanning(len(x))
    n = pad * len(x)
    sp = np.abs(np.fft.rfft(x * w, n))
    f = np.fft.rfftfreq(n, 1 / fs)
    band = (f >= lo) & (f <= hi)
    return float(f[band][np.argmax(sp[band])])


def run_session(name: str) -> pd.DataFrame:
    s = SESSIONS[name]
    b = bias(s)
    rows = []
    for _, r in mapping(s).iterrows():
        if not (
            _root(s) / disk_name(s, r["file"])
        ).exists():  # e.g. workbook rows D39, D40 have no raw file
            print(f"{name}: workbook row {r['file']} ({r['rpm']:.0f} RPM) has no raw file; skipped")
            continue
        v = load_volts(s, disk_name(s, r["file"]))
        ch = channels(v, b, s)
        row = {
            "session": name,
            "file": r["file"],
            "rpm": r["rpm"],
            "wind_measured_ms": r["wind_measured_ms"],
            "n": len(v),
            "duration_s": len(v) / FS,
        }
        for k, x in ch.items():
            m, rms, pk = stats(x)
            row[f"{k}_mean"], row[f"{k}_rms"], row[f"{k}_peak"] = m, rms, pk
        row["bending_dom_hz"] = dominant_freq(ch["bending_avg_mm"])
        row["torsion_dom_hz"] = dominant_freq(ch["torsion_diff_mm"])
        row["vendor2025_torsion_rms_mm"] = (
            stats(vendor_2025_torsion_mm(v, b, s))[1] if name == "y2025" else np.nan
        )
        rows.append(row)
    return pd.DataFrame(rows)


# ---------- free vibration (reference frequencies from raw, D6) ----------


def _segment(x: np.ndarray, fs: float) -> slice:
    w = int(fs)
    sq = np.convolve(x**2, np.ones(w) / w, mode="same")
    rms = np.sqrt(sq)
    i0 = int(np.argmax(rms))
    below = np.where(rms[i0:] < 0.1 * rms[i0])[0]
    i1 = i0 + (int(below[0]) if len(below) else len(x) - i0)
    return slice(i0, i1)


def _damped(t, a, zeta, fd, phi, c):
    return a * np.exp(-zeta * 2 * np.pi * fd * t) * np.cos(2 * np.pi * fd * t + phi) + c


def fit_damped(x: np.ndarray, fs: float, n_boot: int = 500, seed: int = 7) -> dict:
    t = np.arange(len(x)) / fs
    x = x - np.mean(x)
    f0 = dominant_freq(x, fs, 0.5, 10.0, pad=16)
    p0 = [float(np.max(np.abs(x))), 0.005, f0, 0.0, 0.0]
    popt, _ = curve_fit(_damped, t, x, p0=p0, maxfev=20000)
    res = x - _damped(t, *popt)
    out = {
        "f_fft_hz": f0,
        "f_fit_hz": float(popt[2]),
        "zeta": float(popt[1]),
        "amp": float(abs(popt[0])),
        "resid_over_amp": float(np.std(res) / abs(popt[0])),
        "n": len(x),
        "duration_s": len(x) / fs,
    }
    rng = np.random.default_rng(seed)
    bl = int(fs)
    nb = max(len(x) // bl, 1)
    fits = []
    fitted = x - res
    for _ in range(n_boot):
        idx = rng.integers(0, nb, nb)
        r_b = np.concatenate([res[i * bl : (i + 1) * bl] for i in idx])[: len(x)]
        try:
            pb, _ = curve_fit(
                _damped, t[: len(r_b)], fitted[: len(r_b)] + r_b, p0=popt, maxfev=5000
            )
            fits.append((pb[2], pb[1]))
        except RuntimeError:
            continue
    fits = np.array(fits)
    out["f_fit_lo"], out["f_fit_hi"] = (
        (float(np.percentile(fits[:, 0], 2.5)), float(np.percentile(fits[:, 0], 97.5)))
        if len(fits) > 50
        else (np.nan, np.nan)
    )
    out["zeta_lo"], out["zeta_hi"] = (
        (float(np.percentile(fits[:, 1], 2.5)), float(np.percentile(fits[:, 1], 97.5)))
        if len(fits) > 50
        else (np.nan, np.nan)
    )
    out["n_boot_ok"] = len(fits)
    return out


def free_vibration(name: str, mode: str) -> dict:
    s = SESSIONS[name]
    f = Path(paths.load()["laser"][s.data_dir]) / s.free_dir / ("Bd1" if mode == "B" else "Td1")
    v = np.loadtxt(f)[:, :2] * FREE_CAL  # mm
    sig = (v[:, 0] + v[:, 1]) / 2.0 if mode == "B" else (v[:, 1] - v[:, 0])
    sig = sig - np.polyval(np.polyfit(np.arange(len(sig)), sig, 1), np.arange(len(sig)))
    seg = _segment(sig, FS)
    out = fit_damped(sig[seg], FS)
    out.update(
        session=name,
        mode="bending" if mode == "B" else "torsion",
        seg_start_s=seg.start / FS,
        seg_end_s=seg.stop / FS,
        file=str(f),
    )
    return out
