

import os
from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )


# ============================================================
# CREATE GEMMA CLIENT
# ============================================================

client = genai.Client(
    api_key=api_key
)


# ============================================================
# ANALYZE DISCOVERY
# ============================================================

def analyze_discovery(image_file):

    prompt = """
You are EcoPulse, an AI biodiversity assistant.

Analyze the uploaded outdoor image.

Try to identify the main plant, insect, bird,
flower, tree, or other organism visible in the image.

Return your answer in this format:

Identification: <name or best identification>

Confidence: <High, Medium, or Low>

Explanation: <short explanation about what was identified
and the visible characteristics that support the identification>

Biodiversity Information: <short useful information
about the organism and its ecological role>

Important:
- Do not claim certainty when the image is unclear.
- If identification is uncertain, say so.
- Do not invent specific facts.
- Keep the explanation beginner-friendly.
"""

    try:

        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=[
                prompt,
                image_file
            ]
        )

        return response.text.strip()

    except Exception as e:

        print(f"Vision analysis failed: {e}")

        return (
            "Unable to analyze this image right now. "
            "Please try another clear photo."
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "Vision module loaded successfully."
    )