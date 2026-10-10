# ai/missions.py

import os
import json

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
# FALLBACK MISSIONS
# ============================================================

FALLBACK_MISSIONS = [
    "Find a plant with an interesting shape and observe its leaves.",
    "Look for an insect and observe what it is doing without disturbing it.",
    "Find two different plants and compare their appearance.",
    "Observe one living organism and describe the place where you found it.",
    "Look around and find one small sign of biodiversity you might normally miss."
]


# ============================================================
# GENERATE MISSIONS
# ============================================================

def generate_missions(
    environment,
    difficulty,
    biodiversity_type
):

    prompt = f"""
You are EcoPulse, an AI-powered biodiversity exploration assistant.

Create 5 outdoor biodiversity missions.

User context:
- Environment: {environment}
- Difficulty: {difficulty}
- Biodiversity type: {biodiversity_type}

Requirements:
1. Generate exactly 5 missions.
2. Make every mission meaningfully different.
3. Encourage different types of observation such as:
   appearance, behavior, interaction, habitat, comparison,
   texture, sound, or change over time.
4. Missions must be realistic for the given environment.
5. Missions must match the requested difficulty.
6. Do not ask the user to touch, collect, feed, disturb,
   or harm plants or animals.
7. Missions should be possible without special equipment.
8. Keep each mission short and easy to understand.

Return ONLY a JSON list containing exactly 5 mission strings.
Do not include explanations or markdown.
"""

    try:

        # ----------------------------------------------------
        # SEND PROMPT TO GEMMA
        # ----------------------------------------------------

        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=prompt
        )

        # ----------------------------------------------------
        # GET MODEL RESPONSE
        # ----------------------------------------------------

        response_text = response.text.strip()

        # ----------------------------------------------------
        # CONVERT JSON TEXT INTO PYTHON OBJECT
        # ----------------------------------------------------

        missions = json.loads(response_text)

        # ----------------------------------------------------
        # VALIDATE RESPONSE
        # ----------------------------------------------------

        if not isinstance(missions, list):
            print("AI response is not a list.")
            return FALLBACK_MISSIONS

        if len(missions) != 5:
            print("AI did not generate exactly 5 missions.")
            return FALLBACK_MISSIONS

        if not all(isinstance(mission, str) for mission in missions):
            print("AI returned an invalid mission format.")
            return FALLBACK_MISSIONS

        return missions

    except json.JSONDecodeError:

        print("AI returned invalid JSON.")
        return FALLBACK_MISSIONS

    except Exception as e:

        print(f"AI mission generation failed: {e}")
        return FALLBACK_MISSIONS


# ============================================================
# TEST THE FUNCTION
# ============================================================

if __name__ == "__main__":

    missions = generate_missions(
        "College Campus",
        "Easy",
        "General Biodiversity"
    )

    print("\nGenerated Missions:\n")

    for i, mission in enumerate(missions, start=1):
        print(f"{i}. {mission}")
