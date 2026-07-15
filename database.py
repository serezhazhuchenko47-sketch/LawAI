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
            name TEXT,
            register_date TEXT,
            tariff TEXT DEFAULT 'FREE',
            consultations INTEGER DEFAULT 0,
            documents_created INTEGER DEFAULT 0,
            documents_checked INTEGER DEFAULT 0,
            language TEXT DEFAULT 'Українська'
        )
    """)

    # Якщо база вже існувала — додаємо відсутні колонки
    columns = [
        ("register_date", "TEXT"),
        ("tariff", "TEXT DEFAULT 'FREE'"),
        ("consultations", "INTEGER DEFAULT 0"),
        ("documents_created", "INTEGER DEFAULT 0"),
        ("documents_checked", "INTEGER DEFAULT 0"),
        ("language", "TEXT DEFAULT 'Українська'")
    ]

    cursor.execute("PRAGMA table_info(users)")
    existing = [row[1] for row in cursor.fetchall()]

    for column, sql_type in columns:
        if column not in existing:
            cursor.execute(
                f"ALTER TABLE users ADD COLUMN {column} {sql_type}"
            )

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

from datetime import datetime


def create_user(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT register_date FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if row is None:

        cursor.execute("""
            INSERT INTO users(
                user_id,
                register_date,
                tariff,
                consultations,
                documents_created,
                documents_checked,
                language
            )
            VALUES(
                ?, ?, 'FREE', 0, 0, 0, 'Українська'
            )
        """, (
            user_id,
            datetime.now().strftime("%d.%m.%Y")
        ))

    elif row[0] is None:

        cursor.execute("""
            UPDATE users
            SET register_date=?
            WHERE user_id=?
        """, (
            datetime.now().strftime("%d.%m.%Y"),
            user_id
        ))

    conn.commit()
    conn.close()


def get_user(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        history,
        register_date,
        tariff,
        consultations,
        documents_created,
        documents_checked,
        language
    FROM users
    WHERE user_id=?
""", (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
    "name": row[0] or "Невідомо",
    "register_date": row[2] or "-",
    "tariff": row[3] or "FREE",
    "consultations": row[4] or 0,
    "documents_created": row[5] or 0,
    "documents_checked": row[6] or 0,
    "language": row[7] or "Українська"
}

def increment_consultations(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET consultations = consultations + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def increment_documents_created(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET documents_created = documents_created + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def increment_documents_checked(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET documents_checked = documents_checked + 1
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

def get_statistics():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN tariff='PRO' THEN 1 ELSE 0 END),
            SUM(consultations),
            SUM(documents_created),
            SUM(documents_checked)
        FROM users
    """)

        row = cursor.fetchone()

        conn.close()

        return {
        "users": row[0] or 0,
        "pro": row[1] or 0,
        "consultations": row[2] or 0,
        "documents_created": row[3] or 0,
        "documents_checked": row[4] or 0
    }
   
def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            name,
            tariff,
            register_date
        FROM users
        ORDER BY user_id
    """)

    users = cursor.fetchall()

    conn.close()

    return users