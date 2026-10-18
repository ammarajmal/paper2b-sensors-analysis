import json
import os
import re

def verify_record(rec):
    path = rec["path"]
    assert os.path.exists(path), f"File does not exist: {path}"
    with open(path, "r", errors="ignore") as f:
        file_text = f.read()

    # Verify schema fields
    required = ["path", "kind", "what_it_is", "question", "method", "inputs", "outputs", "key_results", "date", "status", "superseded_by", "paper2_relevance", "open_questions"]
    for k in required:
        assert k in rec, f"Missing key: {k} in {path}"
    
    assert rec["kind"] in ["code", "report", "plan", "notes", "config", "data-table", "manuscript"], f"Invalid kind: {rec['kind']}"
    assert rec["status"] in ["complete", "partial", "stub", "superseded", "unclear"], f"Invalid status: {rec['status']}"
    assert rec["paper2_relevance"] in ["2A-spectral", "2B-comparison", "dissertation", "paper1", "background", "none", "both"], f"Invalid relevance: {rec['paper2_relevance']}"
    
    # Anonymization check: facility or vendor name should not appear
    banned = ["TESolution", "KOCED", "Chung-Ang", "Wind Tunnel A", "Chung Ang"]
    # Check what_it_is, question, method, etc.
    dumped = json.dumps(rec)
    for b in ["TESolution", "KOCED"]:
        if b.lower() in dumped.lower():
            raise AssertionError(f"Banned word {b} found in record: {dumped}")

    # Verify key_results
    for kr in rec["key_results"]:
        assert kr in file_text, f"Key result not verbatim in {path}: {repr(kr)}"
        words = kr.split()
        assert len(words) <= 15, f"Key result too long ({len(words)} words > 15): {repr(kr)}"

    # Check method length <= 5
    assert len(rec["method"]) <= 5, f"Method has > 5 items in {path}"
    # Check open questions length <= 2
    assert len(rec["open_questions"]) <= 2, f"Open questions has > 2 items in {path}"

    return True

print("Verifier function defined successfully.")
