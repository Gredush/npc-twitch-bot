import sqlite3
import random

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

    COMMON_REPLIES = {

        "ti kaneis": [
            "kala re 😄",
            "ola kala 😄",
            "ta klasika 😄"
        ],

        "pos eisai": [
            "kala re 😄",
            "ola kala 😄",
            "mia xara 😄"
        ],

        "ti nea": [
            "tipota spoudaio 😄",
            "ta klasika 😄",
            "ola kala 😄"
        ],

        "geia": [
            "geia 😄"
        ],

        "geia xara": [
            "geia re 😄"
        ],

        "kalispera": [
            "kalispera 😄"
        ],

        "kalimera": [
            "kalimera 😄"
        ],

        "opa": [
            "ti egine? 😂"
        ],

        "lol": [
            "😂"
        ],

        "xaxa": [
            "😂"
        ]
    }

    def __init__(self):

        self.social_memory = SocialMemory()

        self.memory_extractor = MemoryExtractor()

        self.affinity_manager = AffinityManager()
        self.affinity_manager.apply_decay()

        self.interest_manager = InterestManager()

        self.npc_memory = NPCMemory()

        self.npc_state = NPCState()

        self.returning_viewer = ReturningViewer()

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

            if self.social_memory.memory_exists(
                username,
                memory
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

            if self.returning_viewer.should_welcome_back(
                username
            ):

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

    def try_common_reply(
        self,
        content
    ):

        text = (
            content
            .lower()
            .strip()
            .replace(";", "")
            .replace("?", "")
            .replace("!", "")
            .replace(".", "")
            .replace(",", "")
        )

        for trigger, replies in (
            self.COMMON_REPLIES.items()
        ):

            if trigger in text:

                return random.choice(
                    replies
                )

        return None

        def maybe_generate_reply(
        self,
        username,
        content,
        force_reply=False,
        mentioned=False
    ):

        print(
            "DEBUG: maybe_generate_reply called"
        )

        common = self.try_common_reply(
            content
        )

        if common:

            print(
                f"DEBUG COMMON: {common}"
            )

            return common

        if not force_reply:

            if not self.npc_state.can_reply():

                print(
                    "DEBUG: can_reply = False"
                )

                return None

        print(
            "DEBUG: can_reply = True"
        )

        if not force_reply:

            try:

                if mentioned:

                    should = (
                        random.random() < 0.90
                    )

                    print(
                        f"DEBUG: mention reply = {should}"
                    )

                else:

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
