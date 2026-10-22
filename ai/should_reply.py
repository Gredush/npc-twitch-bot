from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate


def should_reply(username, message):

    context = build_chat_context(25)

    prompt = f"""
Είσαι μέλος ενός Twitch chat.

Πρέπει να αποφασίσεις ΑΝ χρειάζεται να γράψεις μήνυμα.

Απάντησε ΜΟΝΟ με:

YES

ή

NO

Κανόνες:

- Αν το chat είναι ήσυχο -> NO
- Αν κάποιος είπε μόνο γεια -> NO
- Αν κάποιος είπε μόνο lol -> NO
- Αν δεν έχεις κάτι χρήσιμο να πεις -> NO
- Αν υπάρχει αστεία στιγμή -> YES
- Αν γίνεται συζήτηση -> YES
- Αν υπάρχει ερώτηση που θα απαντούσε φυσιολογικά ένας viewer -> YES

CHAT:

{context}

ΤΕΛΕΥΤΑΙΟ ΜΗΝΥΜΑ:

{username}: {message}
"""

    response = generate(prompt)

    if not response:
        return False

    response = response.strip().upper()

    return "YES" in response