import csv, os, sys, json, hashlib
sys.path.append('/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit')
from verify_quote import verify_record

csv_path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/audit_batches/G1_paper2_core_part05.csv'
with open(csv_path) as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in G1 part05: {len(rows)}")

# Let's see what rows are skipped according to Subagent 1:
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

print("Skipped candidates:", len(skipped_dict))
