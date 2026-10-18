summary = """# GROUP G1: Paper 2 Core Summary

### 1. Scope and Contents
Group G1 contains the authoritative research lineage, code, configuration, experimental data registers, and manuscript versions for Paper 2 (comprising Paper 2A on native-timestamp per-camera spectral identification for Sensors and Paper 2B on multi-camera offline pose reconstruction for Measurement). It spans 908 total inventory rows across 7 batches (549 audited records, 359 skipped third-party/duplicate files).

### 2. Main Experimental Workflow
1. **Acquisition**: Three synchronized Sony cameras captured video of wind-tunnel bridge-deck vibrations across 21 fan speeds (`e0_0rpm` to `e20_320rpm`) plus static baseline tests.
2. **Detection & Admissibility**: AprilTag 36h11 markers (20 mm physical side length) were tracked and filtered through a 5-gate admissibility protocol (Tag ID 0, Hamming=0, decision margin >= 30, completeness >= 0.80, and velocity gating).
3. **Calibration & Spatial Projection**: Production intrinsics (`cam1` fx=20327.9, `cam2` fx=25749.5, `cam3` fx=25630.9) and spatial operators projected 2D fiducial points into vertical bending (centroid mean) and torsion proxy (inter-camera differential).
4. **Spectral Analysis**: Non-uniform native timestamps and Lomb-Scargle/nearest-neighbor resampling were evaluated against uniform FFT.
5. **Laser Comparison**: Camera trajectories were paired with laser displacement records across 19 integer-matched RPM conditions.

### 3. Key Scripts and Results
- **Modal Identification**: `S06_3_MODAL_CONSENSUS_2026-08-13.md` and `S11_1_LDV_NPERSEG4096_RESONANCE_CHECK_2026-08-30.md` established that preliminary 0.938 Hz peaks were FFT grid resolution artifacts (`nperseg=64`), whereas fine-resolution reanalysis confirmed physical bending at 1.406–1.494 Hz, matching the facility benchmark of 1.4303 Hz (bending) and 3.1036 Hz (torsion) synthesized in `03_results.md`.
- **Laser Association**: `03_results.md` established the corrected 19-condition camera-vs-laser association: bending Spearman rho = 0.691 (p = 0.0026) and Pearson r = 0.616 (rho = 0.926 excluding resonance).
- **High-Speed Dropout**: `HIGH_VELOCITY_QUAD_SEGMENTATION_FAILURE_2026-08-13.md` documented the 320 RPM boundary dropout where motion blur caused 39.2% failure in `cam1` and 38.7% in `cam2`.

### 4. Planned but Missing Items and Duplicates
- **Missing Surveyed Geometry**: Caliper measurement of the 2025 camera marker separation is missing; the photogrammetric derivation of 135.14 mm was formally retracted in `FINAL_NUMBER_LEDGER_2026-08-02.md`.
- **Duplications**: 359 files represent third-party Arduino libraries (`SdFat`, `Adafruit`, `Unishox2`), display firmware (`E-Paper_code`), or duplicate LaTeX/bib templates.
"""

path = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/GROUP_G1_paper2_core_SUMMARY.md"
with open(path, "w") as f:
    f.write(summary.strip() + "\n")

word_count = len(summary.split())
print(f"Wrote {path}: {word_count} words (Limit: <= 400 words)")
assert word_count <= 400
