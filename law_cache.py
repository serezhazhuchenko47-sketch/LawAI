import sqlite3

DB_NAME = "law_cache.db"


def init_cache():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laws(
            key TEXT PRIMARY KEY,
            title TEXT,
            text TEXT,
            updated TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_cached(key):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, text FROM laws WHERE key=?",
        (key,)
    )

    row = cursor.fetchone()

    conn.close()

    return row


def save_cache(key, title, text):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO laws
        VALUES (?, ?, ?, datetime('now'))
    """, (key, title, text))

    conn.commit()
    conn.close()