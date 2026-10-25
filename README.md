A Twitch chat bot with an NPC personality — it remembers viewers, builds affinity/relationships over time, tracks topics, detects language, and replies with human-like delays through a pluggable AI brain (with failover). Deployable on Railway.

✨ Features

NPC personality engine — natural, non-spammy responses with human-like delays (npc_engine.py, npc_state.py).

AI brain with failover — multiple providers, automatic fallback (ai/, bot.py).

Social memory — remembers past replies and conversations (social_memory.py, conversation_memory.py, reply_memory.py).

Affinity & relationships — builds affinity with viewers and tracks relationships (affinity_manager.py, relationship_manager.py).

Returning viewer detection — smart "welcome back" system (returning_viewer.py).

Interest & topic management — interest profiles and topic stickiness (interest_manager.py, topic_manager.py).

Conversation awareness & tracking — context recall and social awareness (conversation_awareness.py, conversation_tracker.py, context_recall.py).

Language detection — responds appropriately per language (language_detector.py).

Persistent storage — database-backed memory (database.py, npc_memory.py).

Deployment ready — Procfile + runtime.txt for Railway.

🧱 Tech Stack

Python (see runtime.txt for the pinned version)

Twitch chat integration

Pluggable AI providers (ai/)

Database for persistent memory

Deployment: Railway (Procfile)

📋 Requirements

Python (version from runtime.txt)

A Twitch account + OAuth token for the bot

Twitch channel name(s) to join

API keys for the AI provider(s) you enable

Dependencies from requirements.txt

📄 License

Proprietary — All rights reserved.

This project is not open source. No part of this code may be used, copied, modified, or distributed without explicit permission from the author.

🔗 Links

Repository: https://github.com/Gredush/npc-twitch-bot

Author: @Gredush


Ένα Twitch chat bot με προσωπικότητα NPC — θυμάται viewers, χτίζει affinity/σχέσεις με τον χρόνο, παρακολουθεί topics, ανιχνεύει γλώσσα και απαντά με ανθρώπινες καθυστερήσεις μέσω pluggable AI brain (με failover). Έτοιμο για deploy στο Railway.

✨ Δυνατότητες

Μηχανή προσωπικότητας NPC — φυσικές απαντήσεις χωρίς spam, με ανθρώπινες καθυστερήσεις (npc_engine.py, npc_state.py).

AI brain με failover — πολλαπλοί providers, αυτόματο fallback (ai/, bot.py).

Κοινωνική μνήμη — θυμάται προηγούμενες απαντήσεις και συνομιλίες (social_memory.py, conversation_memory.py, reply_memory.py).

Affinity & σχέσεις — χτίζει affinity με viewers και παρακολουθεί σχέσεις (affinity_manager.py, relationship_manager.py).

Ανίχνευση επιστρεφόντων viewers — έξυπνο σύστημα «welcome back» (returning_viewer.py).

Διαχείριση ενδιαφερόντων & θεμάτων — interest profiles και topic stickiness (interest_manager.py, topic_manager.py).

Επίγνωση & παρακολούθηση συνομιλίας — context recall και social awareness (conversation_awareness.py, conversation_tracker.py, context_recall.py).

Ανίχνευση γλώσσας — απαντά κατάλληλα ανά γλώσσα (language_detector.py).

Μόνιμη αποθήκευση — μνήμη backed από database (database.py, npc_memory.py).

Έτοιμο για deployment — Procfile + runtime.txt για Railway.

🧱 Τεχνολογίες

Python (δείτε το runtime.txt για την έκδοση)

Ενσωμάτωση με Twitch chat

Pluggable AI providers (ai/)

Database για μόνιμη μνήμη

Deployment: Railway (Procfile)

📋 Απαιτήσεις

Python (έκδοση από το runtime.txt)

Λογαριασμός Twitch + OAuth token για το bot

Όνομα/κανάλι(-ια) Twitch για σύνδεση

API keys για τους AI providers που θα ενεργοποιήσεις

Οι εξαρτήσεις από το requirements.txt

📄 Άδεια Χρήσης

Proprietary — All rights reserved.

Το project δεν είναι ανοιχτού κώδικα. Κανένα μέρος του κώδικα δεν επιτρέπεται να χρησιμοποιηθεί, αντιγραφεί, τροποποιηθεί ή διανεμηθεί χωρίς ρητή άδεια από τον δημιουργό.

🔗 Σύνδεσμοι

Αποθετήριο: https://github.com/Gredush/npc-twitch-bot

Δημιουργός: @Gredush
