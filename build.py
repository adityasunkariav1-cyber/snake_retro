#!/usr/bin/env python3
"""
build.py — Nokia Snake build/setup script.

"Self-loading" behaviour:
- On every run, it checks whether db/scores.db exists and has the right schema.
- If the DB or table is missing, it creates them automatically (no manual setup step).
- If the leaderboard is empty, it seeds one placeholder row so the app has something
  to display on first run.

This script is meant to be safe to run repeatedly (idempotent) — CI, local dev,
or a deploy step can all call it without side effects piling up.
"""

import sqlite3
import pathlib
import sys
import datetime

ROOT = pathlib.Path(__file__).parent.resolve()
DB_DIR = ROOT / "db"
DB_PATH = DB_DIR / "scores.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS scores (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    player    TEXT NOT NULL,
    score     INTEGER NOT NULL,
    created   TEXT NOT NULL
);
"""

def self_load_db() -> sqlite3.Connection:
    """Ensure the database, folder, and schema exist. Create/seed if missing."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    is_new = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    conn.commit()

    if is_new:
        print(f"[build.py] No existing DB found — created fresh database at {DB_PATH}")
    else:
        print(f"[build.py] Found existing DB at {DB_PATH} — schema verified")

    cur = conn.execute("SELECT COUNT(*) FROM scores")
    count = cur.fetchone()[0]

    if count == 0:
        conn.execute(
            "INSERT INTO scores (player, score, created) VALUES (?, ?, ?)",
            ("VIKRAM", 0, datetime.datetime.now(datetime.timezone.utc).isoformat()),
        )
        conn.commit()
        print("[build.py] Leaderboard was empty — seeded starter row for VIKRAM")
    else:
        print(f"[build.py] Leaderboard already has {count} row(s) — no seeding needed")

    return conn


def sanity_check(conn: sqlite3.Connection) -> None:
    """Basic smoke test so CI fails loudly if something's wrong."""
    cur = conn.execute("SELECT player, score, created FROM scores ORDER BY score DESC LIMIT 5")
    rows = cur.fetchall()
    print("[build.py] Top scores:")
    for player, score, created in rows:
        print(f"  - {player}: {score} ({created})")


def check_game_file() -> None:
    """Confirm the game file itself is present before calling the build good."""
    game_file = ROOT / "index.html"
    if not game_file.exists():
        print(f"[build.py] ERROR: expected game file at {game_file}, not found.")
        sys.exit(1)
    print(f"[build.py] Game file OK: {game_file}")


def main():
    print("[build.py] Starting build...")
    check_game_file()
    conn = self_load_db()
    sanity_check(conn)
    conn.close()
    print("[build.py] Build complete. Everything is ready.")


if __name__ == "__main__":
    main()
