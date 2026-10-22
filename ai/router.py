from ai.providers.groq_provider import generate as groq_generate
from ai.providers.gemini_provider import generate as gemini_generate
from ai.providers.openrouter_provider import generate as openrouter_generate


def generate(prompt):

    try:
        return groq_generate(prompt)

    except Exception as e:
        print(f"GROQ FAILED: {e}")

    try:
        return gemini_generate(prompt)

    except Exception as e:
        print(f"GEMINI FAILED: {e}")

    try:
        return openrouter_generate(prompt)

    except Exception as e:
        print(f"OPENROUTER FAILED: {e}")

    return "den ksero re 😄"