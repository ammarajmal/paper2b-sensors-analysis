import typer

from . import census

app = typer.Typer(help="bridgedeck-vision-pipeline: gated re-analysis stages", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Stages are subcommands (census, ...)."""


@app.command("census")
def census_cmd(
    set_name: str = typer.Argument(..., help="wtt_main | wtt_5sec | static"),
    limit: int = typer.Option(None, help="only the first N bags (smoke test)"),
):
    df = census.run(set_name, limit)
    typer.echo(f"{len(df)} streams written")


if __name__ == "__main__":
    app()
