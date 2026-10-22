# Marker identity reconciliation (NF-1 / OD-4)

**Verdict: resolved by owner decision (recorded 2026-10-22).** The earlier conflict between two owner statements
(center/near-center versus offset/near-axis) is closed. The owner confirmed the assignment below. The
manuscript's current wording (cam1/cam2 on the center/near-center marker, cam3 on the off-center/side marker)
is the reversed one and must be replaced when manuscript edits begin. No `.tex`, manuscript, supplement or
audit file was edited here. Row-level evidence is in `MARKER_IDENTITY_RECONCILIATION.tsv` (items MK01-MK12).

## 0. Owner-confirmed marker assignment

| Camera(s) | Physical marker | Handwritten label | Decoded AprilTag |
|---|---|---|---|
| cam1 and cam2 | the **same** side / off-center marker | `ID-0-1` | tag36h11 ID 0 |
| cam3 | a **distinct** centre marker | `ID-0-2` | tag36h11 ID 0 |

Consequences that apply everywhere in Paper 2B documentation:

- Both markers decode as AprilTag ID 0. The machine-decoded ID alone does not distinguish them. Camera identity
  and the handwritten labels do.
- The exact physical separation between the two markers was not surveyed. No separation value is quoted.
- cam1/cam2 vertical metric motion (H1,y) includes a lever-arm x roll term and must not be called direct heave.
- Any near-axis statement about the cam3 lever arm must stay data-derived and qualified (section 3). It is an
  estimate from the torsion-line data, not a surveyed distance.

Sources, as you listed them: `analysis/paper2b/per_camera_rms_audit/` and audit-package `08_PROVENANCE/` files
11, 12, 13, 14 and 39B. For the data-derived check I also used `results/s4_roll_and_lever_arm_at_torsion_line.csv`,
`docs/gates/S4.md`, `docs/gates/S5a.md` and `docs/reference_audit/NOTES.md` F1, because they hold the only measured
evidence on the distance-from-axis question. 39B contains nothing about marker identity (it concerns 2024 camera
reproduction), so it adds no evidence here.

## 1. What is verified

| Statement | Status | Evidence |
|---|---|---|
| cam1 and cam2 view the **same** physical marker | VERIFIED | identical framing in all sampled frames (11 rows 2-3); every source agrees (12 Q1; 13 rows 5-6) |
| cam3 views a **different** physical marker | VERIFIED | 11 row 4; 12 Q2; 13 row 7 |
| Both markers decode AprilTag tag36h11 **ID 0**; the decoded ID cannot tell them apart | VERIFIED | 113,852 valid rows, code assertion `EXPECTED_TAG = {0,0,0}` (12 Q3-Q4; 11 rows 5-10) |
| Handwritten labels: cam1/cam2 = `ID-0-1`, cam3 = `ID-0-2` | OWNER-ATTESTED | owner frame review 2026-09-07 (14, mapping table), 2026-10-15 (`docs/DECISIONS.md`) and the 2026-10-22 confirmation. The digits are not legible in the audit's contact sheet (OCR confidence low; 12 lists the digit-to-camera pairing as UNRESOLVED from photos alone) |
| cam1/cam2 marker is the side / off-center marker; cam3 marker is the centre marker | OWNER-CONFIRMED (2026-10-22) | consistent with the data-derived distances in section 3 |

## 2. How the earlier conflict resolved

| Source | cam1/cam2 marker (`ID-0-1`) | cam3 marker (`ID-0-2`) | Status now |
|---|---|---|---|
| Audit package 14 and 13 (owner, 2026-09-07; also the manuscript) | center/near-center | off-center/side | **superseded, reversed** |
| SVR manifests (12, 11) | "documented center marker" | "documented side marker" | **superseded, reversed**; these descriptors must not be ported |
| `docs/DECISIONS.md` 2026-10-15 (owner, "checked images"); `NOTES.md` F1 | offset | near-axis | **confirmed** by the owner, with wording below |
| Owner confirmation 2026-10-22 | side / off-center | centre | **governing** |

The 2026-10-15 statement was right about which marker is which. The words "offset" and "near-axis" are still not
used as unqualified fact, because the distances behind them are estimates (section 3).

## 3. What the data say (independent of the labels)

At the torsion line, vertical amplitude divided by in-plane roll estimates each marker's apparent distance from
the rotation axis (`results/s4_roll_and_lever_arm_at_torsion_line.csv`, six conditions: 90, 140, 160, 180, 200,
220 RPM):

