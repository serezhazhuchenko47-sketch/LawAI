import sqlite3

DB_NAME = "lawai.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_name(user_id: int, name: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users(user_id, name)
        VALUES(?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET name=excluded.name
    """, (user_id, name))

    conn.commit()
    conn.close()


def get_name(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None