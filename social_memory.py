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
            (
                username,
                memory
            )
        )

        row = cursor.fetchone()

        conn.close()

        return row is not None

    def get_memories(
        self,
        username,
        limit=20
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
            (
                username,
                limit
            )
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            row[0]
            for row in rows
        ]

    def get_relevant_memories(
        self,
        username,
        current_message,
        limit=5
    ):

        memories = self.get_memories(
            username,
            50
        )

        text = current_message.lower()

        relevant = []

        for memory in memories:

            memory_words = (
                memory.lower()
                .split()
            )

            for word in memory_words:

                if (
                    len(word) > 3
                    and word in text
                ):

                    relevant.append(
                        memory
                    )

                    break

        if relevant:

            return relevant[:limit]

        return memories[:limit]