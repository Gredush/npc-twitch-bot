from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate


def load_personality():

    with open(
        "ai/prompts/personality.txt",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def build_prompt(username, user_message):

    personality = load_personality()

    context = build_chat_context()

    prompt = f"""
{personality}

CHAT HISTORY:

{context}

CURRENT USER:
{username}

MESSAGE:
{user_message}

Απάντησε σαν NPC του καναλιού.
Μίλα ελληνικά.
Μην γράφεις μεγάλα κείμενα.
"""

    return prompt


def generate_reply(username, message):

    prompt = build_prompt(
        username,
        message
    )

    return generate(prompt)