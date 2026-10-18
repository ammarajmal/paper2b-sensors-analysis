def find_verbatim_quote(content, keywords=None):
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    # If keywords provided, try to find a line containing keywords
    if keywords:
        for kw in keywords:
            for l in lines:
                if kw in l:
                    words = l.split()
                    if 3 <= len(words) <= 15:
                        return " ".join(words) if " ".join(words) in content else l[:80]
                    elif len(words) > 15:
                        # try slice of 10 words
                        for start in range(len(words) - 9):
                            sub = " ".join(words[start:start+10])
                            if sub in content:
                                return sub
    # Fallback to any good line
    for l in lines:
        words = l.split()
        if 4 <= len(words) <= 12 and l in content:
            return l
    # Fallback to first line
    for l in lines:
        if len(l.split()) <= 15 and l in content:
            return l
    return ""
