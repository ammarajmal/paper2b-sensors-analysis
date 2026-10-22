# Forced Camera–Laser Alignment Experiment

**STATUS: EXPLORATORY ONLY — NOT TRUE SYNCHRONIZATION, VALIDATION, OR MODAL IDENTIFICATION.**

The lag was estimated by maximizing correlation on the first 60% of each condition and then applied unchanged to the remaining 40%. This tests whether apparent agreement transfers to held-out samples; it does not recover a physical historical start time.

`FORCED_ALIGNMENT_WAVEFORM_RESULTS.csv` contains lag, training correlation, held-out correlation, standardized waveform RMSE, conditional coherence, and conditional phase. `APPARENT_CAMERA_PHASE_MODE_SHAPE.csv` contains fitted camera phase/amplitude at laser target frequencies relative to cam1. `plots/` contains clean selected-condition plots.

High training correlation is expected to be partly manufactured by lag optimization. Held-out correlation, coherence, and phase remain conditional diagnostics because the acquisitions were separate. The phase table is an apparent camera phase pattern, not a structural mode shape: cam1/cam2 view the same marker, cam3 views a different marker, and the signals are not spatially calibrated into common physical degrees of freedom.

True waveform accuracy requires simultaneous acquisition, a common hardware clock or pulse, the same physical observable, calibrated common units, known spatial registration, and predeclared alignment and acceptance rules. Modal identification additionally requires multiple spatial points, reliable phase relationships, mode-shape completeness, and a structural reference or model.
