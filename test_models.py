from unittest.mock import patch
from ai.providers.groq_provider import generate

@patch("ai.providers.groq_provider.requests.post")
def test_generate_fallback(mock_post):
    """Ελέγχει αν το generate δοκιμάζει το επόμενο μοντέλο αν το πρώτο αποτύχει."""
    # Το πρώτο μοντέλο επιστρέφει error, το δεύτερο πετυχαίνει
    mock_post.side_effect = [
        Exception("API Error"),  # Πρώτη κλήση (αποτυχία)
        type('obj', (object,), {  # Δεύτερη κλήση (επιτυχία)
            'json': lambda: {"choices": [{"message": {"content": "ola kala"}}]},
            'status_code': 200
        })
    ]

    reply = generate("test prompt")
    
    # Πρέπει να επιστρέψει την απάντηση του δεύτερου μοντέλου
    assert reply == "ola kala"
    # Πρέπει να έχει κάνει 2 κλήσεις (μία για κάθε μοντέλο)
    assert mock_post.call_count == 2
