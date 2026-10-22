# Exploratory Waveform, Spectral-Shape, and Apparent Spatial-Response Study

**STATUS: EXPLORATORY ONLY — NOT WAVEFORM VALIDATION AND NOT MODAL IDENTIFICATION.**

Camera centroid-y traces and laser D-file traces were processed independently. Because the campaigns are not synchronized, no camera–laser Pearson waveform correlation, cross-correlation lag, phase error, coherence, or time-domain RMSE was computed. Such values would be physically uninterpretable across separate acquisitions.

Scope: the spectral-shape table has 60 rows (20 laser-matched conditions × 3 cameras) and omits the three camera-only 0 RPM streams of the 63-stream inventory (60 admissible, 2 rejected, 1 diagnostic-only; `results/s2c_stream_table_dev.csv`).

The analysis instead reports:

- camera centroid-y RMS in pixels;
- camera and laser dominant spectral frequencies;
- normalized 0.5–10 Hz spectral-envelope cosine similarity;
- camera cam1/cam2 same-marker response ratios;
- cam3 relative response to the mean of cam1/cam2.

The cam1/cam2/cam3 response table is an **apparent observation-path response pattern**, not a mode shape. Pixel RMS is not a calibrated displacement amplitude, and cam3 differs in marker location, angle, standoff, and optical path.

For genuine waveform-level validation, reacquire the camera and laser signals simultaneously with a common timing signal, use the same physical point and observable, calibrate both in common units, and compare aligned windows with predeclared metrics and uncertainty.
