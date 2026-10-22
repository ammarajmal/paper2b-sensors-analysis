# Independent Validation Report: Paper 2B Per-Camera RMS Reconstruction

**Validation Date:** 2026-10-22\
**Repository HEAD:** `8d03ba3`\
**Execution Environment:** Linux x86_64, Python 3.12.13, NumPy 2.5.4, Pandas 3.0.6, PyArrow 21.0.0\
**Validation Suite:** `validate_per_camera_rms.py`\
**Ledger Table:** [`PER_CAMERA_RMS_VALIDATION.tsv`](PER_CAMERA_RMS_VALIDATION.tsv)\
**Runtime Record:** [`PER_CAMERA_RMS_VALIDATION_RUNTIME.txt`](PER_CAMERA_RMS_VALIDATION_RUNTIME.txt)\
**Reconstruction Target:** [`analysis/paper2b/per_camera_rms/`](.)\

---

## 1. Executive Summary

An exhaustive independent validation of the Paper 2B per-camera RMS reconstruction was performed. All **20 validation checks passed** without exceptions (`20/20 PASS`).

Key validation verdicts:
1. **Source Lineage & Recomputation Parity:** The per-camera RMS values are recomputed strictly from the canonical frame-level Parquet source ([`outputs/s4_pose_channels_by_frame.parquet`](../../../outputs/s4_pose_channels_by_frame.parquet)). In double-precision float64 arithmetic, total mean-removed RMS values match canonical S4 values in [`results/s4_pose_by_stream.csv`](../../../results/s4_pose_by_stream.csv) to within **$4.44 \times 10^{-16}$** on `H1_y_mm` and **$9.89 \times 10^{-17}$** on `H2_roll_rad`. The serialized CSV values in [`PER_CAMERA_RMS_VALUES.csv`](PER_CAMERA_RMS_VALUES.csv) match within $4.55 \times 10^{-10}$, strictly reflecting the expected rounding of the `%.10g` serialization format.
2. **Total Mean-Removed Definition (`ddof=0`):** The reconstruction strictly applies population standard deviation (`ddof=0`) about the admitted stream mean. The sample standard deviation alternative (`ddof=1`) diverges by $\approx 0.027\%$ ($2.73 \times 10^{-4}$ relative difference), which is 12 orders of magnitude larger than the observed parity difference, conclusively refuting `ddof=1`.
3. **No Pooled Table Contamination:** Not a single value was copied or derived from legacy pooled tables (`table_2025_ldv_primary.csv`, [`results/s6_matched_pairs.csv`](../../../results/s6_matched_pairs.csv), or [`EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv`](../exploratory/EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv)).
4. **Stream Accounting & Governance:** The stream inventory comprises exactly **63 detection streams**, **61 S4 pose streams**, **60 admitted streams** ($e_0\dots e_{19} \times 3$ cameras), **2 rejected streams** ($e_{20}$ `cam1` at 60.8% and $e_{20}$ `cam2` at 61.3% completeness), **1 diagnostic-only stream** ($e_{20}$ `cam3`), and **three camera-only 0 RPM noise-floor streams** ($e_0$ `cam1`, `cam2`, `cam3`).
5. **Physical Separation & Interpretation Bounds:** Optical paths for `cam1` and `cam2` (viewing offset marker `ID-0-1`) are strictly isolated from `cam3` (viewing near-axis marker `ID-0-2`). Vertical displacement on `cam1` and `cam2` is explicitly identified as offset-marker displacement dominated by the lever arm rotation ($125\text{ mm} \times \text{roll}$), and is **not equated to laser heave**. `cam3` is designated as the sole defensible primary heave proxy. Camera roll (radians) is not equated to laser pitch or torsion.
6. **Scale Uncertainty Rules:** The provisional $\pm 2.5\%$ tag scale uncertainty is applied strictly and exclusively to millimetre-valued quantities, and is excluded from radian quantities and same-stream noise floor ratios.
7. **Repository Immutability & Determinism:** All 21 raw ROS bags, publication manuscript files, and canonical statistical tables are completely untouched. Full script re-execution generates bit-identical files matching all SHA256 hashes across tables and figures.

---

## 2. Complete Check Matrix

