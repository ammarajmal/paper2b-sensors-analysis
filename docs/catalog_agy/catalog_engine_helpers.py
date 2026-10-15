import os
import re
import ast
import json
import yaml

ALLOWED_TOPICS = {
    "acquisition", "timing", "detection", "calibration", "pose", "fusion",
    "spectral", "laser", "comparison", "uncertainty", "figures", "manuscript",
    "governance", "ros", "utility", "test"
}

ALLOWED_RELATES_TO = {
    "paper2A-spectral", "paper2B-comparison", "dissertation", "paper1",
    "background", "none", "unknown"
}

ALLOWED_STATUS = {
    "complete", "partial", "stub", "debug", "superseded", "unknown"
}

ALLOWED_KINDS = {
    "code", "report", "plan", "config", "notes"
}

FACILITY_PATTERNS = [
    re.compile(r"TE\s*Solution", re.IGNORECASE),
    re.compile(r"TESolution", re.IGNORECASE),
    re.compile(r"Chonbuk", re.IGNORECASE),
    re.compile(r"Jeonbuk", re.IGNORECASE),
    re.compile(r"K-ECo", re.IGNORECASE),
    re.compile(r"KOCED", re.IGNORECASE),
]

def sanitize_facility(text):
    if not text:
        return text
    res = text
    for pat in FACILITY_PATTERNS:
        res = pat.sub("the facility", res)
    return res

def get_exact_quote(text, max_words=12):
    """Find a clean, representative quote of at most 12 words from the text."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    quotes = []
    for l in lines:
        # ignore pure code/formatting/markdown header hashes
        clean_l = re.sub(r"^[#\-\*\>\s\d\.\:]+", "", l).strip()
        if not clean_l or clean_l.startswith("```") or clean_l.startswith("|") or clean_l.startswith("==="):
            continue
        # Split into sentences or clauses
        parts = re.split(r"[\.\;\:\n]", clean_l)
        for p in parts:
            p = p.strip()
            words = p.split()
            if 3 <= len(words) <= max_words:
                # verify character for character exact match
                if p in text and p not in quotes:
                    quotes.append(p)
                    if len(quotes) >= 3:
                        return quotes
    # Fallback to substrings
    if not quotes and lines:
        for l in lines:
            words = l.split()
            if 3 <= len(words) <= max_words and l in text:
                quotes.append(l)
                if len(quotes) >= 2:
                    break
    return quotes[:3]

print("Engine helper loaded.")
