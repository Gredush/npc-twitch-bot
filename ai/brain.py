from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate
from conversation_tracker import ConversationTracker


def load_personality():

    with open(
        "ai/prompts/personality.txt",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def build_prompt(username, user_message):

    personality = load_personality()

    context = build_chat_context(25)

    tracker = ConversationTracker()

    current_topic = tracker.get_current_topic()

    return f"""
{personality}

ΤΡΕΧΟΝ ΘΕΜΑ ΣΥΖΗΤΗΣΗΣ:

{current_topic}

ΠΡΟΣΦΑΤΟ CHAT:

{context}

ΝΕΟ ΜΗΝΥΜΑ:

{username}: {user_message}

Συμπεριφέρσου σαν παλιός viewer.

Αν υπάρχει θέμα συζήτησης, αναφέρσου σε αυτό.

Οι απαντήσεις πρέπει να είναι:

- 1 πρόταση
- σύντομες
- φυσικές
- σαν Twitch viewer

Μην αναφέρεις ποτέ ότι είσαι AI.
Μην αναφέρεις ποτέ ότι είσαι bot.
"""
    

def generate_reply(username, user_message):

    prompt = build_prompt(
        username,
        user_message
    )

    return generate(prompt)