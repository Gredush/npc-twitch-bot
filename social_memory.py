import sqlite3


class SocialMemory:

    def save_memory(
        self,
        username,
        memory
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (username, memory)
            VALUES (?, ?)
            """,
            (username, memory)
        )

        conn.commit()
        conn.close()

    def get_memories(
        self,
        username,
        limit=10
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT memory
            FROM memories
            WHERE username = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (username, limit)
        )

        rows = cursor.fetchall()

        conn.close()

        return [row[0] for row in rows]

    def memory_exists(
        self,
        username,
        memory
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM memories
            WHERE username = ?
            AND memory = ?
            LIMIT 1
            """,
            (username, memory)
        )

        result = cursor.fetchone()

        conn.close()

        return result is not None