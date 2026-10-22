import sqlite3


class RelationshipManager:

    def get_viewer_info(self, username):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                username,
                message_count,
                first_seen,
                last_seen
            FROM viewers
            WHERE username = ?
            """,
            (username,)
        )

        result = cursor.fetchone()

        conn.close()

        return result

    def viewer_role(self, username):

        if username.lower() == "gredush":
            return "streamer"

        info = self.get_viewer_info(username)

        if not info:
            return "new_viewer"

        count = info[1]

        if count >= 500:
            return "veteran"

        if count >= 100:
            return "regular"

        return "new_viewer"