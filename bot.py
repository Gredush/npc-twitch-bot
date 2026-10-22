from twitchio.ext import commands
from dotenv import load_dotenv

from ai.brain import generate_reply
from ai.should_reply import should_reply

from npc_state import NPCState
from npc_memory import NPCMemory

from social_memory import SocialMemory
from memory_extractor import MemoryExtractor

import os
import sqlite3

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_NICK = os.getenv("BOT_NICK")
CHANNEL = os.getenv("CHANNEL_NAME")

npc_state = NPCState()
npc_memory = NPCMemory()

social_memory = SocialMemory()
memory_extractor = MemoryExtractor()


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
        content = message.content.strip()

        print(f"{username}: {content}")

        npc_state.register_message()

        # ======================
        # MEMORY EXTRACTION
        # ======================

        try:

            memory = memory_extractor.extract(
                username,
                content
            )

            if memory:

                if not social_memory.memory_exists(
                    username,
                    memory
                ):

                    social_memory.save_memory(
                        username,
                        memory
                    )

                    print(
                        f"NEW MEMORY: {username} -> {memory}"
                    )

        except Exception as e:

            print("MEMORY ERROR:", e)

        # ======================
        # SAVE USER MESSAGE
        # ======================

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (username, message)
            VALUES (?, ?)
            """,
            (
                username,
                content
            )
        )

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

        # ======================
        # STATS
        # ======================

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

            return

        # ======================
        # DEBUG AI
        # ======================

        if content.lower().startswith("!ai"):

            question = content[3:].strip()

            if not question:
                return

            try:

                reply = generate_reply(
                    username,
                    question
                )

                if reply:

                    reply = (
                        reply
                        .replace("\n", " ")
                        .replace("🤖", "")
                        .replace("AI", "")
                        .replace("bot", "")
                        .strip()
                    )

                    await message.channel.send(
                        reply[:450]
                    )

                    npc_memory.save_npc_message(
                        reply[:450]
                    )

            except Exception as e:

                print("AI ERROR:", e)

            return

        # ======================
        # AUTO NPC
        # ======================

        try:

            if npc_state.can_reply():

                if should_reply(
                    username,
                    content
                ):

                    reply = generate_reply(
                        username,
                        content
                    )

                    if reply:

                        reply = (
                            reply
                            .replace("\n", " ")
                            .replace("🤖", "")
                            .replace("AI", "")
                            .replace("bot", "")
                            .strip()
                        )

                        await message.channel.send(
                            reply[:350]
                        )

                        npc_memory.save_npc_message(
                            reply[:350]
                        )

                        npc_state.register_reply()

        except Exception as e:

            print("NPC ERROR:", e)

        await self.handle_commands(message)


bot = Bot()
bot.run()