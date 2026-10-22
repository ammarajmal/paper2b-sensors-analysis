# Paper 2 A/B Consolidation and Restart Guide

Date: 2026-10-21

## Current status

The requested consolidation target is:

`/mnt/space/adev/research/publications/paper2_fin`

It has not yet been created because `/mnt/space` is mounted read-only in the current session. No source files were modified.

## Resume after reboot

Open a terminal and run:

```bash
findmnt -T /mnt/space/adev/research/publications -o TARGET,SOURCE,FSTYPE,OPTIONS
ls -ld /mnt/space/adev/research/publications
```

If the mount options include `ro`, remount it read-write:

```bash
sudo mount -o remount,rw /mnt/space
```

Confirm that `rw` is shown:

```bash
findmnt -T /mnt/space/adev/research/publications -o TARGET,SOURCE,FSTYPE,OPTIONS
```

Then create the master directory and symbolic links:

```bash
set -e
base=/mnt/space/adev/research/publications/paper2_fin

mkdir -p "$base/00_CONTROL" \
  "$base/01_paper_A_measurement/revised" \
  "$base/02_paper_B_sensors/revised" \
  "$base/02_paper_B_sensors/audit_outputs" \
  "$base/03_shared_linked_data"

ln -sfn /mnt/phd_data/phd_master/05_publications/p02_measurement_revision_2026-10 \
  "$base/01_paper_A_measurement/master"

ln -sfn /mnt/phd_data/phd_master/05_publications/p02_sensors_mdpi_revision_2026-10 \
  "$base/02_paper_B_sensors/master"

ln -sfn /home/ammar/PAPER2_FINAL_AUDIT_2026-10-01 \
  "$base/02_paper_B_sensors/audit_package"

ln -sfn /home/ammar/Paper2_Sensors_Finalization_2026-10/analysis_outputs \
  "$base/02_paper_B_sensors/audit_outputs/current_reconciliation"

ln -sfn /mnt/phd-legacy/rosbag/WTT \
  "$base/03_shared_linked_data/WTT_main_bags"

ln -sfn /mnt/phd-legacy/rosbag/WTT_5sec \
  "$base/03_shared_linked_data/WTT_5sec_bags"

ln -sfn /mnt/phd-legacy/fin_phd/omrpr_fin/results/step01 \
  "$base/03_shared_linked_data/STEP01_extracted_frames"

ln -sfn /mnt/space/adev/research/phd/phd-research-advisory/03_PACKAGES/chat/CLAUDE_SCIENTIFIC_AUDIT_v3/40_PRIMARY_DERIVED_INPUTS \
  "$base/03_shared_linked_data/derived_inputs"

ln -sfn /mnt/phd_data/phd_master/04_code_software/paper2-rebuild-2026-10_snapshot \
  "$base/03_shared_linked_data/rebuild_code_snapshot"

ln -sfn /mnt/space/adev/research/literature/paper2-acquisition-methods-research \
  "$base/03_shared_linked_data/acquisition_methods_research"
```

## Verify the consolidation

```bash
base=/mnt/space/adev/research/publications/paper2_fin
find "$base" -maxdepth 3 -type l -printf '%p -> %l\n' | sort
find "$base" -maxdepth 3 -type l -exec test -e {} \; -printf 'OK %p\n'
du -sh "$base"
```

The large ROS bags and extracted frames must remain links, not copied data.

## Next work session

1. Create a source inventory and SHA-256 manifest for manuscript, supplement, figures, scripts, and audit outputs.
2. Treat the Paper A `master` tree as the Paper A source tree.
3. Treat the Paper B `master` tree as the current Paper B working source, pending explicit freeze.
4. Use each `revised/` directory only for deliberate manuscript revisions.
5. Do not edit raw bags, extracted frames, frozen audit tables, or canonical evidence.
6. Re-run the Paper 2 claim ledger and discrepancy review before any manuscript wording changes.

## Important distinction

The consolidation directory is a controlled navigation and working root. The linked source locations remain the physical data authorities. Do not delete or rename the original source directories after creating the links.
