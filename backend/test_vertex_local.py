import os
import json
from dotenv import load_dotenv
from app.services.vertex_ai import generate_visual_from_sheet 

# 1. Load your .env settings
load_dotenv()

# 2. Load data from kaelen.json
# Note: User's original request mentioned 'kaelon.json' but file is 'kaelen.json'
json_path = os.path.join(os.path.dirname(__file__), '..', 'character_sheets', 'kaelen.json')

with open(json_path, 'r') as f:
    raw_data = json.load(f)

print(f"Loaded JSON data for: {raw_data.get('name')}")

# 3. Run the test with raw dict
print("Starting local Vertex AI test...")
try:
    # Pass the raw dictionary directly to the service
    result = generate_visual_from_sheet(raw_data)
    print(f"Success! Image generated: {result}")
except Exception as e:
    print(f"Test Failed: {e}")