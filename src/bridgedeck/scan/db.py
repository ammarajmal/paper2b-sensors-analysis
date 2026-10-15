"""SQLite cache: resumable, keyed by file content hash + prompt version + model."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .. import paths

SCHEMA = """
CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, label TEXT, rel TEXT, cat TEXT, size INT, mtime TEXT, sha TEXT, skipped TEXT, facts TEXT);
CREATE INDEX IF NOT EXISTS ix_files_sha ON files(sha);
CREATE TABLE IF NOT EXISTS summaries(sha TEXT, ver TEXT, model TEXT, cat TEXT, js TEXT, trust REAL, secs REAL, PRIMARY KEY(sha, ver));
CREATE TABLE IF NOT EXISTS dirs(label TEXT, rel TEXT, ver TEXT, model TEXT, js TEXT, PRIMARY KEY(label, rel, ver));
CREATE TABLE IF NOT EXISTS emb(sha TEXT PRIMARY KEY, model TEXT, vec BLOB);
CREATE TABLE IF NOT EXISTS roots(label TEXT PRIMARY KEY, role TEXT, path TEXT, git TEXT, n_files INT);
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    p = path or (paths.out_dir("scan") / "scan.db")
    con = sqlite3.connect(p)
    con.executescript(SCHEMA)
    return con


def put_file(con, d: dict) -> None:
    con.execute(
        "INSERT OR REPLACE INTO files VALUES(?,?,?,?,?,?,?,?,?)",
        (
            d["path"],
            d["label"],
            d["rel"],
            d["cat"],
            d["size"],
            d["mtime"],
            d["sha"],
            d["skipped"],
            json.dumps(d["facts"]),
        ),
    )
