import typer

from . import census, detect, gates, laser, paths
from .scan.cli import app as scan_app

app = typer.Typer(help="bridgedeck-vision-pipeline: gated re-analysis stages", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Stages are subcommands (census, ...)."""


app.add_typer(scan_app, name="scan")


@app.command("census")
def census_cmd(
    set_name: str = typer.Argument(..., help="wtt_main | wtt_5sec | static"),
    limit: int = typer.Option(None, help="only the first N bags (smoke test)"),
):
    df = census.run(set_name, limit)
    typer.echo(f"{len(df)} streams written")


@app.command("gate-s1")
def gate_s1_cmd():
    """Compare the S1 census with the earlier extraction; write results/gate_S1_report.csv."""
    df = gates.gate_s1()
    out = paths.REPO / "results" / "gate_S1_report.csv"
    df.to_csv(out, index=False)
    bad = df[~df["ok"]]
    typer.echo(f"streams compared: {len(df)}; mismatches: {len(bad)}")
    raise typer.Exit(code=1 if len(bad) else 0)


@app.command("detect")
def detect_cmd(
    set_name: str = typer.Argument("wtt_main"),
    conditions: str = typer.Option(
        "e0_0rpm,e7_90rpm,e14_200rpm", help="comma-separated condition prefixes"
    ),
    workers: int = typer.Option(9),
):
    """Stage S2: detect tags (decode path and detector settings are pinned in docs/gates/S2.md)."""
    df = detect.run(set_name, conditions.split(","), workers)
    typer.echo(f"{len(df)} frames, detected {df['detected'].mean():.4f}")


@app.command("laser")
def laser_cmd():
    """Stage S5a: per-condition laser statistics for both sessions (results/laser_*_by_condition.csv)."""
    for name in laser.SESSIONS:
        df = laser.run_session(name)
        df.to_csv(paths.REPO / "results" / f"laser_{name}_by_condition.csv", index=False)
        typer.echo(f"{name}: {len(df)} conditions")


@app.command("laser-free")
def laser_free_cmd(n_boot: int = typer.Option(500)):
    """Stage S5a criterion 4: reference frequencies from the free-vibration records (no band filter)."""
    import json

    rows = []
    for name in laser.SESSIONS:
        for mode in ("B", "T"):
            r = laser.free_vibration(name, mode)
            typer.echo(
                f"{name} {r['mode']}: f_fit {r['f_fit_hz']:.4f} Hz [{r['f_fit_lo']:.4f}, {r['f_fit_hi']:.4f}]  zeta {r['zeta']:.5f}  fft {r['f_fft_hz']:.4f}  resid/amp {r['resid_over_amp']:.3f}"
            )
            rows.append(r)
    (paths.REPO / "results" / "reference_frequencies_free_vibration.json").write_text(
        json.dumps(rows, indent=1)
    )


if __name__ == "__main__":
    app()