The table below reproduces the results stored in [`PER_CAMERA_RMS_VALIDATION.tsv`](PER_CAMERA_RMS_VALIDATION.tsv).

| Check ID | Category | Description | Criterion / Expected | Observed Result | Status |
|---|---|---|---|---|:---:|
| **CHK-01-PARQUET-HASH** | Source Lineage | Source Parquet SHA256 matches audit registry | `9378c6ea...c612` | `9378c6ea...c612` | **PASS** |
| **CHK-02-INTRINSICS-HASH** | Calibration | Camera intrinsics JSON matches audit registry | `fe2553f1...350f` | `fe2553f1...350f` | **PASS** |
| **CHK-03-RAW-BAGS-HASHES** | Raw Data Integrity | All 21 raw ROS bag files match audit registry | 21/21 matching bag hashes | 21/21 matching bag hashes | **PASS** |
| **CHK-04-DETECTION-STREAMS** | Stream Accounting | Detection streams in `detections_ALL21.parquet` | 63 streams | 63 streams | **PASS** |
| **CHK-05-POSE-STREAMS** | Stream Accounting | Pose streams in `s4_pose_channels_by_frame.parquet` | 61 streams | 61 streams | **PASS** |
| **CHK-06-STREAM-ADMISSION** | Stream Governance | Stream classification breakdown | 60 admitted, 2 rejected, 1 diagnostic | 60 admitted, 2 rejected, 1 diagnostic | **PASS** |
| **CHK-07-E0-CAMERA-ONLY** | Stream Accounting | Three camera-only 0 RPM streams present | 3 admitted streams ($e_0$ cam1-3) | 3 admitted streams ($e_0$ cam1-3) | **PASS** |
| **CHK-08-E20-CAM3-DIAGNOSTIC** | Stream Governance | $e_{20}$ 320 RPM cam3 retained as diagnostic-only | `diagnostic_only` classification | `diagnostic_only` in tables | **PASS** |
| **CHK-09-EXACT-KEYS** | Data Integrity | Exact condition-camera-quantity key matrix | 61 streams $\times$ 8 quantities = 488 rows | 488 rows across 61 streams | **PASS** |
| **CHK-10-NO-DUPLICATES** | Data Integrity | Zero duplicates and zero nulls in required fields | 0 duplicates, 0 nulls | 0 duplicates, 0 nulls | **PASS** |
| **CHK-11-NO-MISSING-DENOMINATORS** | Numerical Robustness | Positive non-zero noise floor denominators | 12 positive $e_0$ floors, 0 invalid ratios | 12 positive floors, 0 invalid ratios | **PASS** |
| **CHK-12-EXACT-RECOMPUTATION** | Numerical Precision | Parquet recomputation parity with S4 | Max error $< 1\times 10^{-12}$ | Max S4 diff: $4.44\times 10^{-16}$ | **PASS** |
| **CHK-13-DDOF0-DEFINITION** | Statistical Definition | Recomputation uses `ddof=0` mean-removed std | `ddof=0` exact; `ddof=1` $\approx 0.027\%$ error | Gap to `ddof=1`: $2.73\times 10^{-4}$ | **PASS** |
| **CHK-14-SENSITIVITY-SEPARATION** | Methodological Separation | Detrended RMS isolated as sensitivity quantity | 0 name collisions, stage isolation | Stage separation strictly preserved | **PASS** |
| **CHK-15-NO-POOLED-VALUES-COPIED** | Source Integrity | Zero pooled values copied to camera rows | 0 matches vs legacy pooled tables | 0 matches found | **PASS** |
| **CHK-16-CAMERA-PATH-SEPARATION** | Physical Architecture | cam1/cam2 separated from cam3 | cam1, cam2, cam3 kept separate | 3 independent optical paths | **PASS** |
| **CHK-17-INTERPRETATION-BOUNDARIES** | Interpretation Governance | cam1/cam2 $\ne$ heave, cam3 primary, roll $\ne$ pitch | Physical boundaries explicit | Disclaimers & boundaries explicit | **PASS** |
| **CHK-18-SCALE-UNCERTAINTY** | Uncertainty Propagation | $\pm 2.5\%$ scale applied strictly to millimetres | mm has scale, rad/ratio are NaN | 122 mm scaled, 366 rad/ratio NaN | **PASS** |
| **CHK-19-REPO-IMMUTABILITY** | Repository Hygiene | Raw bags, manuscripts, and results untouched | 0 modified manuscript/raw files | 0 forbidden modifications | **PASS** |
| **CHK-20-DETERMINISTIC-RERUN** | Reproducibility | Deterministic re-execution preserves all hashes | Bit-identical hash match | Bit-identical match on all artifacts | **PASS** |

