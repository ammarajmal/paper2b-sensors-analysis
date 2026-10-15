import re
import os

def clean_extract_quotes(text, max_words=12):
    quotes = []
    # Clean lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in lines:
        if l.startswith("```") or l.startswith("|") or l.startswith("===") or l.startswith("---"):
            continue
        # Strip markdown formatting for candidates, but ensure we extract exact text
        # Look for full sentences or clean clauses
        # Don't split on dots followed by digits (like S09.03 or 3.14)
        candidates = re.split(r'(?<!\d)\.(?!\d)|\;|\n', l)
        for c in candidates:
            c_str = c.strip()
            # remove leading bullet / header marks
            c_clean = re.sub(r'^[#\-\*\>\s\d\.\:]+', '', c_str).strip()
            if not c_clean:
                continue
            words = c_clean.split()
            if 4 <= len(words) <= max_words:
                if c_clean in text and c_clean not in quotes:
                    quotes.append(c_clean)
                    if len(quotes) >= 3:
                        return quotes
    return quotes[:3]

def extract_purpose_py(content, lines):
    # Match first docstring anywhere before main code
    m = re.search(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', content, re.DOTALL)
    if m:
        doc = (m.group(1) or m.group(2)).strip()
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', doc) if s.strip()]
        if sents:
            return " ".join(sents[:2])
    # check comments
    comms = []
    for l in lines[:25]:
        ls = l.strip()
        if ls.startswith("#") and not ls.startswith("#!"):
            comms.append(ls.lstrip("# \t"))
        elif comms and not ls.startswith("#"):
            break
    if comms:
        return " ".join(comms[:2])
    return ""

def extract_key_results(content, lines, kind):
    results = []
    # Metric keywords with numbers
    metric_pattern = re.compile(
        r'\b(?:rmse|mae|std|noise\s*floor|frequency|frequencies|modal|welch|psd|amplitude|dropout|discrepancy|agreement|threshold|snr|damping|drift)\b',
        re.IGNORECASE
    )
    unit_pattern = re.compile(r'\b(?:\d+(?:\.\d+)?)\s*(?:hz|mm|cm|m|deg|rad|db|%|fps|ms|s|rpm)\b', re.IGNORECASE)
    
    for l in lines:
        ls = l.strip()
        if not ls or ls.startswith("```") or ls.startswith("import ") or ls.startswith("from "):
            continue
        # Check if line contains a metric or unit and a number
        has_metric = metric_pattern.search(ls)
        has_unit = unit_pattern.search(ls)
        if (has_metric or has_unit) and re.search(r'\d+(?:\.\d+)?', ls):
            # Clean markdown formatting like bold, table pipes
            clean = ls.strip("| -*#").strip()
            # Split if too long
            parts = [p.strip() for p in re.split(r'(?<!\d)\.(?!\d)|;', clean) if p.strip()]
            for p in parts:
                if (metric_pattern.search(p) or unit_pattern.search(p)) and re.search(r'\d+(?:\.\d+)?', p):
                    words = p.split()
                    if 3 <= len(words) <= 18:
                        # Verify all numbers in p exist in content
                        nums = re.findall(r'\d+(?:\.\d+)?', p)
                        if all(num in content for num in nums):
                            res_str = f'"{p}"'
                            if res_str not in results:
                                results.append(res_str)
                                if len(results) >= 5:
                                    return results
    return results[:5]

