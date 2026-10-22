from ai.providers.groq_provider import (
    generate as groq_generate
)

from ai.providers.gemini_provider import (
    generate as gemini_generate
)


def generate(prompt):

    try:

        reply = groq_generate(prompt)

        if reply:
            return reply

    except Exception as e:

        print(
            f"GROQ FAILED: {e}"
        )

    try:

        reply = gemini_generate(prompt)

        if reply:
            return reply

    except Exception as e:

        print(
            f"GEMINI FAILED: {e}"
        )

    return "den ksero re 😄"