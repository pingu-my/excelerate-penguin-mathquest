"""SQLite persistence for one server with a persistent disk; no CSV races."""
import sqlite3, os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

def connect():
    path=Path(os.getenv('MATHQUEST_DB','data/leaderboard.sqlite3'))
    path.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(path,timeout=20)
    con.row_factory=sqlite3.Row
    con.execute('''CREATE TABLE IF NOT EXISTS results (
    run_id TEXT PRIMARY KEY, name TEXT NOT NULL, primary_year INTEGER,
    syllabus TEXT, topic TEXT, mode TEXT, score INTEGER, correct INTEGER,
    questions INTEGER, accuracy REAL, best_streak INTEGER, completed_at TEXT)''')
    return con

def save(run_id,profile,stats):
    with connect() as con:
        con.execute('INSERT OR IGNORE INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
          (run_id,profile['name'],profile['year'],profile['syllabus'],profile['topic'],profile['mode'],
           stats['score'],stats['correct'],stats['questions'],stats['accuracy'],stats['best_streak'],
           datetime.now(ZoneInfo('Asia/Kuching')).isoformat(timespec='seconds')))

def rows(profile):
    with connect() as con:
        records=con.execute('''SELECT * FROM results WHERE primary_year=? AND syllabus=? AND topic=? AND mode=?
          ORDER BY score DESC, accuracy DESC, completed_at ASC''',
          (profile['year'],profile['syllabus'],profile['topic'],profile['mode'])).fetchall()
    return [dict(r) for r in records]
