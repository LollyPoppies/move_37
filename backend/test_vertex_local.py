import os
import json
from dotenv import load_dotenv
from app.services.vertex_ai import generate_visual_from_sheet 

# 1. Load your .env settings
load_dotenv()

# 2. Load data from kaelen.json
# Note: User's original request mentioned 'kaelon.json' but file is 'kaelen.json'
json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'character_sheets', 'kaelen.json')

with open(json_path, 'r') as f:
    raw_data = json.load(f)

print(f"Loaded JSON data for: {raw_data.get('name')}")

# 3. Run the test with raw dict
try:
    # Pass the raw dictionary directly to the service
    images = generate_visual_from_sheet(raw_data)
    
    # Save the images
    output_dir = os.path.join(os.getcwd(), 'output', 'characters')
    os.makedirs(output_dir, exist_ok=True)
    
    base_filename = raw_data.get('name', 'asset')
    
    for i, image in enumerate(images):
        filename = f"{base_filename}_{i+1}.png"
        output_filename = os.path.join(output_dir, filename)
        image.save(location=output_filename, include_generation_parameters=False)
        print(f"Success! Image generated and saved to: {output_filename}")

except Exception as e:
    print(f"Test Failed: {e}")