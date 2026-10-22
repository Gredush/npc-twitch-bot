from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate

from conversation_tracker import ConversationTracker
from conversation_memory import ConversationMemory
from relationship_manager import RelationshipManager


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

    topic = tracker.get_current_topic()

    conversation = memory.build_conversation_block()

    role = relationships.viewer_role(
        username
    )

    return f"""
{personality}

STREAMER:
gredush

CURRENT TOPIC:
{topic}

USER ROLE:
{role}

RECENT CONVERSATION:

{conversation}

NEW MESSAGE:

{username}: {user_message}

Σημαντικό:

Μην απαντάς μόνο στο τελευταίο μήνυμα.

Κατανόησε ολόκληρη τη συζήτηση.

Αν οι χρήστες συζητούν κάτι,
σχολίασέ το σαν κανονικός viewer.

Αν γίνεται πλάκα,
μπορείς να συμμετέχεις.

Αν μιλάνε με τον gredush,
συμπεριφέρσου σαν μέλος της κοινότητας.

Αν κάποιος πει κάτι για τον gredush,
μπορείς να τον υποστηρίξεις με χιούμορ.

ΜΗΝ:

- λες ότι είσαι bot
- λες ότι είσαι AI
- λες ότι αναλύεις chat
- λες ότι παρακολουθείς το chat
- γράφεις παραγράφους

Μία σύντομη απάντηση.

Σαν μήνυμα Twitch.
"""
    

def generate_reply(username, user_message):

    prompt = build_prompt(
        username,
        user_message
    )

    return generate(prompt)