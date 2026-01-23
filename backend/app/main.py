# In backend/app/main.py
from fastapi import FastAPI
from app.services.vertex_ai import generate_visual_from_sheet
import os, json

app = FastAPI()

@app.post("/batch-render")
async def batch_render():
    """Reads all local JSONs and generates images in bulk."""
    results = []
    # Process Characters
    char_path = "../../data/characters/"
    for file in os.listdir(char_path):
        if file.endswith(".json"):
            with open(os.path.join(char_path, file), "r") as f:
                data = json.load(f)
                img_url = generate_visual_from_sheet(data, sheet_type="character")
                results.append({"name": data.get("name"), "url": img_url})
    
    return {"status": "Complete", "rendered_assets": results}