---

## 3. Deep-Dive Validation Findings

### 3.1 Source Lineage & Hashing Verification
All input hashes were checked against the approved audit ledger [`analysis/paper2b/per_camera_rms_audit/PER_CAMERA_RMS_SOURCE_HASHES.sha256`](../per_camera_rms_audit/PER_CAMERA_RMS_SOURCE_HASHES.sha256):
- **Frame-level Parquet:** `outputs/s4_pose_channels_by_frame.parquet` has SHA256 `9378c6ea75ec1793ecd1cd183362b795cbe55c75ac57ebcac6a60f291ba3c612`, exactly matching the audit registry.
- **Camera Intrinsics:** `config/intrinsics_bag.json` has SHA256 `fe2553f16a4a1727ec0e289a4b85e94f16e45431db153f1b7e964da8300a350f`, matching the audit registry.
- **Raw Bags:** All 21 raw ROS bag files under `/mnt/phd_data/phd_master/03_datasets/ds004_windtunnel_cameras_2025/raw/wtt-main/` match their registered SHA256 hashes bit-for-bit.

### 3.2 Stream Accounting and Gate S2c Admissibility
Cross-referencing [`outputs/s2_detect/wtt_main/detections_ALL21.parquet`](../../../outputs/s2_detect/wtt_main/detections_ALL21.parquet), [`outputs/s4_pose_channels_by_frame.parquet`](../../../outputs/s4_pose_channels_by_frame.parquet), and [`results/s2c_stream_table_dev.csv`](../../../results/s2c_stream_table_dev.csv) confirms:
1. **63 Detection Streams:** 21 conditions ($e_0\dots e_{20}$) $\times$ 3 cameras (`cam1`, `cam2`, `cam3`) = 63 streams (115,276 total frames).
2. **60 Admitted Streams:** Conditions $e_0$ through $e_{19}$ have 100% detection completeness (1,827 to 1,833 frames per stream) and are classified as `admissible`.
3. **2 Rejected Streams:** $e_{20}\_320\text{rpm}$ `cam1` (completeness 60.8%, 1,112/1,829 frames) and $e_{20}\_320\text{rpm}$ `cam2` (completeness 61.3%, 1,122/1,829 frames) violate the S2c completeness threshold and tag-tracking speed limits. They were excluded from S4 pose computation and have no values in the tables.
4. **1 Diagnostic-Only Stream:** $e_{20}\_320\text{rpm}$ `cam3` (completeness 100%, 1,831 frames) was admitted into S4, but carries high IPPE ambiguity (order $b$, 93% ambiguous). In [`PER_CAMERA_RMS_VALUES.csv`](PER_CAMERA_RMS_VALUES.csv), it is classified as `diagnostic_only` and is strictly excluded from all full results.
5. **Three Camera-Only 0 RPM Streams:** $e_0\_0\text{rpm}$ (`cam1`, `cam2`, `cam3`) are admitted camera streams serving as the empirical zero-velocity noise floor. There are no matched laser runs at 0 RPM.

### 3.3 Recomputation Parity and Statistical Form
Independent calculation directly from the canonical Parquet source yielded:
- **Total RMS Formula:**
  $$\text{RMS}_{\text{total}} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \bar{y})^2} = \text{std}(y, \text{ddof}=0)$$
  - Against [`results/s4_pose_by_stream.csv`](../../../results/s4_pose_by_stream.csv):
    - `H1_y_mm_rms` max absolute difference: **$4.4409 \times 10^{-16}\text{ mm}$**
    - `H2_roll_rad_rms` max absolute difference: **$9.8879 \times 10^{-17}\text{ rad}$**
  - Against [`PER_CAMERA_RMS_VALUES.csv`](PER_CAMERA_RMS_VALUES.csv):
    - Max absolute difference: **$4.5547 \times 10^{-10}$** (due to CSV float formatting `%.10g`)
    - Max relative difference: **$4.2093 \times 10^{-10}$**
