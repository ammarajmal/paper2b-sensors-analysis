VER = "v2"
TAGS = "acquisition, timing, detection, calibration, pose, fusion, spectral, laser, comparison, uncertainty, figures, manuscript, governance, ros, utility, test, data-prep, other"
SYSTEM = (
    "You catalogue research files for a PhD student who needs to know what was already done, so nothing is repeated or lost. "
    "Use ONLY the file content and the computed facts. Never guess numbers, results or file contents that are not shown. "
    "If something is unclear write 'unclear'. Output a single JSON object and nothing else."
)

CODE = """FILE: {rel}
TREE: {label} ({role})
COMPUTED FACTS (trustworthy): {facts}

CONTENT (may be truncated):
<<<
{content}
>>>

Return JSON with exactly these keys:
"purpose": 1-2 sentences, what the file does;
"method": list of up to 6 short strings (algorithms, steps, estimators actually used);
"inputs": list of files/data it reads (names as written in the code);
"outputs": list of files/figures/tables it writes;
"parameters": list of up to 8 "NAME=value" strings copied from the code;
"status": one of complete, partial, stub, debug, superseded, unknown;
"tags": up to 4 from [{tags}];
"paper_relevance": one of 2A-spectral, 2B-comparison, dissertation, paper1, background, none, unknown;
"open_questions": list of up to 3 things the file leaves unresolved or assumes without checking (units, mappings, calibration, unfinished parts); empty list if none;
"evidence": list of 2-4 EXACT quotes (max 12 words each, copied character for character from CONTENT) that support "purpose"."""

DOC = """FILE: {rel}
TREE: {label} ({role})
COMPUTED FACTS (trustworthy): {facts}

CONTENT (may be truncated):
<<<
{content}
>>>

Return JSON with exactly these keys:
"summary": 2-3 sentences;
"key_findings": list of up to 6 short statements the document makes (only what the text says);
"numbers": list of up to 8 objects {{"quantity": ..., "value": "number with unit exactly as written in the text", "context": short}}; only measured or computed results and parameter values, never line counts, dates or section numbers;
"decisions": list of decisions or rules stated (up to 5);
"mentions_files": list of file or script names mentioned (up to 8);
"status": one of final, draft, superseded, plan, report, notes, unknown;
"tags": up to 4 from [{tags}];
"paper_relevance": one of 2A-spectral, 2B-comparison, dissertation, paper1, background, none, unknown;
"open_questions": list of up to 3 open issues or unverified assumptions the document itself states;
"evidence": list of 2-4 EXACT quotes (max 12 words each, copied character for character from CONTENT) that support "summary"."""

DIR = """FOLDER: {rel} in tree {label} ({role})
FILES (name: purpose [status; tags]):
{items}

Return JSON with keys:
"what_it_does": 2-3 sentences describing this folder as a whole, only from the list;
"pipeline_role": one of acquisition, detection, calibration, pose, spectral, laser, comparison, uncertainty, figures, manuscript, governance, utility, mixed, unclear;
"key_files": up to 5 file names that matter most;
"overlaps": file names that appear to repeat each other;
"gaps": things the list suggests were planned or referenced but have no file here (or 'none visible')."""

ASK = (
    "You answer questions about a PhD student's older research files using ONLY the numbered catalogue entries given. "
    "Cite entries as [n]. If the entries do not answer the question, say so. Do not invent results."
)
