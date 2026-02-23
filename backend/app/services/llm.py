import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "move-37")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

SYSTEM_PROMPT = """
You are an expert character designer for animation and film. 
Your task is to take a natural language description of a character and convert it into a structured JSON format.

The output must be a valid JSON object matching this schema:
{
    "character_id": "string (leave empty or generate code like c_003)",
    "name": "string",
    "physical_traits": {
        "age_range": "string",
        "hair": "string",
        "eyes": "string",
        "physique": "string"
    },
    "style_id": "string (use an existing style like 'cyberpunk_v1', 'ghibli_esque', 'claymation', 'hyper_real', 'noir' or suggest a new one)",
    "clothing": "string (detailed description of outfit)",
    "extra_details": "string (any other unique identifiers, tattoos, scars, accessories)",
    "negative_prompt": "string (things to avoid in image generation, e.g., 'glasses, hat')",
    "reference_images": {
        "default": {
            "head": "",
            "full_body": "",
            "side": "",
            "back": ""
        }
    }
}

Be descriptive and creative. If the user prompt is brief, expand on it to make a high-quality character sheet.
Do not include any text other than the JSON object.
"""

def generate_character_json(prompt: str):
    model = GenerativeModel("gemini-1.5-flash")
    
    generation_config = GenerationConfig(
        response_mime_type="application/json",
    )
    
    response = model.generate_content(
        [SYSTEM_PROMPT, prompt],
        generation_config=generation_config
    )
    
    try:
        # Gemini with response_mime_type="application/json" returns a clean json string
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw response: {response.text}")
        raise e
