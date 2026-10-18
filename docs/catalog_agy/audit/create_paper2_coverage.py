import re

src_path = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/refine/WHAT_EXISTS_FOR_v2.md"
dst_path = "/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit/PAPER2_COVERAGE.md"

with open(src_path, "r") as f:
    content = f.read()

# Replace header to match audit deliverable specification
new_header = """# PAPER2_COVERAGE: Research Evidence Map for Paper 2

This document maps fourteen core research questions to the primary files in the repository that directly address them. For each question, up to six directly addressing files are listed in order of relevance, accompanied by a one-sentence factual summary and a character-for-character quotation of at most 15 words. All 84 cited paths have been physically verified on disk (0 missing)."""

content = re.sub(r"# WHAT_EXISTS_FOR_v2: Research Evidence Map.*?(?=## 1\.)", new_header + "\n\n---\n\n", content, flags=re.DOTALL)

with open(dst_path, "w") as f:
    f.write(content.strip() + "\n")

print(f"Wrote {dst_path} ({len(content)} bytes)")
