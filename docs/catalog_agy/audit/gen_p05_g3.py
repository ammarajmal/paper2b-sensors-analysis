import sys, os, csv, json
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

def get_group3():
    recs = []
    
    # 24: 71_FINAL_SYNTHESIS_MERGE_EXECUTION.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/71_FINAL_SYNTHESIS_MERGE_EXECUTION.csv",
        "kind": "data-table",
        "what_it_is": "Merge execution ledger recording pre- and post-merge cryptographic checksums and actions resolving manuscript candidate differences.",
        "question": "What exact merge operations and hash transitions were executed during the final synthesis of manuscript candidates?",
        "method": ["tracking merge operation IDs", "recording pre- and post-merge SHA-256 hashes", "verifying evidence-based editorial adjudications"],
        "inputs": ["candidate manuscript drafts", "editorial defect registers"],
        "outputs": ["71_FINAL_SYNTHESIS_MERGE_EXECUTION.csv"],
        "key_results": ["MRG-M01,OPUS,opus/paper2_sensors_opus.tex (7.6417 Hz),manuscript/final_candidates/synthesis_v2/paper2_sensors_synthesis.tex,INHERITED_FROM_BASE - no further edit required; Opus base"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 25: SUPPLEMENT_MANIFEST.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/structural_vision_research/manuscript/final_candidates/synthesis/supplement_rebuilt/SUPPLEMENT_MANIFEST.csv",
        "kind": "data-table",
        "what_it_is": "Distribution manifest mapping supplemental data CSV items S1 through S4 to their canonical paths and cryptographic hashes.",
        "question": "Which data artifacts constitute the official electronic supplement and what are their verification hashes?",
        "method": ["cataloguing supplemental items S1 through S4", "verifying distributed file paths and SHA-256 digests against the registry"],
        "inputs": ["supplementary CSV data files"],
        "outputs": ["SUPPLEMENT_MANIFEST.csv"],
        "key_results": ["S1,21_FULL_PER_CAMERA_FREQUENCY_SWEEP.csv,data/21_FULL_PER_CAMERA_FREQUENCY_SWEEP.csv"],
        "date": "unclear",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })

    # 26: 68_FINAL_SYNTHESIS_MERGE_PLAN.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/68_FINAL_SYNTHESIS_MERGE_PLAN.csv",
        "kind": "plan",
        "what_it_is": "Arbitration merge plan detailing defect-by-defect adjudications between Terra and Opus manuscript versions.",
        "question": "How are specific numerical discrepancies and narrative differences between the Terra and Opus candidate texts reconciled?",
        "method": ["identifying canonical drafting defects", "comparing proposed resolutions from Terra and Opus candidates", "establishing primary evidence adjudications"],
        "inputs": ["Terra and Opus manuscript drafts", "audit evidence registers"],
        "outputs": ["68_FINAL_SYNTHESIS_MERGE_PLAN.csv"],
        "key_results": ["MRG-M01,M-01 last-digit value,\"5.5 states e0_0rpm cam3 reaches 7.6419 Hz; frozen"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 27: 63A_TERRA_INTERRUPTED_CANDIDATE_MANIFEST.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/63A_TERRA_INTERRUPTED_CANDIDATE_MANIFEST.csv",
        "kind": "data-table",
        "what_it_is": "Filesystem snapshot inventory recording sizes and pre-modification SHA-256 hashes of the Terra manuscript tree upon task interruption.",
        "question": "What was the exact state and cryptographic integrity of the Terra manuscript files when the author session was interrupted?",
        "method": ["logging file sizes and modification timestamps", "calculating SHA-256 digests of all candidate artifacts"],
        "inputs": ["Terra candidate manuscript directory tree"],
        "outputs": ["63A_TERRA_INTERRUPTED_CANDIDATE_MANIFEST.csv"],
        "key_results": ["paper2_sensors_terra.tex,88334,1c963cb3872034ea75a2435f571462b594b41f34cc02a44ad72e5aae6e3582f4,2026-09-08 22:51:39,TERRA_AS_FOUND"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 28: 51_PASS4_BUILD_VERIFICATION.json
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/51_PASS4_BUILD_VERIFICATION.json",
        "kind": "report",
        "what_it_is": "Automated build verification report logging successful compilation of paper2_sensors.tex with zero LaTeX errors.",
        "question": "Did the Pass-4 revised Sensors manuscript compile cleanly using latexmk without errors or missing references?",
        "method": ["executing latexmk in nonstopmode", "evaluating process exit status and error count"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["51_PASS4_BUILD_VERIFICATION.json"],
        "key_results": ["\"command\": \"latexmk -pdf -interaction=nonstopmode paper2_sensors.tex\","],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 29: 51_PASS4_CLOSURE_VERIFICATION.json
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/51_PASS4_CLOSURE_VERIFICATION.json",
        "kind": "report",
        "what_it_is": "Closure audit report recording final SHA-256 digest, abstract token count, and duration ranges for the Sensors manuscript.",
        "question": "Does the final Sensors manuscript meet all journal length constraints and maintain frozen cryptographic integrity?",
        "method": ["computing SHA-256 digest of final manuscript", "counting abstract source tokens", "checking duration ranges"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["51_PASS4_CLOSURE_VERIFICATION.json"],
        "key_results": ["\"manuscript_sha256\": \"ae734f96079dcca0ca4a2f1c216c08e5fbde087a0f1d9aaa8d27716bde9b084c\","],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 30: 51_PASS4_REQUIRED_TERM_REVIEW.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/51_PASS4_REQUIRED_TERM_REVIEW.csv",
        "kind": "data-table",
        "what_it_is": "Automated scan log certifying zero active hits for unverified numerical values like 135.14 across the manuscript prose.",
        "question": "Are unverified legacy tag dimensions or uncalibrated constants completely eliminated from active manuscript prose?",
        "method": ["case-insensitive regex scanning across uncommented source lines", "validating zero active hits for prohibited numerical strings"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["51_PASS4_REQUIRED_TERM_REVIEW.csv"],
        "key_results": ["135.14,,ZERO_ACTIVE_HITS,Case-insensitive scan of uncommented source; acronym word boundaries."],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 31: 51_PASS4_LEGACY_CLAIM_SCAN.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/51_PASS4_LEGACY_CLAIM_SCAN.csv",
        "kind": "data-table",
        "what_it_is": "Contextual claim audit table confirming that occurrences of 'accuracy' and 'validation' are restricted strictly to limitation sections.",
        "question": "Are evaluative terms like 'accuracy' appropriately bounded as interpretive limitations rather than unverified performance claims?",
        "method": ["scanning manuscript for occurrences of 'accuracy' and 'validation'", "classifying each instance by section and epistemic status"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["51_PASS4_LEGACY_CLAIM_SCAN.csv"],
        "key_results": ["accuracy,434,active prose/end matter,ACTIVE_ALLOWED_LIMITATION,\"Explicit negation, interpretive limitation, open gate or prospective"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 32: 51_PASS4_CLAIM_TRACEABILITY.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/51_PASS4_CLAIM_TRACEABILITY.csv",
        "kind": "data-table",
        "what_it_is": "Traceability matrix mapping every core claim in the Pass-4 Sensors manuscript to formal claim IDs and primary data evidence.",
        "question": "How does each scientific statement in Paper 2A trace directly to primary experimental datasets and formal registry items?",
        "method": ["extracting manuscript sentences by section", "mapping sentences to 42B claim IDs and primary evidence artifacts"],
        "inputs": ["paper2_sensors.tex", "42B_CLAIM_TO_SECTION_MATRIX_CORRECTED.csv"],
        "outputs": ["51_PASS4_CLAIM_TRACEABILITY.csv"],
        "key_results": ["Native-Timestamp Per-Camera Spectral Characterization of Wind-Excited Bridge-Deck Response: Cross-View Agreement"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 33: 50_PASS4_BUILD_VERIFICATION.json
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/50_PASS4_BUILD_VERIFICATION.json",
        "kind": "report",
        "what_it_is": "Preliminary Pass-4 build log recording the generation of a 22-page Sensors PDF with zero errors.",
        "question": "Did the initial Pass-4 compilation yield the expected page count and zero latexmk errors?",
        "method": ["invoking latexmk on paper2_sensors.tex", "logging page count and error totals"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["50_PASS4_BUILD_VERIFICATION.json"],
        "key_results": ["\"pages\": 22,"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 34: 50_PASS4_CLAIM_TRACEABILITY.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/50_PASS4_CLAIM_TRACEABILITY.csv",
        "kind": "data-table",
        "what_it_is": "Initial Pass-4 claim traceability matrix linking manuscript sections to evidence records prior to final closure.",
        "question": "What was the preliminary mapping of manuscript claims to evidence artifacts in Pass-4?",
        "method": ["cataloguing manuscript claims across sections", "verifying supporting evidence artifacts and qualification criteria"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["50_PASS4_CLAIM_TRACEABILITY.csv"],
        "key_results": ["Native-Timestamp Per-Camera Spectral Characterization of Wind-Excited Bridge-Deck Response: Cross-View Agreement"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 35: 50_PASS4_LEGACY_CLAIM_SCAN.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/50_PASS4_LEGACY_CLAIM_SCAN.csv",
        "kind": "data-table",
        "what_it_is": "Preliminary keyword scan table evaluating occurrences of legacy terminology in manuscript draft 50.",
        "question": "Were legacy evaluative terms flagged in draft 50 before final revision approval?",
        "method": ["identifying occurrences of monitored keywords", "classifying line numbers and allowed limitation contexts"],
        "inputs": ["paper2_sensors.tex"],
        "outputs": ["50_PASS4_LEGACY_CLAIM_SCAN.csv"],
        "key_results": ["accuracy,434,active prose/end matter,ACTIVE_ALLOWED_LIMITATION,\"Explicit negation, interpretive limitation, open gate or prospective"],
        "date": "2026-09-08",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 36: 42B_CLAIM_TO_SECTION_MATRIX_CORRECTED.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/42B_CLAIM_TO_SECTION_MATRIX_CORRECTED.csv",
        "kind": "data-table",
        "what_it_is": "Corrected epistemic claim ledger defining precise authorized wording, evidence artifacts, and section assignments for Paper 2A.",
        "question": "What exact claims regarding stream admissibility and AprilTag detection gates are approved for inclusion in each section?",
        "method": ["defining formal claim statements CL01 through CL10", "assigning epistemic classes and mandatory phrasing bounds"],
        "inputs": ["admissibility classification results", "detector gate logs"],
        "outputs": ["42B_CLAIM_TO_SECTION_MATRIX_CORRECTED.csv"],
        "key_results": ["CL01,\"63 camera streams (21 conditions x 3 cameras) were classified"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 37: 42_CLAIM_TO_SECTION_MATRIX.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/42_CLAIM_TO_SECTION_MATRIX.csv",
        "kind": "data-table",
        "what_it_is": "Initial baseline claim-to-section matrix outlining epistemic classifications and evidence artifacts across Paper 2A.",
        "question": "How were Paper 2A claims initially organized across manuscript sections before the 42B correction?",
        "method": ["formulating initial claim bounds for camera stream processing", "mapping claims to target manuscript sections"],
        "inputs": ["experimental data analyses"],
        "outputs": ["42_CLAIM_TO_SECTION_MATRIX.csv"],
        "key_results": ["CL01,\"63 camera streams (21 conditions x 3 cameras) were processed"],
        "date": "2026-09-07",
        "status": "superseded",
        "superseded_by": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/42B_CLAIM_TO_SECTION_MATRIX_CORRECTED.csv",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 38: 37_FACILITY_FREQUENCY_LINEAGE.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/37_FACILITY_FREQUENCY_LINEAGE.csv",
        "kind": "data-table",
        "what_it_is": "Forensic lineage audit cataloguing free-vibration test records, duration, sample counts, and timestamp columns from the facility.",
        "question": "What raw test files document the facility's 1.4303 Hz bending and 3.1036 Hz torsion natural frequency values?",
        "method": ["auditing file structures of B1.csv and T1.csv", "verifying sample counts, durations, and explicit timestamp availability"],
        "inputs": ["facility free-vibration data files"],
        "outputs": ["37_FACILITY_FREQUENCY_LINEAGE.csv"],
        "key_results": ["1,B1.csv,camera_fiducial_extract,bending_vertical,100.06 (inferred from companion file; no timestamp column in this"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 39: 34_STREAM_STABILITY_DIAGNOSTIC_MATRIX.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/34_STREAM_STABILITY_DIAGNOSTIC_MATRIX.csv",
        "kind": "data-table",
        "what_it_is": "Diagnostic stability matrix evaluating dominant frequency persistence across 10-second windows and half-records for all 63 streams.",
        "question": "Which camera streams exhibit within-band frequency wobble or half-record persistence failures across the 21 test conditions?",
        "method": ["segmenting camera displacement time series into 10-second windows", "evaluating frequency persistence across half-records", "logging min, max, and range of windowed peaks"],
        "inputs": ["camera centroid time histories across 21 conditions"],
        "outputs": ["34_STREAM_STABILITY_DIAGNOSTIC_MATRIX.csv"],
        "key_results": ["e0_0rpm,0,cam1,True,8.9476,9.6662,0.7186,True,True,9.6662|9.2570|8.9476|9.2797|9.3054,min=8.9673 max=9.2902 range=0.3228 Hz | sequence: 8.9673|9.2433|9.2902,\"Sec.4: within-band wobble in"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 40: 32_BACKGROUND_BAND_RECONCILIATION.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/32_BACKGROUND_BAND_RECONCILIATION.csv",
        "kind": "data-table",
        "what_it_is": "Reconciliation table verifying independent reproduction of the ~9 Hz background band peaks across centroid and corner coordinate signals.",
        "question": "Do centroid and corner coordinate signals independently reproduce identical peak frequencies in the 8-10 Hz band?",
        "method": ["extracting periodograms from centroid_x, centroid_y, corner0_x, and corner1_x signals", "comparing independently reproduced peaks against prior results"],
        "inputs": ["per-frame detection logs"],
        "outputs": ["32_BACKGROUND_BAND_RECONCILIATION.csv"],
        "key_results": ["e0_0rpm,0,cam1,centroid_x,9.2828,9.2828,True,8.0045,9.2844,y_family,True"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 41: 22_REFERENCE_BLIND_PEAKS_LONG.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/22_REFERENCE_BLIND_PEAKS_LONG.csv",
        "kind": "data-table",
        "what_it_is": "Long-format database tabulating extracted reference-blind spectral peaks, normalized power, prominence, and vertical frequency metrics.",
        "question": "What ranked spectral peaks, powers, and prominences are identified across all conditions without reference knowledge?",
        "method": ["computing Lomb-Scargle periodograms on native timestamps", "ranking spectral peaks by power and prominence", "extracting vertical frequency candidates"],
        "inputs": ["camera centroid time series"],
        "outputs": ["22_REFERENCE_BLIND_PEAKS_LONG.csv"],
        "key_results": ["e0_0rpm,0,cam1,1,9.282812744970565,0.12396914629634793,1.0,0.1239357087224193,7.852512744970565,549."],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 42: 11_TAG_ID_RECONCILIATION.csv.superseded_2026-09-07_pre-comma-quoting-fix.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/_superseded_snapshots/11_TAG_ID_RECONCILIATION.csv.superseded_2026-09-07_pre-comma-quoting-fix.csv",
        "kind": "data-table",
        "what_it_is": "Pre-fix snapshot of the AprilTag ID reconciliation table archived before correcting comma-quoting syntax errors.",
        "question": "What was the unquoted preliminary structure of the tag ID reconciliation table before formatting fixes?",
        "method": ["mapping camera viewpoints to physical tag IDs", "archiving pre-fix CSV snapshot"],
        "inputs": ["dataset contact sheets"],
        "outputs": ["11_TAG_ID_RECONCILIATION.csv.superseded_2026-09-07_pre-comma-quoting-fix.csv"],
        "key_results": ["\"e0_0rpm; e5_70rpm; e20_320rpm (contact-sheet sample frames)\",cam1,\"front oblique (per dataset readme.md;"],
        "date": "2026-09-07",
        "status": "superseded",
        "superseded_by": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/11_TAG_ID_RECONCILIATION.csv",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 43: 13_CAMPAIGN_GEOMETRY_RECONCILIATION.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/13_CAMPAIGN_GEOMETRY_RECONCILIATION.csv",
        "kind": "data-table",
        "what_it_is": "Geometry reconciliation table verifying physical camera setups, marker placements, and photo evidence across the 2024 and 2025 campaigns.",
        "question": "How did camera placement geometry and physical target locations differ between the 2024 and 2025 wind-tunnel campaigns?",
        "method": ["auditing campaign metadata and photographic evidence", "documenting camera field-of-view, mounting points, and physical targets"],
        "inputs": ["campaign documentation photographs", "test protocol records"],
        "outputs": ["13_CAMPAIGN_GEOMETRY_RECONCILIATION.csv"],
        "key_results": ["source field photograph documenting 2024 marker mounting"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })

    # 44: 11_TAG_ID_RECONCILIATION.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/11_TAG_ID_RECONCILIATION.csv",
        "kind": "data-table",
        "what_it_is": "Verified tag ID reconciliation table confirming physical marker locations, tag family (tag36h11), and expected IDs for all three cameras.",
        "question": "Which AprilTag IDs, physical locations, and viewing angles correspond to cameras 1, 2, and 3 across test conditions?",
        "method": ["inspecting contact sheet sample frames", "binding physical marker positions (center vs side) to camera channels and tag IDs"],
        "inputs": ["camera contact sheets across test conditions"],
        "outputs": ["11_TAG_ID_RECONCILIATION.csv"],
        "key_results": ["\"e0_0rpm; e5_70rpm; e20_320rpm (contact-sheet sample frames)\",cam1,\"front oblique (per dataset readme.md;"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 45: 09_64_SAMPLE_SYNTHETIC_CHECK.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/09_64_SAMPLE_SYNTHETIC_CHECK.csv",
        "kind": "data-table",
        "what_it_is": "Synthetic frequency estimation benchmark testing FFT peak bin detection accuracy on short 64-sample window segments.",
        "question": "What frequency bin quantization error occurs when performing spectral analysis on short 64-sample segments with constant vs linear detrending?",
        "method": ["synthesizing sinusoidal test signals at 0.8 Hz and 1.4303 Hz", "computing FFT with 64-point segments under constant and linear detrending", "evaluating reported peak bin locations"],
        "inputs": ["synthetic sinusoidal signal series"],
        "outputs": ["09_64_SAMPLE_SYNTHETIC_CHECK.csv"],
        "key_results": ["0.8,0.9375,constant,64"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 46: 10_FREE_VIBRATION_CHECK.json
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/10_FREE_VIBRATION_CHECK.json",
        "kind": "report",
        "what_it_is": "Verification registry logging file paths, cryptographic hashes, and extracted frequency values for free-vibration video runs.",
        "question": "What are the verified file hashes and natural frequencies recorded during the facility free-vibration calibration tests?",
        "method": ["cataloguing free-vibration raw data files", "recording SHA-256 cryptographic hashes for video recordings"],
        "inputs": ["free vibration raw video and text records"],
        "outputs": ["10_FREE_VIBRATION_CHECK.json"],
        "key_results": ["\"15f01e7fab6016f8d094068b17509318a122da619a0860073ae77ed368f407a3\","],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 47: additional_run.json
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/additional_run.json",
        "kind": "report",
        "what_it_is": "Cryptographic execution log recording SHA-256 digests of the tracking script, motion compensation inputs, and raw track data.",
        "question": "What input script and data versions were used during the motion compensation rerun?",
        "method": ["hashing processing script and input tracking files", "logging execution state for audit repeatability"],
        "inputs": ["compensated tracking input files"],
        "outputs": ["additional_run.json"],
        "key_results": ["\"script_sha256\": \"7a7def69c35efcf86202ce3a7edd38e6a702dd1c1c3447bd7d2c9e6e5a0afd87\","],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 48: 08_COMPENSATION_CHECK.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/08_COMPENSATION_CHECK.csv",
        "kind": "data-table",
        "what_it_is": "Diagnostic comparison table measuring standard deviation changes before and after background motion compensation across test conditions.",
        "question": "Does background motion compensation reduce coordinate standard deviation consistently across cameras and wind speeds?",
        "method": ["calculating pixel y standard deviation on raw detections", "recomputing standard deviation following background reference subtraction", "evaluating compensated-to-raw variance ratios"],
        "inputs": ["raw and background-compensated coordinate time series"],
        "outputs": ["08_COMPENSATION_CHECK.csv"],
        "key_results": ["e0_0rpm,cam1,1832,0.08423068655699582,0.057158103291247146,0.6785900201890239,same_valid_samples; full_record_mean_removed; no_resampling,processing_sensitivity_not_accuracy"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 49: 07_NATIVE_TIMESTAMP_CROSSCHECK.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/07_NATIVE_TIMESTAMP_CROSSCHECK.csv",
        "kind": "data-table",
        "what_it_is": "Cross-check results table comparing Lomb-Scargle dominant peak frequencies and powers extracted on native timestamps for exploratory runs.",
        "question": "What peak frequencies and normalized spectral powers are resolved when evaluating native timestamps directly on conditions e4 and e13?",
        "method": ["computing Lomb-Scargle periodogram on native frame timestamps", "resolving dominant frequency peaks using a 0.005 Hz search step"],
        "inputs": ["native camera detection timestamps"],
        "outputs": ["07_NATIVE_TIMESTAMP_CROSSCHECK.csv"],
        "key_results": ["e13_180rpm,cam1,native_timestamp_Lomb_Scargle,3.065000000000002,0.005,0.9773307936699247,exploratory"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 50: 06_CALIBRATION_REGISTRY.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/06_CALIBRATION_REGISTRY.csv",
        "kind": "data-table",
        "what_it_is": "Master calibration registry tabulating image dimensions, focal lengths (fx, fy), hashes, and verification statuses for all calibration YAMLs.",
        "question": "What are the focal lengths, image dimensions, and verified applicability scopes for each camera calibration file in the repository?",
        "method": ["cataloguing calibration files across cam1, cam2, and cam3", "extracting focal lengths fx and fy from camera matrices", "checking extrinsics verification status"],
        "inputs": ["camera calibration YAML files"],
        "outputs": ["06_CALIBRATION_REGISTRY.csv"],
        "key_results": ["03_datasets/ds004_windtunnel_cameras_2025/calibration/calib_data/cam1/ost.yaml,f0d0b8384592a5e1357f1"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })

    # 51: 04_FREQUENCY_FEASIBILITY.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/04_FREQUENCY_FEASIBILITY.csv",
        "kind": "data-table",
        "what_it_is": "Feasibility study table evaluating spectral bin resolution and dominant peak frequencies across varying FFT segment lengths.",
        "question": "How does spectral bin spacing (df) affect dominant frequency recovery in the 9 Hz band when segment length varies from 512 to 1066?",
        "method": ["resampling raw centroid_y to uniform 60 Hz timebase", "computing Welch periodograms with nperseg=512, 1024, and 1066", "comparing discrete bin peaks against parabolic-interpolated peak frequencies"],
        "inputs": ["e0_0rpm camera 1 centroid time series"],
        "outputs": ["04_FREQUENCY_FEASIBILITY.csv"],
        "key_results": ["e0_0rpm,cam1,512,59.93972303076083,0.11706977154445475,9.13144218046747,9.116244513345801,17.7678498"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "2A-spectral",
        "open_questions": []
    })

    # 52: 02_BAG_TOPIC_MANIFEST.csv
    recs.append({
        "path": "/mnt/phd_data/phd_master/00_inbox/Paper2_Review_2026-09-06/02_BAG_TOPIC_MANIFEST.csv",
        "kind": "data-table",
        "what_it_is": "ROS bag manifest indexing topics, connection IDs, message counts, and timestamps across the wind-tunnel test recordings.",
        "question": "What ROS topics, message types, and indexed message counts are contained in the raw wind tunnel bag files?",
        "method": ["inspecting ROS bag headers with rosbags library", "extracting topic names, connection IDs, and message counts", "logging record start and end timestamps"],
        "inputs": ["raw wind tunnel bag files"],
        "outputs": ["02_BAG_TOPIC_MANIFEST.csv"],
        "key_results": ["03_datasets/ds004_windtunnel_cameras_2025/raw/wtt-5sec/e0_0rpm/e0_0rpm_run1.bag,wtt-5sec,e0_0rpm,0,/"],
        "date": "2026-09-07",
        "status": "complete",
        "superseded_by": "",
        "paper2_relevance": "both",
        "open_questions": []
    })

    return recs

if __name__ == '__main__':
    recs = get_group3()
    print(f"Testing {len(recs)} records from Group 3...")
    for i, r in enumerate(recs):
        ok, msg = verify_record(r)
        if not ok:
            print(f"Error in {i} ({r['path']}): {msg}")
            sys.exit(1)
    print("All Group 3 records (rows 24-52) passed successfully!")
