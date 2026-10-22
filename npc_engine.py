import sqlite3

from ai.brain import generate_reply
from ai.should_reply import should_reply

from social_memory import SocialMemory
from memory_extractor import MemoryExtractor

from affinity_manager import AffinityManager
from interest_manager import InterestManager

from npc_memory import NPCMemory
from npc_state import NPCState

from reply_memory_instance import reply_memory

from returning_viewer import (
    ReturningViewer
)


class NPCEngine:

    def __init__(self):

        self.social_memory = SocialMemory()

        self.memory_extractor = (
            MemoryExtractor()
        )

        self.affinity_manager = (
            AffinityManager()
        )

        self.affinity_manager.apply_decay()

        self.interest_manager = (
            InterestManager()
        )

        self.npc_memory = NPCMemory()

        self.npc_state = NPCState()

        self.returning_viewer = (
            ReturningViewer()
        )

    def save_user_message(
        self,
        username,
        content
    ):

        conn = sqlite3.connect(
            "memory.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (username, message)
            VALUES (?, ?)
            """,
            (username, content)
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

    def process_memory(
        self,
        username,
        content
    ):

        memory = (
            self.memory_extractor.extract(
                username,
                content
            )
        )

        if not memory:
            return

        if (
            self.social_memory.memory_exists(
                username,
                memory
            )
        ):
            return

        self.social_memory.save_memory(
            username,
            memory
        )

        print(
            f"NEW MEMORY: {username} -> {memory}"
        )

    def process_message(
        self,
        username,
        content
    ):

        self.npc_state.register_message()

        welcome_message = None

        if (
            self.returning_viewer
            .should_welcome_back(
                username
            )
        ):

            if self.npc_state.can_reply():

                welcome_message = (
                    self.returning_viewer
                    .welcome_message(
                        username
                    )
                )

                self.npc_state.register_reply()

        self.affinity_manager.increase(
            username,
            1
        )

        self.save_user_message(
            username,
            content
        )

        self.process_memory(
            username,
            content
        )

        self.interest_manager.process_message(
            username,
            content
        )

        return welcome_message

    def maybe_generate_reply(
        self,
        username,
        content
    ):

        if not self.npc_state.can_reply():
            return None

        if not should_reply(
            username,
            content
        ):
            return None

        reply = generate_reply(
            username,
            content
        )

        if not reply:
            return None

        reply = (
            reply
            .replace("\n", " ")
            .replace("🤖", "")
            .replace("AI", "")
            .replace("bot", "")
            .strip()
        )

        self.npc_memory.save_npc_message(
            reply
        )

        reply_memory.register_npc_message(
            reply
        )

        self.npc_state.register_reply()

        return reply