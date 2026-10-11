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

    try:
        image = Image.open(
            BytesIO(image_file.getvalue())
        )

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt, image]
        )

        result = json.loads(response.text.strip())

        return result

    except json.JSONDecodeError:

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
