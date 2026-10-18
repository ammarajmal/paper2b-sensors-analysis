import os, sys

def verify_record(rec):
    path = rec['path']
    if not os.path.exists(path):
        return False, f"File not found: {path}"
    with open(path, 'r', errors='ignore') as f:
        content = f.read()
    
    # Check key_results
    for kr in rec.get('key_results', []):
        if kr not in content:
            return False, f"Quote not found in {path}: {repr(kr)}"
        if len(kr.split()) > 15:
            return False, f"Quote too long (>15 words) in {path}: {len(kr.split())} words: {repr(kr)}"
            
    # Check forbidden facility / vendor names in what_it_is, question, method, etc.
    # TESolution -> the facility, Keyence -> the vendor
    forbidden = ["TESolution", "TESOLUTION", "Keyence", "KEYENCE"]
    for field in ['what_it_is', 'question', 'superseded_by']:
        val = rec.get(field, '')
        for forb in forbidden:
            if forb in val:
                return False, f"Forbidden name {forb} in {field} for {path}"
    for field in ['method', 'inputs', 'outputs', 'open_questions']:
        for item in rec.get(field, []):
            for forb in forbidden:
                if forb in item:
                    return False, f"Forbidden name {forb} in {field} item {repr(item)} for {path}"
                    
    # Check valid enums
    if rec['kind'] not in ["code", "report", "plan", "notes", "config", "data-table", "manuscript"]:
        return False, f"Invalid kind: {rec['kind']} for {path}"
    if rec['status'] not in ["complete", "partial", "stub", "superseded", "unclear"]:
        return False, f"Invalid status: {rec['status']} for {path}"
    if rec['paper2_relevance'] not in ["2A-spectral", "2B-comparison", "dissertation", "paper1", "background", "none", "both"]:
        return False, f"Invalid paper2_relevance: {rec['paper2_relevance']} for {path}"
        
    return True, "OK"
