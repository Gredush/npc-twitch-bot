from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate
from conversation_awareness import ConversationAwareness


def should_reply(username, message):

    awareness = ConversationAwareness()

    if awareness.looks_like_reply_to_npc(
        username,
        message
    ):
        return True

    chat_context = build_chat_context(15)

    prompt = f"""
Είσαι viewer σε Twitch chat.
Ο στόχος σου είναι να συμμετέχεις ΜΟΝΟ όταν έχει απόλυτο νόημα και να μην είσαι σπαμ.

Απάντησε ΜΟΝΟ με τη λέξη YES ή NO.

Απάντησε YES αν:
- Το μήνυμα περιέχει ερώτηση (π.χ. "τι ώρα", "πόσο", "τι παίζεις;", ακόμα και αν είναι ρητορική)
- Κάποιος λέει κάτι που αφορά το παιχνίδι (π.χ. "πόσο dmg", "τι class")
- Κάποιος κράζει ή κοροϊδεύει τον streamer (για να συμφωνήσεις ή να διαφωνήσεις)
- Κάποιος λέει κάτι αστείο και αξίζει ένα σχόλιο
- Κάποιος απευθύνεται σε εσένα (mention)

Απάντησε NO ΜΟΝΟ αν:
- Είναι απλός χαιρετισμός (geia, kalimera)
- Είναι απλά reactions (xaxa, lol, emojis)
- Είναι ειδοποιήσεις από bots
- Κάποιος μιλάει με κάποιον άλλον και όχι μαζί σου

CHAT CONTEXT:
{chat_context}

ΝΕΟ ΜΗΝΥΜΑ:
{username}: {message}
"""

    result = generate(prompt)

    if not result:
        return False

    return "YES" in result.upper()