- **Refutation of `ddof=1`:**
  Computing sample standard deviation with $\text{ddof}=1$ yields a systematic shift of $\sqrt{N/(N-1)} - 1 \approx 2.73 \times 10^{-4}$ ($\approx 0.027\%$). Because the observed parity difference is $4.44 \times 10^{-16}$, `ddof=1` is conclusively disproved.
- **Linearly Detrended Sensitivity RMS:**
  Least-squares linear trend subtraction was independently evaluated:
  $$y_{\text{detrended}} = y - (mt + c), \quad \text{RMS}_{\text{detrended}} = \text{std}(y_{\text{detrended}}, \text{ddof}=0)$$
  Detrended RMS matches [`PER_CAMERA_RMS_VALUES.csv`](PER_CAMERA_RMS_VALUES.csv) within $4.999 \times 10^{-10}$ (relative difference $< 4.35 \times 10^{-10}$). Over all 61 streams, detrending alters total RMS by at most $2.4\%$ (ratio $\ge 0.976$).

### 3.4 Disentanglement from Pooled RMS Tables
A condition-by-condition numerical search was conducted across:
- `/mnt/phd_data/phd_master/05_publications/p02_sensors_windtunnel/scripts/table_2025_ldv_primary.csv`
- [`results/s6_matched_pairs.csv`](../../../results/s6_matched_pairs.csv)
- [`analysis/paper2b/exploratory/EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv`](../exploratory/EXPLORATORY_CAMERA_LASER_RMS_COMPARISON.csv)

Zero matches were found between per-camera rows and any pooled bend or torsion values for the corresponding condition. The per-camera values represent genuine unpooled channels derived from $H_1$ and $H_2$.

### 3.5 Noise Floor Ratios & Denominator Validation
- Denominators are the empirical $e_0\_0\text{rpm}$ values:
  - `cam1`: $H_{1,y} = 0.005725\text{ mm}$, $H_{2,\text{roll}} = 1.044\times 10^{-4}\text{ rad}$
  - `cam2`: $H_{1,y} = 0.006174\text{ mm}$, $H_{2,\text{roll}} = 9.775\times 10^{-5}\text{ rad}$
  - `cam3`: $H_{1,y} = 0.003156\text{ mm}$, $H_{2,\text{roll}} = 1.916\times 10^{-4}\text{ rad}$
- All 12 denominators are strictly positive and finite.
- Every condition ratio in [`PER_CAMERA_RMS_VALUES.csv`](PER_CAMERA_RMS_VALUES.csv) is finite and positive.
- The `below_5x_camera_floor` flag is assigned strictly when $\text{ratio} < 5.0$ and condition $\ne e_0\_0\text{rpm}$ (verified with 0 errors across all 244 ratio rows).

### 3.6 Physical Interpretation Boundaries & Camera Separation
The validation confirmed that the reconstruction and report adhere to strict governance boundaries:
1. **Marker Path Differentiation:**
   - `cam1` and `cam2` view tag `ID-0-1`, positioned at an offset of $\approx 125\text{ mm}$ from the deck rotation axis.
   - `cam3` views tag `ID-0-2`, positioned near the deck rotation axis ($\approx 6\text{ mm}$).
   - `cam3` has distinct camera intrinsics ($f_x = 25631\text{ px}$ vs $20328\text{ px}$ for `cam1` and $25750\text{ px}$ for `cam2`) and a nominal frame rate of $60.00\text{ Hz}$ (vs $59.94\text{ Hz}$ for `cam1`/`cam2`).
   - The three optical paths are kept strictly independent in all data tables and figures.
2. **Rejection of Heave Equivalence for cam1/cam2:**
   - In roll-dominated conditions ($90\text{ rpm}$, $100\text{ rpm}$, $140\text{--}220\text{ rpm}$), `cam1` and `cam2` vertical displacement $H_{1,y}$ is almost entirely explained by the lever-arm term:
     $$\frac{H_{1,y}}{\text{lever} \times H_{2,\text{roll}}} \approx 0.97 \text{ to } 1.13$$
   - In [`PER_CAMERA_RMS_COMPARISON.csv`](PER_CAMERA_RMS_COMPARISON.csv) and [`PER_CAMERA_RMS_REPORT.md`](PER_CAMERA_RMS_REPORT.md), `cam1`/`cam2` $H_{1,y}$ is explicitly disclaimed: *"offset-marker vertical displacement incl. lever-arm x roll, NOT heave"*.
