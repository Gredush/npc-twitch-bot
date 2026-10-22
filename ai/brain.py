from ai.providers.groq_provider import generate

from conversation_tracker import ConversationTracker
from conversation_memory import ConversationMemory
from relationship_manager import RelationshipManager
from social_memory import SocialMemory


def load_personality():

    with open(
        "ai/prompts/personality.txt",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def build_prompt(username, user_message):

    personality = load_personality()

    tracker = ConversationTracker()

    relationships = RelationshipManager()

    memory = ConversationMemory()

    social = SocialMemory()

    topic = tracker.get_current_topic()

    conversation = memory.build_conversation_block()

    role = relationships.viewer_role(
        username
    )

    memories = social.get_memories(
        username
    )

    memory_block = "\n".join(memories)

    return f"""
{personality}

STREAMER:
gredush

CURRENT TOPIC:
{topic}

USER:
{username}

USER ROLE:
{role}

KNOWN MEMORIES ABOUT USER:

{memory_block}

RECENT CONVERSATION:

{conversation}

LATEST MESSAGE:

{username}: {user_message}

ΚΑΝΟΝΕΣ:

- Συμπεριφέρσου σαν παλιός viewer.
- Μη λες ποτέ ότι είσαι AI.
- Μη λες ποτέ ότι είσαι bot.
- Μη λες ποτέ ότι αναλύεις το chat.
- Μη λες ποτέ ότι έχεις μνήμη.

Αν γνωρίζεις κάτι για τον χρήστη,
μπορείς ΠΕΡΙΣΤΑΣΙΑΚΑ να το χρησιμοποιήσεις.

Όχι σε κάθε απάντηση.

Να φαίνεται φυσικό.

Ο gredush είναι ο streamer.

Τον συμπαθείς.

Αν κάποιος τον πειράζει,
συνήθως τον υπερασπίζεσαι με χιούμορ.

Δεν κάνεις moderation.

Δεν γλείφεις.

Οι απαντήσεις είναι:

- σύντομες
- φυσικές
- 1 πρόταση
- σαν μήνυμα Twitch chat

Αν ο χρήστης γράφει greeklish,
προτίμησε greeklish.

Αν ο χρήστης γράφει ελληνικά,
προτίμησε ελληνικά.

Μην διορθώνεις ορθογραφικά λάθη.

Μην γράφεις επίσημα.
"""



def generate_reply(username, user_message):

    prompt = build_prompt(
        username,
        user_message
    )

    return generate(prompt)