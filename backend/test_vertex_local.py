print("DEBUG: SANITY CHECK - RUNNING test_vertex_local.py")
import os
from dotenv import load_dotenv
from app.services.vertex_ai import generate_visual_from_sheet # Path to your logic
from app.models.schemas import CharacterSheet

import json

# 1. Load your .env settings
load_dotenv()
# 1. Load your .env settings
load_dotenv()

# 2. Load data from kaelen.json
json_path = os.path.join(os.path.dirname(__file__), '..', 'character_sheets', 'kaelen.json')

with open(json_path, 'r') as f:
    raw_data = json.load(f)

# 3. Map JSON data to flat CharacterSheet schema
# The schema expects flat fields, but our JSON has nested structures
test_data = {
    "name": raw_data["name"],
    "age_range": raw_data["physical_traits"]["age_range"],
    "hair_details": raw_data["physical_traits"]["hair"],
    "eye_color": raw_data["physical_traits"]["eyes"],
    "clothing_description": raw_data["clothing"],
    "art_style": raw_data["style"]["art_style"],
    # Convert 'physique' and any other traits to a list
    "physical_traits": [raw_data["physical_traits"]["physique"]]
}

# 3. Create a Pydantic object
char_sheet = CharacterSheet(**test_data)
print(f"Loaded CharacterSheet: {char_sheet}")

# 4. Run the test
print("Starting local Vertex AI test...")
try:
    result = generate_visual_from_sheet(char_sheet.model_dump())
    print(f"Success! Image generated: {result}")
except Exception as e:
    print(f"Test Failed: {e}")