3. **cam3 Designated Sole Primary Heave Proxy:**
   - `cam3_H1_y_vs_laser_heave_y2025_PRIMARY` is explicitly labelled as the primary heave comparison against the LDV centre head.
4. **Rejection of Roll-Pitch Equivalence:**
   - Camera in-plane roll (radians) is not equated to laser pitch or torsion, correctly avoiding unsupported assumptions about unmeasured lever distance $d$.
5. **Visible Instrumental Discrepancies:**
   - All comparison notes explicitly preserve differences in bandwidth (camera $\approx 30\text{ Hz}$ Nyquist vs laser $180\text{ Hz}$ band), duration ($30.5\text{ s}$ vs $20\text{ s}$), and non-simultaneous recording sessions.

### 3.7 Scale Uncertainty Propagation
- Target budget: $\pm 2.5\%$ relative scale uncertainty based on provisional tag geometry ($20.0\text{ mm}$).
- Implementation audit:
  - All 122 millimetre rows (`unit == 'mm'`) have `scale_rel_unc = 0.025`, `rms_scale_lo = 0.975 * rms_value`, and `rms_scale_hi = 1.025 * rms_value`.
  - All 122 radian rows (`unit == 'rad'`) have `scale_rel_unc = NaN`, `rms_scale_lo = NaN`, `rms_scale_hi = NaN`.
  - All 244 ratio rows (`unit == 'ratio'`) have `scale_rel_unc = NaN`, `rms_scale_lo = NaN`, `rms_scale_hi = NaN` (since scale factor cancels identically in identical-channel ratios).
  - In [`PER_CAMERA_RMS_COMPARISON.csv`](PER_CAMERA_RMS_COMPARISON.csv), ratio scale bounds are applied strictly to millimetre comparisons or mm ratio checks, and never to radian comparisons.

### 3.8 Deterministic Reproducibility
Executing [`run_per_camera_rms.py`](run_per_camera_rms.py) cleanly from scratch reproduced all generated artifacts bit-for-bit:
- `PER_CAMERA_RMS_VALUES.csv`: `785178b7b1fed8618877db4144e08fb1e96f09b909413de43eb2af716e486d26`
- `PER_CAMERA_RMS_COMPARISON.csv`: `03accf651b859aa6948a29e036932f1f385745ab25720b6385e3262a3aa495b1`
- `PER_CAMERA_RMS_DEFINITION_LEDGER.csv`: `3aef22f6e7077965cb208d676eb7b5dcc2d3ca839a0c910ea8f794831329d646`
- `PER_CAMERA_RMS_SOURCE_HASHES.sha256`: `57576e4e61393e3f37a2e201f9d246fc719eec0736dd1fc2bf5634047de17c31`
- All 5 plot PNGs in [`plots/`](plots) matched bit-identical hashes.

---

## 4. Conclusion & Governance Sign-Off

The Paper 2B per-camera RMS reconstruction is **fully validated, statistically sound, numerically exact, and methodologically partitioned**. It completely satisfies every requirement of the CONDITIONAL GO approval:

> [!NOTE] Validated Scientific Claims
> 1. **Repeatability:** `cam1` and `cam2` demonstrate near-perfect physical repeatability on marker `ID-0-1` (geometric mean ratio $0.992$, Spearman $1.00$).
> 2. **Observation-Path Divergence:** `cam3` divergence from `cam1`/`cam2` in roll conditions is physically explained by marker placement relative to the rotation axis, not sensor discrepancy.
> 3. **Laser Comparison Boundaries:** Near-axis heave agreement between `cam3` and LDV y2025 has a geometric mean ratio of $0.515$ and Spearman $0.726$ across all 19 admitted conditions. Excluding the regime-boundary transition conditions ($60$ and $80\text{ rpm}$) increases Spearman rank correlation to **$0.985$**.
> 4. **Zero Claims of Equivalence:** No unsupported claims of camera–laser calibration, absolute heave equivalence for offset markers, or roll–torsion equivalence are made.
