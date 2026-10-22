import sqlite3


def get_recent_messages(limit=20):
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, message
        FROM messages
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    return rows


def get_viewer_stats(username):
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