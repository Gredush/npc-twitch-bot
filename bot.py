from twitchio.ext import commands
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_NICK = os.getenv("BOT_NICK")
CHANNEL = os.getenv("CHANNEL_NAME")


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f"{BOT_NICK} connected!")
        print(f"Watching: {CHANNEL}")

    async def event_message(self, message):

        if message.echo:
            return

        username = message.author.name
        content = message.content

        print(f"{username}: {content}")

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        # Αποθήκευση μηνύματος
        cursor.execute(
            """
            INSERT INTO messages (username, message)
            VALUES (?, ?)
            """,
            (username, content)
        )

        # Έλεγχος αν υπάρχει viewer profile
        cursor.execute(
            """
            SELECT username
            FROM viewers
            WHERE username = ?
            """,
            (username,)
        )

        viewer = cursor.fetchone()

        if viewer is None:
            cursor.execute(
                """
                INSERT INTO viewers
                (username, message_count)
                VALUES (?, 1)
                """,
                (username,)
            )

            print(f"New viewer detected: {username}")

        else:
            cursor.execute(
                """
                UPDATE viewers
                SET
                    message_count = message_count + 1,
                    last_seen = CURRENT_TIMESTAMP
                WHERE username = ?
                """,
                (username,)
            )

        conn.commit()
        conn.close()

        if content.lower() == "!stats":

            conn = sqlite3.connect("memory.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT message_count
                FROM viewers
                WHERE username = ?
                """,
                (username,)
            )

            result = cursor.fetchone()

            conn.close()

            if result:
                await message.channel.send(
                    f"@{username} έχεις γράψει {result[0]} μηνύματα στο chat."
                )

        if "kalimera" in content.lower():
            await message.channel.send(
                f"Kalimera @{username}!"
            )

        await self.handle_commands(message)


bot = Bot()
bot.run()