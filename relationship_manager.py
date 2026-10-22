import sqlite3
from datetime import datetime
from affinity_manager import AffinityManager


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

        info = self.get_viewer_info(
            username
        )

        if not info:
            return "new_viewer"

        count = info[1]

        affinity = (
            AffinityManager()
            .get_score(username)
        )

        if affinity >= 100:
            return "close_friend"

        if count >= 500:
            return "veteran"

        if count >= 100:
            return "regular"

        return "new_viewer"

    def returning_viewer_days(
        self,
        username
    ):

        info = self.get_viewer_info(
            username
        )

        if not info:
            return 0

        last_seen = info[3]

        if not last_seen:
            return 0

        try:

            last_seen_dt = (
                datetime.fromisoformat(
                    last_seen
                )
            )

            return (
                datetime.now()
                - last_seen_dt
            ).days

        except Exception:
            return 0