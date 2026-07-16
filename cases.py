from database import (
    get_connection,
)


class CaseService:

    def create_case(self, user_id, title, description=""):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO cases(
                user_id,
                title,
                description,
                created_at
            )
            VALUES (?, ?, ?, DATE('now'))
            """,
            (
                user_id,
                title,
                description
            )
        )

        conn.commit()
        conn.close()

    def get_cases(self, user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                created_at
            FROM cases
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        conn.close()

        return rows


case_service = CaseService()