| Camera | median (mm) | range (mm) |
|---|---|---|
| cam1 | 127.0 | 117.9 - 134.5 |
| cam2 | 125.4 | 116.6 - 132.5 |
| cam3 | 5.9 | 1.4 - 14.2 |

All three cameras measure the same roll within 2% (cam2/cam1 1.014, cam3/cam1 1.009), which is what one rigid
rotation seen by all three cameras would give. This agrees with the owner-confirmed assignment (cam3 much closer to
the rotation axis than cam1/cam2). It remains an estimate: it assumes rigid rotation about a fixed axis, uses six
conditions, drifts with RPM (cam1 falls from about 135 to 118 mm), carries a 2.5% tag-size scale bound, and
measures distance from the rotation axis, not the physical separation between the two markers.

## 4. Answers to the questions

1. **Which camera views which marker?** cam1 and cam2 view one marker (side / off-center, `ID-0-1`); cam3 views
   another (centre, `ID-0-2`). *Verified for the same/different split; location owner-confirmed.*
2. **Is each label verified, inferred or unresolved?** Same/different marker: verified. `ID-0-1`/`ID-0-2` and the
   side/centre locations: owner-attested and owner-confirmed. Distance from the axis: data-derived estimate.
3. **Are "Marker A" and "Marker B" safe manuscript labels?** **No.** They come from the SVR manifests, whose
   location descriptors are reversed relative to the owner-confirmed assignment, and `NOTES.md` F1 says not to
   port those names. The current Table 3 caption uses "(Marker A)"; replace it when edits begin.
4. **May cam3 be called near-axis?** Only as a data-derived, qualified statement: "its apparent distance from the
   rotation axis, estimated from the data and not surveyed, is small (about 6 mm median)". Do not state a surveyed
   or exact near-axis geometry.
5. **Is any lever-arm distance verified?** No. About 125 mm (cam1/cam2) and about 6 mm (cam3) are data-derived
   estimates. The 135.14 mm separation is retracted (2024 photograph, different geometry), 200 mm is an unverified
   report, and no survey exists (14, "What remains unresolved" item 4; `NOTES.md` F13).

## 5. Approved labels

| Use | Instead of |
|---|---|
| cam1/cam2 **side / off-center marker**, handwritten label `ID-0-1` | center/near-center marker, "Marker A" |
| cam3 **centre marker**, handwritten label `ID-0-2` | off-center/side marker, "Marker B" |
| "both markers decode as AprilTag ID 0" | "tag 1"/"tag 2", "marker ID" for the handwritten label |
| "apparent distance from the rotation axis, estimated from the data" | "lever arm of N mm" unless labelled an estimate |
| "vertical metric motion of the side/off-center marker" | "heave" (for cam1/cam2) |

Where the existing manuscript says center/near-center or off-center/side (tex lines 190-193, 254-258, 696-698,
797-799 in the audit-package copy, plus the Table 3 caption "Marker A"), the revision must swap in the approved
labels. No result number depends on this, since every spectral feature is computed per camera (TSV MK10). The
cam3 90-RPM divergence stays unranked and unexplained (TSV MK11).

## 6. Effect on earlier documents

`PER_CAMERA_RMS_MANUSCRIPT_SCOPE_DECISION.md` section 5 and `UPDATED_MANUSCRIPT_INTEGRATION_OPEN_ITEMS.md` NF-1
are updated to this assignment. The Antigravity validation (CHK-CAM-01, CHK-CAM-06) stated cam1/cam2 as the
"offset marker" and cam3 as the "near-axis marker" as fact. The assignment turned out to be right, but those
checks did not establish it. They are now read as consistent with the owner decision, not as independent proof.

## 7. Remaining items

OD-4 is closed. Still open: correct the dataset `metadata.yaml` field `marker_ids: [0, 1, 2]` (contradicted by all
other sources), and, if a surveyed separation is ever wanted, take a legible photograph or measurement of both
markers relative to the rotation axis.

## 8. Housekeeping

Antigravity created root-level copies `MANUSCRIPT_SCOPE_VALIDATION.md` and `.tsv`. I confirmed with `cmp` that they
were byte-identical to the copies in `docs/paper2b/` and deleted the root copies. The canonical files remain in
`docs/paper2b/`, nothing committed.
