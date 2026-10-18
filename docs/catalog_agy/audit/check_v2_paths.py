import os, re

prefix = '/mnt/phd_data/phd_master/'
path = '/mnt/space/adev/projects/active/bridgedeck-vision-pipeline/docs/catalog_agy/refine/WHAT_EXISTS_FOR_v2.md'

with open(path) as f:
    text = f.read()

matches = re.findall(r'\*\*`([^`]+)`\*\*', text)
print(f'Total paths found: {len(matches)}')

missing = []
for m in matches:
    full = os.path.join(prefix, m)
    if not os.path.exists(full):
        missing.append((m, full))

print(f'Missing paths: {len(missing)}')
for m, full in missing:
    print('  FAIL:', m)
