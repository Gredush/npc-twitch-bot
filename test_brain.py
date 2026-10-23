import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from ai.brain import build_prompt, generate_reply

@pytest.fixture(autouse=True)
def mock_db():
    """Mockάρει τη σύνδεση με τη βάση δεδομένων για όλα τα tests."""
    with patch("sqlite3.connect") as mock_connect:
        # Φτιάχνουμε μια ψεύτικη in-memory βάση
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE messages (id INTEGER, message TEXT)")
        cursor.execute("CREATE TABLE viewers (username TEXT, message_count INTEGER)")
        cursor.execute("CREATE TABLE social_memory (username TEXT, memory TEXT)")
        cursor.execute("CREATE TABLE interests (username TEXT, interest TEXT, score INTEGER)")
        conn.commit()
        
        mock_connect.return_value = conn
        yield

def test_build_prompt_structure(mock_db):
    """Ελέγχει αν το prompt χτίζεται σωστά."""
    prompt = build_prompt("test_user", "geia re")
    
    assert "Είσαι θεατής σε Twitch chat" in prompt
    assert "test_user" in prompt
    assert "geia re" in prompt
    assert "ΚΑΝΟΝΕΣ:" in prompt

@patch("ai.providers.groq_provider.requests.post")
def test_generate_reply_mocked(mock_post, mock_db):
    """Ελέγχει αν το generate_reply επιστρέφει σωστά την απάντηση."""
    mock_post.return_value.json.return_value = {
        "choices": [{"message": {"content": "kala re 😄"}}]
    }
    mock_post.return_value.status_code = 200

    reply = generate_reply("test_user", "ti kaneis?")
    assert reply == "kala re 😄"
    mock_post.assert_called_once()
