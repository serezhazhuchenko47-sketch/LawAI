import sqlite3
import json
from datetime import datetime, timedelta

DB_NAME = "lawai.db"

CACHE_DAYS = 30


def init_cache():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_cache(
            query TEXT PRIMARY KEY,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_cache(query):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT result, created_at
        FROM search_cache
        WHERE query = ?
    """, (query.lower(),))

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    result, created_at = row

    created_at = datetime.fromisoformat(created_at)

    if datetime.now() - created_at > timedelta(days=CACHE_DAYS):
        return None

    return json.loads(result)


def save_cache(query, result):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO search_cache
        VALUES(?,?,?)
    """, (
        query.lower(),
        json.dumps(result, ensure_ascii=False),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()