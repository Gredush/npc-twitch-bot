import sqlite3


class NPCMemory:

    def save_npc_message(self, message):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (username, message)
            VALUES (?, ?)
            """,
            (
                "KynigaoBot",
                message
            )
        )

        conn.commit()
        conn.close()