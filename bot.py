from twitchio.ext import commands
from dotenv import load_dotenv

from npc_engine import NPCEngine

import sqlite3
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_NICK = os.getenv("BOT_NICK")
CHANNEL = os.getenv("CHANNEL_NAME")

npc = NPCEngine()


class Bot(commands.Bot):

    def __init__(self):

        super().__init__(
            token=TOKEN,
            prefix="!",
            initial_channels=[
                CHANNEL
            ]
        )

    async def event_ready(self):

        print(
            f"{BOT_NICK} connected!"
        )

        print(
            f"Watching: {CHANNEL}"
        )

    async def event_message(
        self,
        message
    ):

        if message.echo:
            return

        username = (
            message.author.name
        )

        content = (
            message.content.strip()
        )

        print(
            f"{username}: {content}"
        )

        npc.process_message(
            username,
            content
        )

        if content.lower() == "!stats":

            conn = sqlite3.connect(
                "memory.db"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT message_count
                FROM viewers
                WHERE username = ?
                """,
                (username,)
            )

            row = cursor.fetchone()

            conn.close()

            if row:

                await message.channel.send(
                    f"@{username} έχεις γράψει {row[0]} μηνύματα στο chat."
                )

            return

        if content.lower().startswith(
            "!ai"
        ):

            question = content[3:].strip()

            if not question:
                return

            reply = npc.maybe_generate_reply(
                username,
                question
            )

            if reply:

                await message.channel.send(
                    reply[:450]
                )

            return

        reply = npc.maybe_generate_reply(
            username,
            content
        )

        if reply:

            await message.channel.send(
                reply[:350]
            )

        await self.handle_commands(
            message
        )


bot = Bot()
bot.run()