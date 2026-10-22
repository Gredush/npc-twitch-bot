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

        try:

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

        except Exception as e:

            print(
                f"MEMORY ERROR: {e}"
            )

    def process_message(
        self,
        username,
        content
    ):

        print(
            "DEBUG: process_message"
        )

        self.npc_state.register_message()

        welcome_message = None

        try:

            if (
                self.returning_viewer
                .should_welcome_back(
                    username
                )
            ):

                print(
                    "DEBUG: returning viewer detected"
                )

                if self.npc_state.can_reply():

                    welcome_message = (
                        self.returning_viewer
                        .welcome_message(
                            username
                        )
                    )

                    self.npc_state.register_reply()

        except Exception as e:

            print(
                f"RETURNING VIEWER ERROR: {e}"
            )

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

        print(
            "DEBUG: maybe_generate_reply called"
        )

        if not self.npc_state.can_reply():

            print(
                "DEBUG: can_reply = False"
            )

            return None

        print(
            "DEBUG: can_reply = True"
        )

        try:

            should = should_reply(
                username,
                content
            )

            print(
                f"DEBUG: should_reply = {should}"
            )

            if not should:
                return None

        except Exception as e:

            print(
                f"SHOULD_REPLY ERROR: {e}"
            )

            return None

        try:

            reply = generate_reply(
                username,
                content
            )

            print(
                f"DEBUG REPLY: {reply}"
            )

        except Exception as e:

            print(
                f"GENERATE_REPLY ERROR: {e}"
            )

            return None

        if not reply:

            print(
                "DEBUG: Empty reply"
            )

            return None

        reply = (
            reply
            .replace("\n", " ")
            .replace("🤖", "")
            .replace("AI", "")
            .replace("bot", "")
            .strip()
        )

        try:

            self.npc_memory.save_npc_message(
                reply
            )

            reply_memory.register_npc_message(
                reply
            )

            self.npc_state.register_reply()

        except Exception as e:

            print(
                f"SAVE REPLY ERROR: {e}"
            )

        return reply