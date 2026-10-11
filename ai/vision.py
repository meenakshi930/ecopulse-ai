import os
import json
from io import BytesIO

from dotenv import load_dotenv
from google import genai
from PIL import Image


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=api_key)


def extract_json_object(text):
    """
    Pull the JSON object out of the model's reply.

    The model sometimes wraps the JSON in ```json fences or adds a
    sentence before/after it. We keep only the part from the first '{'
    to the last '}' so json.loads sees clean JSON.
    Returns None if no object markers are found.
    """
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end < start:
        return None

    return text[start:end + 1]


def analyze_discovery(image_file):

    prompt = """
You are EcoPulse, an AI biodiversity assistant.

Analyze the uploaded outdoor image.

Try to identify the main plant, insect, bird,
flower, tree, or other organism visible in the image.

Return ONLY valid JSON in this exact structure:

{
    "identification": "name of the organism",
    "confidence": "High, Medium, or Low",
    "explanation": "short explanation about the identification",
    "biodiversity_information": "short useful information about the organism"
}

Important:
- Do not claim certainty when the image is unclear.
- If identification is uncertain, say so.
- Do not invent specific facts.
- Keep the explanation beginner-friendly.
"""

    # Declared before try so the except blocks can print it for debugging
    raw_text = ""

    try:
        image = Image.open(
            BytesIO(image_file.getvalue())
        )

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt, image]
        )

        raw_text = (response.text or "").strip()

        json_part = extract_json_object(raw_text)

        if json_part is None:
            print(f"No JSON object found in model reply: {raw_text!r}")
            raise json.JSONDecodeError("No JSON object found", raw_text, 0)

        result = json.loads(json_part)

        if not isinstance(result, dict):
            raise json.JSONDecodeError("JSON is not an object", raw_text, 0)

        return result

    except json.JSONDecodeError:

        print(f"Invalid JSON from vision model: {raw_text!r}")

        return {
            "identification": "Unknown",
            "confidence": "Low",
            "explanation": "The AI returned an invalid response.",
            "biodiversity_information": ""
        }

    except Exception as e:

        print(f"Vision analysis failed: {e}")

        return {
            "identification": "Unknown",
            "confidence": "Low",
            "explanation": "Unable to analyze this image right now.",
            "biodiversity_information": ""
        }
