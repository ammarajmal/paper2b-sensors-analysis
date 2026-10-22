# Paper 2B marker-identity owner decision

**Status:** owner-confirmed visual decision, 2026-10-22.

Manual review of the extracted camera images resolves the camera-to-marker
identity used by the revised manuscript:

- cam1 and cam2 view the same physical marker on the side/off-center portion of
  the bridge model, slightly left of the model centre in the reviewed view. Its
  handwritten human label is `ID-0-1`.
- cam3 views a distinct physical marker placed at the centre of the bridge
  model. Its handwritten human label is `ID-0-2`.
- Both physical markers decode as AprilTag ID 0. The decoded machine ID alone
  therefore does not distinguish them; camera identity, reviewed imagery, and
  the handwritten labels provide the distinction.

This decision does not provide a physical survey of the marker separation or a
validated lever-arm length. Statements about apparent near-axis behaviour or
relative marker amplitude remain data-derived interpretations. The manuscript
therefore uses `side/off-center marker` for cam1/cam2 and `centre marker` for
cam3, while retaining the restriction that cam1/cam2 vertical metric motion is
not direct heave.

The original audit-package manuscript and supplement are preserved. This file
governs the editable revision copy in this directory.

## Mirror note

Mirrored from the editable manuscript tree
(`02_paper_B_sensors/working/MARKER_IDENTITY_OWNER_DECISION.md`) on 2026-10-22.
Bootstrap settings in the per-camera RMS report were checked against
`analysis/paper2b/per_camera_rms/run_per_camera_rms.py` (10,000 resamples,
seed 0); no stale seed prose was found.
This decision supersedes earlier "near-axis / far marker" wording in
`MARKER_IDENTITY_RECONCILIATION.md` where the two differ.
