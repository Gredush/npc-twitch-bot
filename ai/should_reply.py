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

Απάντησε YES ΜΟΝΟ αν:
- Το μήνυμα περιέχει ξεκάθαρη ερώτηση (π.χ. "τι παίζεις;", "πόσο είναι το ilvl;")
- Κάποιος απευθύνεται σε εσένα προσωπικά
- Κάποιος λέει κάτι τόσο αστείο που αξίζει ένα σχόλιο

Απάντησε NO αν:
- Είναι απλό χαιρετισμός (geia, kalimera, kalispera)
- Είναι απλά reactions (xaxa, lol, emojis, απλά "ναι", "όχι")
- Είναι ειδοποιήσεις από άλλα bots (streamelements, soundalerts κλπ)
- Κάποιος μιλάει με κάποιον άλλον (π.χ. @username) και όχι μαζί σου
- Δεν έχεις κάτι ουσιαστικό να προσθέσεις στη συζήτηση

CHAT CONTEXT:
{chat_context}

ΝΕΟ ΜΗΝΥΜΑ:
{username}: {message}
"""

    result = generate(prompt)

    if not result:
        return False

    return "YES" in result.upper()