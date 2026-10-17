# S8 number check summary

Ledger rows 5007; P1 empty fields 0; recompute mismatches 0.

## Curated claims (results/claims_map.csv)

| id | printed | rebuilt value | status | relation | description |
|---|---|---|---|---|---|
| M01 | 0.9711 | 0.9717 | DIFFER | ANALOGUE | bending Pearson r on 16 regime-interior conditions (R002) |
| M02 | 0.288 | 0.2802 | DIFFER | ANALOGUE | bending RMSE mm on 16 conditions |
| M03 | 0.205 | 0.2005 | DIFFER | ANALOGUE | bending MAE mm on 16 conditions |
| M04 | 1.217 | 1.1375 | DIFFER | ANALOGUE | mean camera/LDS bending ratio on 16 conditions |
| M05 | 0.9682 | 0.9673 | DIFFER | ANALOGUE | torsion-proxy Pearson r on 16 conditions (R004) |
| M06 | 0.830 | 0.8132 | DIFFER | ANALOGUE | mean camera/LDS torsion ratio on 16 conditions |
| M07 | 0.6307 | 0.6266 | DIFFER | ANALOGUE | bending Pearson r all 19 conditions (R001) |
| M08 | 0.2930 | 0.2995 | DIFFER | ANALOGUE | torsion-proxy Pearson r all 19 conditions (R003) |
| M09 | 0.9294 | 0.9294 | AGREE | ANALOGUE | bending Spearman rho on 16 conditions |
| M10 | 0.9676 | 0.9676 | AGREE | ANALOGUE | torsion Spearman rho on 16 conditions |
| M11 | 0.718 | 0.7277 | DIFFER | CANDIDATE_DEFINITION | torsion regression slope (R005; definition not stated; candidate OLS) |
| M12 | 1.4323 | 1.4318 | DIFFER | ANALOGUE | bending natural frequency Hz (facility log decrement per paper) |
| M13 | 3.0827 | 3.0982 | DIFFER | ANALOGUE | torsion natural frequency Hz (facility log decrement per paper) |
| M14 | 24.7 | 24.6996 | AGREE | SAME_QUANTITY | largest single-frame gap ms (cam1 value in the ledger) |
| M15 | 1.4290 |  | NOT_IN_LEDGER | NOT_IN_LEDGER | camera FFT free-vibration frequency Hz |
| M16 | 1.4303 |  | NOT_IN_LEDGER | NOT_IN_LEDGER | facility-quoted vertical frequency Hz |
| S01 | 60.00 | 60.0002 | AGREE | SAME_QUANTITY | cam3 effective frame rate Hz |
| S02 | 59.998 | 59.9969 | DIFFER | SAME_QUANTITY | cam3 lowest per-stream mean rate Hz |
| S03 | 60.014 | 60.0013 | DIFFER | SAME_QUANTITY | cam3 highest per-stream mean rate Hz |
| S04 | 59.94 | 59.9414 | AGREE | SAME_QUANTITY | cam1 and cam2 effective frame rate Hz (cam1 median in ledger) |
| S05 | 59.925 | 59.9309 | DIFFER | SAME_QUANTITY | cam2 lowest per-stream mean rate Hz |
| S06 | 59.956 | 59.9545 | DIFFER | SAME_QUANTITY | cam1 highest per-stream mean rate Hz |

## Full scan of decimal numbers (VALUE_IN_LEDGER = equal at the printed precision to some ledger value; coincidence is likely at 1-2 decimals)

| manuscript | decimals | in ledger | not in ledger |
|---|---|---|---|
| measurement | 1 | 49 | 35 |
| measurement | 2 | 193 | 46 |
| measurement | 3 | 234 | 128 |
| measurement | 4+ | 17 | 73 |
| sensors | 1 | 31 | 8 |
| sensors | 2 | 82 | 6 |
| sensors | 3 | 134 | 38 |
| sensors | 4+ | 246 | 49 |
