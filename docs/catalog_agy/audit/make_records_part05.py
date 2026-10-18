import os, sys, json, csv
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

csv_path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G1_paper2_core_part05.csv'
with open(csv_path) as f:
    batch_rows = list(csv.DictReader(f))

# Skipped files:
# 71: omrpr-paper2-manuscript.json -> VSCode PR extension storage
# 96: literature-review-prompt.txt -> generic prompt template
# 97: reading-list-prompt.txt -> generic prompt template
# 101: zotero_export.bib -> empty file (0 bytes)
# 136: applet_access_history.json -> Google AI Studio metadata
skipped_dict = {
    '/home/ammar/.config/Code/User/globalStorage/github.vscode-pull-request-github/assignableUsers/ammarajmal/omrpr-paper2-manuscript.json': 
        "third-party IDE extension cache (VSCode GitHub Pull Request plugin metadata, no research content)",
    '/mnt/phd_data/phd_master/98_legacy_imports/career_legacy_paper2_prework/literature-review-prompt.txt':
        "generic prompt template (no project research content)",
    '/mnt/phd_data/phd_master/98_legacy_imports/career_legacy_paper2_prework/reading-list-prompt.txt':
        "generic prompt template (no project research content)",
    '/mnt/phd-legacy/fin_phd/omrpr_manuscript/references/zotero_export.bib':
        "empty file (0 bytes)",
    '/mnt/phd_data/phd_master/02_research_projects/p02_ros_multicamera_shm/p2_new/Paper 2 - Ideas Folder/Google AI Studio/applet_access_history.json':
        "third-party platform access history log (Google AI Studio metadata, no research content)"
}

print(f"Skipped count defined: {len(skipped_dict)}")
