import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)


FALLBACK_MISSIONS = [
    "Find a plant with an interesting shape and observe its leaves.",
    "Look for an insect and observe what it is doing without disturbing it.",
    "Find two different plants and compare their appearance.",
    "Observe one living organism and describe the place where you found it.",
    "Find one small sign of biodiversity you might normally miss."
]


def extract_json_list(text):
    """
    Pull the JSON list out of the model's reply.

    The model sometimes wraps the list in ```json fences or adds a
    sentence before/after it. We keep only the part from the first '['
    to the last ']' so json.loads sees clean JSON.
    Returns None if no list markers are found.
    """
    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1 or end < start:
        return None

    return text[start:end + 1]


def generate_missions(environment, difficulty, biodiversity_type):

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
3. Encourage different types of observation such as
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

    # Declared before try so the except block can print it for debugging
    raw_text = ""

    try:
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=prompt
        )

        raw_text = (response.text or "").strip()

        json_part = extract_json_list(raw_text)

        if json_part is None:
            print(f"No JSON list found in model reply: {raw_text!r}")
            return FALLBACK_MISSIONS

        missions = json.loads(json_part)

        if not isinstance(missions, list):
            return FALLBACK_MISSIONS

        if len(missions) != 5:
            return FALLBACK_MISSIONS

        if not all(isinstance(mission, str) for mission in missions):
            return FALLBACK_MISSIONS

        return missions

    except Exception as e:
        print(f"Mission generation failed: {e}")
        print(f"Raw model reply was: {raw_text!r}")
        return FALLBACK_MISSIONS
