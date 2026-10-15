# bridgedeck-vision-pipeline

Gated re-analysis of the 2025 wind-tunnel bridge-deck camera recordings (3 x Sony RX10 IV, AprilTags, ROS1 bags)
and the 2024/2025 laser sessions. One pipeline, one results ledger, three consumers:
Paper 2A (MDPI Sensors), Paper 2B (Elsevier Measurement) and the dissertation chapters.

## Rules
1. Raw data stays where it is and is read-only (`config/paths.yaml`; `paths.assert_not_input` guards writes).
2. A stage may start only after the previous stage's gate passes. Gate criteria are written before the stage runs.
3. A mismatch with published numbers is a finding. Never tune a parameter until it agrees.
4. Manuscript numbers come from `results/ledger.csv` (to be created in stage S3), never typed by hand.
5. Camera intrinsics: use the values stored in the bags' `camera_info` (identical to `omrpr_fin/config/pipeline_config.yaml`).
   They are never selected or adjusted by laser agreement. (Owner decision 2026-10-16.)

## Setup (once)
```bash
cd /mnt/space/adev/projects/active/bridgedeck-vision-pipeline
uv sync                 # creates .venv from pyproject.toml / uv.lock (Python 3.12)
uv run pytest -q        # 3 tests
uv run bvp --help
```
Without uv: `python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pip install -e .`
`requirements.txt` is exported from `uv.lock` (`uv export --no-hashes --no-emit-project > requirements.txt`).

## Layout
| Path | Purpose |
|---|---|
| `src/bridgedeck/` | package: `paths`, `census` (S1), more per stage |
| `config/paths.yaml` | every input/output location |
| `stages/` | stage notes and one-off scripts |
| `results/` | small tracked results (CSV/JSON, ledger) |
| `outputs/` | large generated files (not in git) |
| `docs/` | decisions, reference audit of the older code, stage plan |
| `tests/` | pytest |

## Stages
S1 timing census (done, matches earlier extraction) -> S1b static bags -> S2 detection -> S3 estimators -> S4 pose chain -> S5 laser -> S6 comparison -> S7 figures/ledger.
See `docs/STAGE_PLAN.md`.
