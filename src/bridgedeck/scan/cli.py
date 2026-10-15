"""`bvp scan ...` subcommands. Everything is local (Ollama on 127.0.0.1) and read-only on the scanned trees."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .. import paths
from . import ask as ask_mod
from . import db, llm, prompts, results_index, summarize, synth, walk

app = typer.Typer(help="Offline repository scan with a local model", no_args_is_help=True)
DEFAULT_MODEL = "qwen3:14b"
EMBED_MODEL = "qwen3-embedding:4b"


@app.command()
def inventory(only: str = typer.Option(None, help="only roots whose label matches this text")):
    """Stage 1: list files, hash, deterministic facts, git state (no model needed)."""
    cfg = walk.load_roots()
    con = db.connect()
    for r in cfg["roots"]:
        if only and only not in r["label"]:
            continue
        if not Path(r["path"]).exists():
            typer.echo(f"MISSING {r['label']}: {r['path']}")
            continue
        n = 0
        for d in walk.walk_root(r, cfg):
            db.put_file(con, d)
            n += 1
        con.execute(
            "INSERT OR REPLACE INTO roots VALUES(?,?,?,?,?)",
            (r["label"], r["role"], r["path"], json.dumps(walk.git_info(Path(r["path"]))), n),
        )
        con.commit()
        typer.echo(f"{r['label']}: {n} files")
    u = con.execute(
        "SELECT COUNT(DISTINCT sha) FROM files WHERE skipped='' AND cat IN ('code','doc')"
    ).fetchone()[0]
    typer.echo(f"unique code/doc files to summarise: {u}")


@app.command()
def summarise(
    model: str = DEFAULT_MODEL,
    limit: int = typer.Option(None),
    only: str = typer.Option(None, help="regex on file path"),
):
    """Stage 2: model summaries with evidence-quote verification (resumable)."""
    if model not in llm.available_models():
        raise typer.BadParameter(f"{model} not installed; have {llm.available_models()}")
    cfg = walk.load_roots()
    con = db.connect()
    typer.echo(summarize.run(con, cfg, model, limit, only))


@app.command()
def folders(model: str = DEFAULT_MODEL, min_files: int = 3):
    """Stage 3: folder-level syntheses."""
    cfg = walk.load_roots()
    con = db.connect()
    typer.echo(f"{synth.folder_summaries(con, cfg, model, min_files)} folder summaries")


@app.command()
def embed(model: str = EMBED_MODEL):
    """Embed summaries for semantic search and similar-file lookup."""
    con = db.connect()
    typer.echo(f"{summarize.embed_all(con, model)} embeddings")


@app.command()
def results(
    roots: list[str] = typer.Argument(None, help="label=path pairs; default: known result trees"),
):
    """Index result folders (CSV headers, JSON keys, scripts that name the files). Deterministic."""
    con = db.connect()
    producers: dict[str, list[str]] = {}
    for rel, facts in con.execute("SELECT rel, facts FROM files WHERE cat='code'"):
        for lit in json.loads(facts).get("path_literals", []):
            producers.setdefault(Path(lit).name, []).append(rel)
    P = paths.load()["phd_root"]
    defaults = [
        (
            "omrpr_fin_results",
            Path(P, "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin/results"),
        ),
        (
            "omrpr_fin_wtt5sec",
            Path(P, "98_legacy_imports/source_mnt_phd_fin_phd/omrpr_fin/results_wtt5sec"),
        ),
        (
            "svr_evidence",
            Path(
                P,
                "02_research_projects/p02_ros_multicamera_shm/structural_vision_research/evidence",
            ),
        ),
        (
            "omrpr_analysis_outputs",
            Path(P, "02_research_projects/p04_offline_pose_reconstruction/omrpr_analysis/outputs"),
        ),
        ("p00_results", Path(P, "02_research_projects/P00_shm-displacement-project/data/results")),
        (
            "github_results",
            Path(P, "04_code_software/github/shm-displacement-project/data/results"),
        ),
        (
            "p03_data",
            Path(P, "02_research_projects/p03_windtunnel_bridgedeck/experimental_analysis/data"),
        ),
    ]
    pairs = [tuple(r.split("=", 1)) for r in roots] if roots else defaults
    rows = results_index.index_results(
        [(a, Path(b)) for a, b in pairs if Path(b).exists()], producers
    )
    import csv

    out = paths.REPO / "docs/catalog"
    out.mkdir(exist_ok=True, parents=True)
    with open(out / "results_index.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    typer.echo(f"{len(rows)} result folders indexed -> docs/catalog/results_index.csv")


@app.command()
def render():
    """Write docs/catalog/INDEX.md, CATALOG_<tree>.md and catalog.csv."""
    cfg = walk.load_roots()
    con = db.connect()
    typer.echo(synth.write_catalog(con, cfg, paths.REPO / "docs/catalog"))


@app.command()
def ask(question: str, chat_model: str = DEFAULT_MODEL, k: int = 8):
    """Ask what was already done, e.g. 'what spectral estimators were tried?'. Answers cite catalogue entries."""
    con = db.connect()
    typer.echo(ask_mod.answer(con, question, chat_model, EMBED_MODEL, k))


@app.command()
def status():
    """Counts and trust distribution."""
    con = db.connect()
    q = lambda s: con.execute(s).fetchone()[0]  # noqa: E731
    unique = con.execute(
        "select count(distinct sha) from files where skipped='' and cat in ('code','doc')"
    ).fetchone()[0]
    done = con.execute("select count(*) from summaries where ver=?", (prompts.VER,)).fetchone()[0]
    typer.echo(
        f"files {q('select count(*) from files')} | unique code/doc {unique} | summarised {done}"
    )
    tr = [r[0] for r in con.execute("select trust from summaries where ver=?", (prompts.VER,))]
    if tr:
        import statistics

        typer.echo(
            f"trust: mean {statistics.mean(tr):.2f}, share >=0.5: {sum(t >= 0.5 for t in tr) / len(tr):.0%}, zero: {sum(t == 0 for t in tr)}"
        )
