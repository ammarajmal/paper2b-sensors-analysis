#!/usr/bin/env python3
"""Condition-level statistical package for Paper 2B exploratory evidence.

The script consumes only the existing exploratory derived tables.  It writes
all package artifacts below its own directory and never edits manuscript,
canonical, raw, or pre-existing audit files.
"""

from __future__ import annotations

import hashlib
import platform
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PLOTS = OUT / "plots"
SEED = 0
B = 10_000
RPM_ALL = [
    20,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
    110,
    120,
    140,
    160,
    180,
    200,
    220,
    240,
    260,
    280,
    300,
    320,
]
RPM_FREQ = RPM_ALL[:-1]

INPUTS = {
    "stream_table": ROOT / "results/s2c_stream_table_dev.csv",
    "frequency_matches": ROOT
    / "analysis/paper2b/exploratory/EXPLORATORY_CAMERA_LASER_FREQUENCY_MATCHES.csv",
    "rms_comparison": ROOT
    / "analysis/paper2b/exploratory/EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv",
    "spectral_shape": ROOT / "analysis/paper2b/exploratory/EXPLORATORY_WAVEFORM_SPECTRAL_SHAPE.csv",
    "spatial_response": ROOT
    / "analysis/paper2b/exploratory/EXPLORATORY_APPARENT_SPATIAL_RESPONSE.csv",
    "forced_alignment": ROOT
    / "analysis/paper2b/exploratory/forced_alignment/FORCED_ALIGNMENT_WAVEFORM_RESULTS.csv",
    "source_hashes": ROOT / "analysis/paper2b/exploratory/EXPLORATORY_SOURCE_HASHES.json",
    "forced_source_hashes": ROOT
    / "analysis/paper2b/exploratory/forced_alignment/FORCED_ALIGNMENT_SOURCE_HASHES.json",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def q(x: np.ndarray) -> float:
    return float(np.quantile(x, 0.25))


def iqr(x: np.ndarray) -> float:
    return float(np.quantile(x, 0.75) - np.quantile(x, 0.25))


def safe_corr(x: np.ndarray, y: np.ndarray, method: str) -> float:
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    if method == "pearson":
        return float(stats.pearsonr(x, y).statistic)
    return float(stats.spearmanr(x, y).statistic)


def robust_corr(x: np.ndarray, y: np.ndarray) -> float:
    """Winsorized Pearson correlation; descriptive, not a model-based test."""

    def winsor(a):
        med = np.median(a)
        mad = np.median(np.abs(a - med))
        if mad == 0:
            return a
        return np.clip(a, med - 3 * 1.4826 * mad, med + 3 * 1.4826 * mad)

    return safe_corr(winsor(x), winsor(y), "pearson")


def boot(values: np.ndarray, fn, rng: np.random.Generator) -> tuple[float, float, float]:
    values = np.asarray(values)
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    observed = float(fn(values))
    idx = rng.integers(0, len(values), size=(B, len(values)))
    samples = np.asarray([fn(values[i]) for i in idx], dtype=float)
    return observed, float(np.nanquantile(samples, 0.025)), float(np.nanquantile(samples, 0.975))


def paired_boot(x, y, fn, rng):
    pairs = np.column_stack([x, y])
    observed = float(fn(pairs[:, 0], pairs[:, 1]))
    idx = rng.integers(0, len(pairs), size=(B, len(pairs)))
    vals = np.asarray([fn(pairs[sample_idx, 0], pairs[sample_idx, 1]) for sample_idx in idx], float)
    return observed, float(np.nanquantile(vals, 0.025)), float(np.nanquantile(vals, 0.975))


def scope_mask(df, scope: str) -> pd.Series:
    if scope == "full_20":
        return pd.Series(True, index=df.index)
    if scope == "non_320":
        return df.rpm < 320
    if scope == "non_320_excl_60_80":
        return (df.rpm < 320) & ~df.rpm.isin([60, 80])
    raise ValueError(scope)


def row(**kwargs):
    return kwargs


STREAM_CLASSES = ["admissible", "rejected", "diagnostic-only"]
STREAM_EXPECTED = {"total": 63, "admissible": 60, "rejected": 2, "diagnostic-only": 1}


def classify_stream(condition: str, camera: str) -> str:
    """Stream class from the project evidence boundary, independent of the ledger column."""
    if condition == "e20_320rpm":
        return "diagnostic-only" if camera == "cam3" else "rejected"
    return "admissible"


def stream_inventory(streams: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Classify the canonical 63-stream table and validate it against the boundary."""
    streams = streams.copy()
    streams["stream_class"] = [
        classify_stream(c, cam) for c, cam in zip(streams.condition, streams.camera)
    ]
    streams["camera_laser_matched"] = streams.condition != "e0_0rpm"
    ledger = streams.ledger.replace({"diagnostic": "diagnostic-only"})
    if not (ledger == streams.stream_class).all():
        bad = streams[ledger != streams.stream_class]
        raise ValueError(f"stream ledger disagrees with evidence boundary:\n{bad}")
    counts = streams.stream_class.value_counts().to_dict()
    observed = {"total": len(streams), **{k: counts.get(k, 0) for k in STREAM_CLASSES}}
    if observed != STREAM_EXPECTED:
        raise ValueError(f"stream inventory {observed} != expected {STREAM_EXPECTED}")
    zero = streams[streams.condition == "e0_0rpm"]
    if len(zero) != 3 or not (zero.stream_class == "admissible").all():
        raise ValueError("e0_0rpm must be three camera-only admissible streams")
    validation = pd.DataFrame(
        [
            row(
                quantity=k,
                observed=observed[k],
                expected=STREAM_EXPECTED[k],
                passed=observed[k] == STREAM_EXPECTED[k],
                source="results/s2c_stream_table_dev.csv",
            )
            for k in STREAM_EXPECTED
        ]
        + [
            row(
                quantity="camera_only_0rpm_streams",
                observed=len(zero),
                expected=3,
                passed=True,
                source="e0_0rpm cam1/cam2/cam3: in inventory, no matched laser",
            ),
            row(
                quantity="camera_laser_matched_streams",
                observed=int(streams.camera_laser_matched.sum()),
                expected=60,
                passed=int(streams.camera_laser_matched.sum()) == 60,
                source="63 minus 3 camera-only 0 RPM streams; still includes 320 RPM",
            ),
        ]
    )
    return streams, validation


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PLOTS.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    freq = pd.read_csv(INPUTS["frequency_matches"])
    rms = pd.read_csv(INPUTS["rms_comparison"])
    shape = pd.read_csv(INPUTS["spectral_shape"])
    spatial = pd.read_csv(INPUTS["spatial_response"])
    forced = pd.read_csv(INPUTS["forced_alignment"])
    for d in [freq, rms, shape, spatial, forced]:
        d["rpm"] = d["rpm"].astype(int)
    streams, stream_validation = stream_inventory(pd.read_csv(INPUTS["stream_table"]))
    stream_validation.to_csv(OUT / "STREAM_INVENTORY_VALIDATION.csv", index=False)
    stream_counts = {k: int((streams.stream_class == k).sum()) for k in STREAM_CLASSES}

    source_manifest = {}
    for name, p in INPUTS.items():
        if p.suffix == ".json":
            source_manifest[str(p)] = sha(p)
    for p in INPUTS.values():
        if p.suffix != ".json":
            source_manifest[str(p)] = sha(p)
    (OUT / "STATISTICAL_SOURCE_HASHES.sha256").write_text(
        "".join(f"{v}  {k}\n" for k, v in sorted(source_manifest.items()))
    )

    # A: nearest retained camera peak correspondence.  The 20-condition laser
    # domain is explicit, while 320 RPM is excluded from inferential frequency
    # summaries because cam1/cam2 are rejected and cam3 is diagnostic-only.
    fr = []
    for target in ["bend", "torsion"]:
        for cam_scope, cams in [
            ("cam1", ["cam1"]),
            ("cam2", ["cam2"]),
            ("cam1_cam2_pooled", ["cam1", "cam2"]),
            ("cam3", ["cam3"]),
            ("all_cameras", ["cam1", "cam2", "cam3"]),
        ]:
            for scope in ["non_320", "non_320_excl_60_80"]:
                g = freq[
                    (freq.laser_target == target)
                    & freq.camera.isin(cams)
                    & (freq.admissibility == "admissible")
                    & scope_mask(freq, scope)
                ]
                if not len(g):
                    continue
                x = g.signed_error_hz.to_numpy(float)
                a = np.abs(x)
                ray = g.error_rayleigh.to_numpy(float)
                _, lo_med, hi_med = boot(a, np.median, rng)
                fr.append(
                    row(
                        analysis="frequency_correspondence",
                        target=target,
                        camera_scope=cam_scope,
                        subset=scope,
                        n_conditions=int(g.rpm.nunique()),
                        n_condition_camera_rows=len(g),
                        denominator=len(g),
                        mean_signed_hz=float(x.mean()),
                        median_signed_hz=float(np.median(x)),
                        mean_abs_hz=float(a.mean()),
                        median_abs_hz=float(np.median(a)),
                        iqr_abs_hz=iqr(a),
                        rmse_hz=float(np.sqrt(np.mean(x * x))),
                        p90_abs_hz=float(np.quantile(a, 0.9)),
                        within_0_1_fraction=float(np.mean(a <= 0.1)),
                        within_one_rayleigh_fraction=float(np.mean(ray <= 1)),
                        median_abs_boot_lo=lo_med,
                        median_abs_boot_hi=hi_med,
                        method="nearest of five retained peaks; condition-level bootstrap",
                        bootstrap_seed=SEED,
                        exclusions="320 RPM: cam1/cam2 rejected; cam3 diagnostic-only",
                        evidence="exploratory cross-session operational correspondence",
                        interpretation="not modal-frequency accuracy; not simultaneous validation",
                    )
                )
    pd.DataFrame(fr).to_csv(OUT / "FREQUENCY_CORRESPONDENCE_RESULTS.csv", index=False)

    # B: common-unit RMS scaling. The source has one pooled camera summary per
    # condition; retain that limitation explicitly and do not derive cam3 mm.
    rs = []
    for metric, cx, ly, ratio in [
        ("bending", "camera_bend_rms_mm", "laser_bend_rms_mm", "bend_ratio"),
        ("torsion", "camera_torsion_rms_mm", "laser_torsion_rms_mm", "torsion_ratio"),
    ]:
        for scope in ["full_20", "non_320", "non_320_excl_60_80"]:
            g = rms[scope_mask(rms, scope)].copy()
            x = g[cx].to_numpy(float)
            y = g[ly].to_numpy(float)
            r = g[ratio].to_numpy(float)
            pr = safe_corr(x, y, "pearson")
            sp = safe_corr(x, y, "spearman")
            rc = robust_corr(x, y)
            slope, intercept, rr, pval, stderr = stats.linregress(y, x)
            _, slo, shi = paired_boot(y, x, lambda a, b: stats.linregress(a, b).slope, rng)
            _, cro, crhi = paired_boot(x, y, lambda a, b: safe_corr(a, b, "pearson"), rng)
            rs.append(
                row(
                    analysis="rms_response_scaling",
                    metric=metric,
                    camera_scope="pooled_camera_source",
                    subset=scope,
                    n_conditions=len(g),
                    denominator=len(g),
                    pearson_r=pr,
                    spearman_r=sp,
                    robust_winsorized_r=rc,
                    rmse_mm=float(np.sqrt(np.mean((x - y) ** 2))),
                    mean_ratio=float(r.mean()),
                    median_ratio=float(np.median(r)),
                    ratio_iqr=iqr(r),
                    regression_slope=float(slope),
                    regression_intercept_mm=float(intercept),
                    r_squared=float(rr * rr),
                    slope_boot_lo=slo,
                    slope_boot_hi=shi,
                    pearson_boot_lo=cro,
                    pearson_boot_hi=crhi,
                    residual_mean_mm=float(np.mean(x - (intercept + slope * y))),
                    residual_sd_mm=float(np.std(x - (intercept + slope * y), ddof=1)),
                    method="condition-level paired RMS; descriptive regression",
                    bootstrap_seed=SEED,
                    exclusions="none"
                    if scope == "full_20"
                    else ("320 RPM" if scope == "non_320" else "320, 60, 80 RPM"),
                    evidence="exploratory cross-session response-trend correspondence",
                    interpretation="not calibration or accuracy; source does not provide camera-specific common-unit RMS for cam3",
                )
            )
    # Explicit non-computable scope prevents a reader from mistaking pooled RMS for cam3.
    rs.append(
        row(
            analysis="rms_response_scaling",
            metric="bending_and_torsion",
            camera_scope="with_cam3_separate",
            subset="all_requested_scopes",
            n_conditions=0,
            denominator=0,
            pearson_r=np.nan,
            spearman_r=np.nan,
            robust_winsorized_r=np.nan,
            rmse_mm=np.nan,
            mean_ratio=np.nan,
            median_ratio=np.nan,
            ratio_iqr=np.nan,
            regression_slope=np.nan,
            regression_intercept_mm=np.nan,
            r_squared=np.nan,
            slope_boot_lo=np.nan,
            slope_boot_hi=np.nan,
            pearson_boot_lo=np.nan,
            pearson_boot_hi=np.nan,
            residual_mean_mm=np.nan,
            residual_sd_mm=np.nan,
            method="not estimable from available source schema",
            bootstrap_seed=SEED,
            exclusions="camera-specific cam3 common-unit RMS absent",
            evidence="schema limitation",
            interpretation="do not infer cam3 laser scaling",
        )
    )
    pd.DataFrame(rs).to_csv(OUT / "RMS_SCALING_RESULTS.csv", index=False)

    # C: same-marker repeatability, condition-level cam1/cam2 pairs.
    piv = shape[shape.rpm < 320].pivot(
        index="rpm", columns="camera", values=["camera_peak_hz", "camera_centroid_y_rms_px"]
    )
    rep = []
    for scope, mask in [
        ("non_320", np.ones(len(piv), bool)),
        ("non_320_excl_60_80", ~piv.index.isin([60, 80])),
    ]:
        p = piv.loc[mask]
        fd = (p[("camera_peak_hz", "cam1")] - p[("camera_peak_hz", "cam2")]).to_numpy(float)
        ad = np.abs(fd)
        rr = p[("camera_centroid_y_rms_px", "cam1")].to_numpy(float) / p[
            ("camera_centroid_y_rms_px", "cam2")
        ].to_numpy(float)
        rel = (
            2
            * (
                p[("camera_centroid_y_rms_px", "cam1")] - p[("camera_centroid_y_rms_px", "cam2")]
            ).to_numpy(float)
            / (
                p[("camera_centroid_y_rms_px", "cam1")] + p[("camera_centroid_y_rms_px", "cam2")]
            ).to_numpy(float)
        )
        _, dlo, dhi = boot(ad, np.median, rng)
        _, rlo, rhi = boot(rr, np.median, rng)
        perm = stats.permutation_test(
            (fd,),
            lambda z: np.mean(np.abs(z)),
            permutation_type="samples",
            n_resamples=B,
            random_state=SEED,
        ).pvalue
        rep.append(
            row(
                analysis="same_marker_repeatability",
                camera_scope="cam1_vs_cam2",
                subset=scope,
                n_conditions=len(p),
                denominator=len(p),
                median_frequency_difference_hz=float(np.median(fd)),
                mean_frequency_difference_hz=float(np.mean(fd)),
                iqr_abs_frequency_difference_hz=iqr(ad),
                median_abs_frequency_difference_hz=float(np.median(ad)),
                abs_frequency_boot_lo=dlo,
                abs_frequency_boot_hi=dhi,
                median_rms_ratio=float(np.median(rr)),
                mean_rms_ratio=float(np.mean(rr)),
                rms_ratio_iqr=iqr(rr),
                rms_ratio_boot_lo=rlo,
                rms_ratio_boot_hi=rhi,
                mean_relative_difference=float(np.mean(rel)),
                paired_permutation_p=float(perm),
                method="paired condition-level bootstrap and permutation",
                bootstrap_seed=SEED,
                exclusions="320 RPM rejected cam1/cam2"
                if scope == "non_320"
                else "320, 60, 80 RPM",
                evidence="same-marker repeatability",
                interpretation="not external accuracy",
            )
        )
    pd.DataFrame(rep).to_csv(OUT / "REPEATABILITY_RESULTS.csv", index=False)

    # D: cam3 observation-path dependence.
    sp = spatial[spatial.rpm < 320].copy()
    sp["same_marker_mean"] = (sp.cam1 + sp.cam2) / 2
    sp["cam3_relative"] = sp.cam3 / sp.same_marker_mean
    obs = []
    for scope in ["non_320", "non_320_excl_60_80"]:
        g = sp[scope_mask(sp, scope)]
        d = g.cam3_relative.to_numpy(float)
        freq_d = (
            (
                shape[(shape.camera == "cam3") & (shape.rpm < 320)].set_index("rpm").camera_peak_hz
                - shape[(shape.camera == "cam1") & (shape.rpm < 320)]
                .set_index("rpm")
                .camera_peak_hz
            )
            .reindex(g.rpm)
            .to_numpy(float)
        )
        _, dlo, dhi = boot(d, np.median, rng)
        obs.append(
            row(
                analysis="observation_path_dependence",
                camera_scope="cam3_vs_cam1_cam2_mean",
                subset=scope,
                n_conditions=len(g),
                denominator=len(g),
                median_relative_rms=float(np.median(d)),
                mean_relative_rms=float(np.mean(d)),
                relative_rms_iqr=iqr(d),
                relative_rms_boot_lo=dlo,
                relative_rms_boot_hi=dhi,
                median_frequency_difference_hz=float(np.median(freq_d)),
                mean_frequency_difference_hz=float(np.mean(freq_d)),
                method="condition-level ratios and paired frequency differences",
                bootstrap_seed=SEED,
                exclusions="320 RPM diagnostic-only" if scope == "non_320" else "320, 60, 80 RPM",
                evidence="observation-path dependence",
                interpretation="not unique torsional mode, marker-location effect, or modal shape",
            )
        )
    pd.DataFrame(obs).to_csv(OUT / "STATISTICAL_COMPARISONS.csv", index=False)

    # E: corrected forced alignment diagnostics copied with explicit provenance.
    fa = forced[(forced.admissibility == "admissible")].copy()
    fa["scope"] = "non_320"
    fa.loc[fa.rpm.isin([60, 80]), "scope"] = "non_320_including_60_80"
    faout = []
    for _, r in fa.iterrows():
        faout.append(
            row(
                analysis="forced_alignment_stress_test",
                **r.to_dict(),
                method="60% lag estimation, fixed lag on 40% held-out; interpolated common mathematical grid",
                bootstrap_seed=SEED,
                interpretation="mathematical forced alignment, not physical shared-clock recovery",
            )
        )
    faout = pd.DataFrame(faout)
    # Keep one rectangular comparison file while retaining separate analysis
    # namespaces; missing columns are intentional for different estimands.
    pd.concat([pd.DataFrame(obs), faout], ignore_index=True, sort=False).to_csv(
        OUT / "STATISTICAL_COMPARISONS.csv", index=False
    )

    # F: leave-one-condition-out for every primary RMS correlation.
    loo = []
    for metric, cx, ly in [
        ("bending", "camera_bend_rms_mm", "laser_bend_rms_mm"),
        ("torsion", "camera_torsion_rms_mm", "laser_torsion_rms_mm"),
    ]:
        for scope in ["full_20", "non_320", "non_320_excl_60_80"]:
            g = rms[scope_mask(rms, scope)].reset_index(drop=True)
            vals = []
            for i in range(len(g)):
                h = g.drop(index=i)
                vals.append(
                    row(
                        analysis="leave_one_condition_out",
                        metric=metric,
                        subset=scope,
                        removed_rpm=int(g.loc[i, "rpm"]),
                        denominator=len(h),
                        pearson_r=safe_corr(
                            h[cx].to_numpy(float), h[ly].to_numpy(float), "pearson"
                        ),
                        spearman_r=safe_corr(
                            h[cx].to_numpy(float), h[ly].to_numpy(float), "spearman"
                        ),
                    )
                )
            loo.extend(vals)
            for method in ["pearson_r", "spearman_r"]:
                z = np.array([v[method] for v in vals], float)
                best = vals[int(np.nanargmax(z))]["removed_rpm"]
                worst = vals[int(np.nanargmin(z))]["removed_rpm"]
                loo.append(
                    row(
                        analysis="leave_one_condition_out_summary",
                        metric=metric,
                        subset=scope,
                        removed_rpm="SUMMARY",
                        denominator=len(g) - 1,
                        min_correlation=float(np.nanmin(z)),
                        median_correlation=float(np.nanmedian(z)),
                        max_correlation=float(np.nanmax(z)),
                        correlation_type=method,
                        max_after_removing_rpm=best,
                        min_after_removing_rpm=worst,
                        influential_rpms="60,70,80,300,320 inspected",
                        interpretation="influence diagnostic; no causal inference",
                    )
                )
    pd.DataFrame(loo).to_csv(OUT / "LEAVE_ONE_CONDITION_OUT.csv", index=False)

    # A compact bootstrap ledger makes method/seed/estimand provenance easy to
    # audit without reverse-engineering the wider result tables.
    boot_rows = []
    for r in fr:
        boot_rows.append(
            row(
                analysis=r["analysis"],
                metric=f"{r['target']}:median_abs_hz",
                camera_scope=r["camera_scope"],
                subset=r["subset"],
                denominator=r["denominator"],
                estimate=r["median_abs_hz"],
                ci_low=r["median_abs_boot_lo"],
                ci_high=r["median_abs_boot_hi"],
                resamples=B,
                seed=SEED,
                unit="condition-camera-target",
            )
        )
    for r in rs:
        if r.get("denominator", 0):
            boot_rows.append(
                row(
                    analysis=r["analysis"],
                    metric=f"{r['metric']}:pearson_r",
                    camera_scope=r["camera_scope"],
                    subset=r["subset"],
                    denominator=r["denominator"],
                    estimate=r["pearson_r"],
                    ci_low=r["pearson_boot_lo"],
                    ci_high=r["pearson_boot_hi"],
                    resamples=B,
                    seed=SEED,
                    unit="condition",
                )
            )
            boot_rows.append(
                row(
                    analysis=r["analysis"],
                    metric=f"{r['metric']}:slope",
                    camera_scope=r["camera_scope"],
                    subset=r["subset"],
                    denominator=r["denominator"],
                    estimate=r["regression_slope"],
                    ci_low=r["slope_boot_lo"],
                    ci_high=r["slope_boot_hi"],
                    resamples=B,
                    seed=SEED,
                    unit="condition",
                )
            )
    for r in rep:
        boot_rows.append(
            row(
                analysis=r["analysis"],
                metric="median_abs_frequency_difference_hz",
                camera_scope=r["camera_scope"],
                subset=r["subset"],
                denominator=r["denominator"],
                estimate=r["median_abs_frequency_difference_hz"],
                ci_low=r["abs_frequency_boot_lo"],
                ci_high=r["abs_frequency_boot_hi"],
                resamples=B,
                seed=SEED,
                unit="paired condition",
            )
        )
    for r in obs:
        boot_rows.append(
            row(
                analysis=r["analysis"],
                metric="median_relative_rms",
                camera_scope=r["camera_scope"],
                subset=r["subset"],
                denominator=r["denominator"],
                estimate=r["median_relative_rms"],
                ci_low=r["relative_rms_boot_lo"],
                ci_high=r["relative_rms_boot_hi"],
                resamples=B,
                seed=SEED,
                unit="condition",
            )
        )
    pd.DataFrame(boot_rows).to_csv(OUT / "BOOTSTRAP_RESULTS.csv", index=False)
    claims = [
        [
            "C01",
            "same-marker repeatability",
            "PERMITTED",
            "cam1/cam2 paired condition-level frequency and pixel-RMS similarity",
            "REPEATABILITY_RESULTS.csv",
            "not accuracy",
        ],
        [
            "C02",
            "operational frequency correspondence",
            "PERMITTED",
            "camera and laser condition-level frequency differences",
            "FREQUENCY_CORRESPONDENCE_RESULTS.csv",
            "not modal-frequency accuracy or simultaneous validation",
        ],
        [
            "C03",
            "response-trend correspondence",
            "PERMITTED",
            "pooled camera/laser RMS correlations and ratios",
            "RMS_SCALING_RESULTS.csv",
            "not calibration, equality, or causality",
        ],
        [
            "C04",
            "cam3 observation-path dependence",
            "PERMITTED",
            "cam3 relative response versus same-marker mean",
            "STATISTICAL_COMPARISONS.csv",
            "not unique mode or marker-location effect",
        ],
        [
            "C05",
            "mathematical forced-alignment stress test",
            "PERMITTED",
            "held-out diagnostics after 60% lag fitting",
            "STATISTICAL_COMPARISONS.csv",
            "not physical shared-clock recovery or waveform validation",
        ],
        [
            "C06",
            "camera accuracy",
            "PROHIBITED",
            "no simultaneous calibrated common-observable reference",
            "STATISTICAL_RESULTS_REPORT.md",
            "unresolved",
        ],
        [
            "C07",
            "structural modal identification",
            "PROHIBITED",
            "dominant frequency and observation paths are insufficient",
            "STATISTICAL_RESULTS_REPORT.md",
            "unresolved",
        ],
    ]
    pd.DataFrame(
        claims, columns=["claim_id", "claim", "status", "evidence_basis", "artifact", "restriction"]
    ).to_csv(OUT / "STATISTICAL_CLAIM_LEDGER.csv", index=False)
    make_plots(freq, rms, piv, sp, fa, pd.DataFrame(loo))
    write_plan()
    write_report(fr, rs, rep, obs, fa, loo)
    runtime = [
        f"python={sys.version}",
        f"platform={platform.platform()}",
        f"numpy={np.__version__}",
        f"pandas={pd.__version__}",
        f"scipy={stats.__version__ if hasattr(stats, '__version__') else 'installed'}",
        "matplotlib=installed",
        f"statsmodels={statsmodels.__version__}",
        f"bootstrap_resamples={B}",
        f"bootstrap_seed={SEED}",
        f"matched_laser_conditions={len(RPM_ALL)}",
        f"frequency_conditions={len(RPM_FREQ)}",
        f"camera_stream_rows={len(streams)}",
        f"admissibility_counts={stream_counts}",
        f"spectral_shape_input_rows={len(shape)} (camera-laser matched streams only; excludes camera-only 0 RPM)",
        f"camera_laser_frequency_conditions_per_camera={len(RPM_FREQ)}",
        f"frequency_condition_camera_target_rows={len(freq[freq.admissibility == 'admissible'])}",
        "units=condition; no frame-level inferential tests",
        "forced_alignment=corrected source; obsolete r_test=-0.118 not used",
    ]
    (OUT / "STATISTICAL_RUNTIME.txt").write_text("\n".join(runtime) + "\n")


def make_plots(freq, rms, piv, sp, fa, loo):
    def save(name):
        plt.tight_layout()
        plt.savefig(PLOTS / name, dpi=170)
        plt.close()

    # 1 frequency
    fig, ax = plt.subplots(figsize=(9, 5))
    g = freq[
        (freq.laser_target == "bend") & (freq.admissibility == "admissible") & (freq.rpm < 320)
    ]
    for cam, c in [("cam1", "C0"), ("cam2", "C1"), ("cam3", "C2")]:
        ax.scatter(
            g[g.camera == cam].rpm,
            g[g.camera == cam].camera_best_frequency_hz,
            label=cam,
            s=18,
            c=c,
        )
    ax.set(
        xlabel="RPM",
        ylabel="Camera matched frequency (Hz)",
        title="Operational frequency correspondence; n=19 conditions/camera; 320 RPM excluded",
    )
    ax.legend()
    save("01_frequency_by_rpm.png")
    # 2 rms
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(rms.rpm, rms.camera_bend_rms_mm, "o-", label="camera pooled")
    ax.plot(rms.rpm, rms.laser_bend_rms_mm, "s-", label="laser")
    ax.set(
        xlabel="RPM",
        ylabel="Bending RMS displacement (mm)",
        title="Condition-level RMS response; full n=20",
    )
    ax.legend()
    save("02_rms_by_rpm.png")
    # 3 regressions
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for ax, mask, label in [
        (axs[0], np.ones(len(rms), bool), "full n=20"),
        (axs[1], (rms.rpm < 320) & ~rms.rpm.isin([60, 80]), "sensitivity n=17"),
    ]:
        g = rms[mask]
        ax.scatter(g.laser_bend_rms_mm, g.camera_bend_rms_mm)
        slope, inter, *_ = stats.linregress(g.laser_bend_rms_mm, g.camera_bend_rms_mm)
        xx = np.linspace(g.laser_bend_rms_mm.min(), g.laser_bend_rms_mm.max(), 40)
        ax.plot(xx, inter + slope * xx)
        ax.set(
            xlabel="Laser bending RMS (mm)", ylabel="Camera pooled bending RMS (mm)", title=label
        )
    save("03_full_vs_sensitivity_regression.png")
    # 4 frequency difference
    fig, ax = plt.subplots(figsize=(8, 4))
    d = piv[("camera_peak_hz", "cam1")] - piv[("camera_peak_hz", "cam2")]
    ax.hist(d, bins=10)
    ax.set(
        xlabel="Cam1 − cam2 dominant frequency (Hz)",
        ylabel="Conditions (n=19)",
        title="Same-marker repeatability",
    )
    save("04_cam1_cam2_frequency_difference.png")
    # 5 ratio
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(
        piv.index,
        piv[("camera_centroid_y_rms_px", "cam1")] / piv[("camera_centroid_y_rms_px", "cam2")],
        "o-",
    )
    ax.axhline(1, color="k", ls="--")
    ax.set(
        xlabel="RPM",
        ylabel="Cam1 / cam2 RMS ratio (pixel units)",
        title="Same-marker RMS ratio; n=19; 320 RPM excluded",
    )
    save("05_cam1_cam2_rms_ratio.png")
    # 6 cam3
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(sp.rpm, sp.cam3_to_same_marker_mean_ratio, "o-")
    ax.axhline(1, color="k", ls="--")
    ax.set(
        xlabel="RPM",
        ylabel="Cam3 / (cam1+cam2)/2 RMS ratio",
        title="Cam3 observation-path dependence; n=19; 320 RPM excluded",
    )
    save("06_cam3_relative_response.png")
    # 7 loo
    fig, ax = plt.subplots(figsize=(9, 4))
    g = loo[
        (loo.analysis == "leave_one_condition_out")
        & (loo.metric == "bending")
        & (loo.subset == "non_320")
    ]
    ax.plot(g.removed_rpm, g.pearson_r, "o-", label="Pearson")
    ax.plot(g.removed_rpm, g.spearman_r, "s-", label="Spearman")
    ax.set(
        xlabel="Removed RPM condition",
        ylabel="Correlation",
        title="Leave-one-condition-out; bending non-320 n=19",
    )
    ax.legend()
    save("07_leave_one_out_range.png")
    # 8 forced
    fig, ax = plt.subplots(figsize=(7, 5))
    g = fa[(fa.target == "bending") & (fa.camera == "cam1")]
    ax.scatter(g.train_corr, g.test_corr)
    ax.axline((0, 0), slope=1, color="k", ls="--")
    ax.set(
        xlabel="Training correlation (60%)",
        ylabel="Held-out correlation (40%)",
        title="Forced-alignment stress test; cam1 bending; n=19",
    )
    save("08_forced_alignment_train_heldout.png")
    # 9 rayleigh
    fig, ax = plt.subplots(figsize=(8, 4))
    g = freq[(freq.admissibility == "admissible") & (freq.rpm < 320)]
    ax.hist(g.error_rayleigh, bins=20)
    ax.axvline(1, color="k", ls="--")
    ax.set(
        xlabel="Absolute frequency error / Rayleigh interval",
        ylabel="Condition-camera-target rows (n=114)",
        title="Frequency error relative to Rayleigh resolution",
    )
    save("09_frequency_error_rayleigh.png")
    # 10 ratios/error bars
    fig, ax = plt.subplots(figsize=(9, 4))
    g = rms[rms.rpm < 320]
    ax.errorbar(g.rpm, g.bend_ratio, yerr=0, fmt="o", label="bending ratio")
    ax.errorbar(g.rpm, g.torsion_ratio, yerr=0, fmt="s", label="torsion ratio")
    ax.axhline(1, color="k", ls="--")
    ax.set(
        xlabel="RPM",
        ylabel="Camera pooled / laser RMS ratio",
        title="Condition-level ratios; n=19; 320 RPM excluded",
    )
    ax.legend()
    save("10_ratio_summary.png")
    captions = """# Statistical plot captions\n\nAll plots use condition-level units drawn from the 60 camera-laser matched streams (the 63-stream inventory minus three camera-only 0 RPM streams; see `STREAM_INVENTORY_VALIDATION.csv`). Frequency and RMS comparisons are cross-session operational correspondence, not accuracy or simultaneous validation.\n\n1. `01_frequency_by_rpm.png`: Camera frequency selected by the existing nearest-retained-peak rule against RPM for the laser bending target; 19 non-320 admissible conditions per camera.\n2. `02_rms_by_rpm.png`: Pooled camera and laser bending RMS values in millimetres across all 20 matched RPM conditions.\n3. `03_full_vs_sensitivity_regression.png`: Descriptive camera-on-laser regression for the full 20-condition set and predeclared sensitivity subset excluding 320, 60, and 80 RPM.\n4. `04_cam1_cam2_frequency_difference.png`: Same-marker cam1 minus cam2 dominant-frequency differences for 19 non-320 conditions.\n5. `05_cam1_cam2_rms_ratio.png`: Cam1/cam2 pixel-RMS ratio by RPM for 19 non-320 conditions.\n6. `06_cam3_relative_response.png`: Cam3 RMS relative to the same-marker cam1/cam2 mean; observation-path dependence only.\n7. `07_leave_one_out_range.png`: Correlations after removing each non-320 condition; no frame-level replication.\n8. `08_forced_alignment_train_heldout.png`: Corrected mathematical forced-alignment training versus held-out correlation; not physical clock recovery.\n9. `09_frequency_error_rayleigh.png`: Absolute frequency error in Rayleigh intervals; Rayleigh resolution is not estimator uncertainty.\n10. `10_ratio_summary.png`: Condition-level camera/laser RMS ratios; the pooled source lacks camera-specific cam3 common-unit RMS.\n"""
    (PLOTS / "FIGURE_CAPTIONS.md").write_text(captions)


def write_plan():
    (OUT / "STATISTICAL_ANALYSIS_PLAN.md").write_text(
        """# Paper 2B Statistical Analysis Plan\n\n## Scope\n\nThis is a separate, evidence-first, condition-level statistical package. It does not edit the manuscript, supplement, frozen outputs, raw bags, canonical source files, or existing audit outputs.\n\n## Units and domains\n\nMatched RPM condition is the unit for camera–laser comparisons; condition-camera stream is the unit for camera spectral results; cam1/cam2 same-marker condition pair is the unit for repeatability. The laser domain contains 20 RPM conditions (20–320 RPM). Camera frequency summaries use 19 admissible non-320 conditions because cam1/cam2 at 320 RPM are rejected and cam3 is diagnostic-only. RMS pooled camera/laser values are available for all 20 conditions. The complete camera inventory is 63 streams (60 admissible, 2 rejected, 1 diagnostic-only), including three camera-only 0 RPM streams that have no matched laser condition and are excluded from every camera–laser comparison.\n\n## Estimands\n\nFrequency correspondence reports signed and absolute error, median, mean, IQR, RMSE, 90th percentile, 0.1 Hz and Rayleigh fractions. RMS scaling reports Pearson, Spearman, robust winsorized Pearson, RMSE in available mm units, ratios, descriptive regression, residuals, and full-before-sensitivity subsets. Repeatability reports paired frequency differences, pixel-RMS ratios, relative differences, bootstrap intervals, and a paired permutation test. Cam3 is retained as observation-path dependence.\n\n## Resampling and tests\n\nAll bootstrap resampling is at the complete-condition level, with 10,000 percentile resamples and fixed seed 0. Leave-one-condition-out results are reported for each RMS correlation. No frame-level hypothesis tests are performed. statsmodels is installed in the project environment; no network access is used.\n\n## Forced alignment\n\nThe corrected pre-existing forced-alignment outputs are reused: lag estimated on the first 60%, applied to the last 40%, with interpolation onto a common mathematical grid. Training/held-out correlation, standardized RMSE, and conditional coherence/phase are diagnostics only. This is mathematical forced alignment, not recovery of a physical shared clock. The obsolete `r_test = -0.118` value is excluded.\n\n## Interpretation restrictions\n\nThese results are operational correspondence, response-trend association, same-marker repeatability, observation-path dependence, and processing sensitivity. They do not establish camera accuracy, calibration, causality, simultaneous validation, synchronization, a unique structural mode, or modal identification.\n"""
    )


def write_report(fr, rs, rep, obs, fa, loo):
    (OUT / "STATISTICAL_RESULTS_REPORT.md").write_text(
        """# Paper 2B Statistical Results Report\n\n**Status:** exploratory, evidence-bounded, and separate from manuscript authority.\n\n## Scope and denominators\n\nThe matched laser domain is exactly 20 RPM conditions. The canonical stream table (`results/s2c_stream_table_dev.csv`) contains 63 condition-camera streams (21 conditions x 3 cameras): 60 admissible, 2 rejected (cam1/cam2 at 320 RPM), and 1 diagnostic-only (cam3 at 320 RPM). The complete camera inventory contains 63 condition-camera streams, including three camera-only 0 RPM streams. Camera–laser correspondence analyses use 19 non-320 matched RPM conditions; 0 RPM streams are not treated as laser-matched observations. The spectral-shape input has 60 rows because it excludes the camera-only 0 RPM streams; it is a matched-analysis input, not the stream inventory (see `STREAM_INVENTORY_VALIDATION.csv`). Frequency correspondence therefore has 19 admissible conditions per camera and 114 condition-camera-target rows across three cameras, two targets, and 19 conditions. RMS response scaling uses the available pooled camera/laser table with 20 conditions; it is not camera-specific for cam1/cam2/cam3.\n\n## Results\n\nThe CSV outputs are the numerical record. Full results precede sensitivity subsets in every table. `FREQUENCY_CORRESPONDENCE_RESULTS.csv` reports operational frequency correspondence, not modal-frequency accuracy. `RMS_SCALING_RESULTS.csv` reports cross-session response-trend association and descriptive regression. `REPEATABILITY_RESULTS.csv` is the strongest basis for a same-marker repeatability claim. `STATISTICAL_COMPARISONS.csv` keeps cam3 separate and contains the corrected forced-alignment diagnostics.\n\nPearson describes linear trend association; Spearman describes monotonic trend association; neither proves equality, calibration, causality, or accuracy. Regression is a cross-campaign response-scaling description, not calibration. RMS ratios are not expected to equal one without validated common-unit and spatial equivalence.\n\n## Sensitivity and uncertainty\n\nCondition-level percentile bootstrap intervals use 10,000 resamples and seed 0. Leave-one-condition-out results identify the effect of individual RPM conditions on Pearson and Spearman correlations. The 60, 70, 80, 300, and 320 RPM conditions are retained in the audit trail; excluding 60 and 80 RPM is a sensitivity analysis and cannot replace the full result.\n\n## Forced-alignment warning\n\nThe forced-alignment result estimates lag from the first 60% and evaluates the fixed lag on the remaining 40% after interpolation to a common mathematical grid. It is mathematical forced alignment, not recovery of a physical shared clock. Conditional coherence and phase are diagnostics, not physical waveform validation. The obsolete `r_test = -0.118` result is not used.\n\n## Claim boundary\n\nPermitted language is: condition-level statistical characterization of camera spectral-feature repeatability, response-trend correspondence, observation-path dependence, and processing sensitivity. Prohibited language is camera accuracy, simultaneous validation, synchronized exposure, calibration, unique torsional/bending mode, or structural modal identification.\n\n## Reproducibility\n\nRun `python3 run_statistical_analysis.py` from this directory. Input hashes (including the canonical stream table `results/s2c_stream_table_dev.csv`) are recorded in `STATISTICAL_SOURCE_HASHES.sha256`; the 63/60/2/1 stream-inventory check is in `STREAM_INVENTORY_VALIDATION.csv`; runtime, package versions, bootstrap seed, domains, and admissibility counts are in `STATISTICAL_RUNTIME.txt`.\n"""
    )


if __name__ == "__main__":
    main()
