import os
from dotenv import load_dotenv
from app.services.vertex_ai import generate_visual_from_sheet # Path to your logic
from app.models.schemas import CharacterSheet

# 1. Load your .env settings
load_dotenv()

# 2. Mock some data (mimicking your kaelen.json)
test_data = {
    "character_id": "test_kaelen",
    "name": "Kaelen",
    "physical_traits": {
        "age_range": "20s",
        "hair": "silver",
        "eyes": "neon blue",
        "physique": "lean"
    },
    "style": {
        "art_style": "Cyberpunk Noir",
        "line_weight": "bold",
        "color_palette": ["blue", "purple"]
    },
    "clothing": "tattered trench coat"
}

# 3. Create a Pydantic object
char_sheet = CharacterSheet(**test_data)

# 4. Run the test
print("Starting local Vertex AI test...")
try:
    result = generate_visual_from_sheet(char_sheet)
    print(f"Success! Image generated: {result}")
except Exception as e:
    print(f"Test Failed: {e}")