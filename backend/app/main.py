from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import glob

# Import services
# Assuming running from backend/ directory as `uvicorn app.main:app`
# Adjust imports if necessary based on actual python path
try:
    from app.services.character_refs import generate_character_references
    from app.services.environment_refs import generate_environment_references
    from app.services.llm import generate_character_json
except ImportError:
    # Fallback for running directly or differently
    from services.character_refs import generate_character_references
    from services.environment_refs import generate_environment_references
    from services.llm import generate_character_json

app = FastAPI()

# Config
# Data directory is at project root: move_37/data
# We are in move_37/backend/app/main.py
# So we need to go up 3 levels to get to move_37, then into data
# abspath(__file__) -> move_37/backend/app/main.py
# dirname -> move_37/backend/app
# dirname -> move_37/backend
# dirname -> move_37
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

print(f"DATA_DIR resolved to: {DATA_DIR}")

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
# Access via http://localhost:8000/static/characters/kaelen_refs/...
if os.path.exists(DATA_DIR):
    app.mount("/static", StaticFiles(directory=DATA_DIR), name="static")
else:
    print(f"WARNING: DATA_DIR {DATA_DIR} does not exist. Static files will not be served.")

# Schemas
class GenerateRequest(BaseModel):
    id: str # Filename without extension or full ID
    style_id: Optional[str] = None
    force: bool = False

class PromptRequest(BaseModel):
    prompt: str

class FileSaveRequest(BaseModel):
    content: str # content as string (JSON/YAML)

@app.get("/")
def read_root():
    return {"message": "Move 37 Backend API"}

@app.post("/generate/character")
def generate_character(request: GenerateRequest):
    try:
        # Check if file exists
        char_path = os.path.join(DATA_DIR, "characters", f"{request.id}.json")
        if not os.path.exists(char_path):
             # Try adding .json
             if not request.id.endswith(".json"):
                 char_path = os.path.join(DATA_DIR, "characters", f"{request.id}.json")
        
        if not os.path.exists(char_path):
             raise HTTPException(status_code=404, detail=f"Character file not found: {request.id}")

        # The service expects data_dir to be the directory containing the json files
        result = generate_character_references(
            character_id=request.id,
            data_dir=os.path.join(DATA_DIR, "characters"),
            style_id=request.style_id,
            force=request.force
        )
        return {"status": "success", "images": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/environment")
def generate_environment(request: GenerateRequest):
    try:
        # Check if file exists
        env_path = os.path.join(DATA_DIR, "environments", f"{request.id}.json")
        if not os.path.exists(env_path):
             # Try adding .json
             if not request.id.endswith(".json"):
                 env_path = os.path.join(DATA_DIR, "environments", f"{request.id}.json")

        if not os.path.exists(env_path):
             raise HTTPException(status_code=404, detail=f"Environment file not found: {request.id}")

        result = generate_environment_references(
            environment_id=request.id,
            data_dir=os.path.join(DATA_DIR, "environments")
        )
        return {"status": "success", "images": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/character-json")
def generate_character_json_endpoint(request: PromptRequest):
    """Generate a character sheet JSON from a text prompt."""
    try:
        result = generate_character_json(request.prompt)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/assets")
def list_assets():
    """List all generated assets (images/videos) in the data directory."""
    assets = []
    # Recursively find all jpg, png, mp4
    search_patterns = ["**/*.jpg", "**/*.png", "**/*.mp4"]
    
    for pattern in search_patterns:
        # glob.glob in python 3.10+ supports root_dir, but let's be safe
        # We need relative paths for glob to work nicely with recursive=True sometimes
        # or just join path
        full_pattern = os.path.join(DATA_DIR, pattern)
        files = glob.glob(full_pattern, recursive=True)
        
        for f in files:
            rel_path = os.path.relpath(f, DATA_DIR)
            # Convert backslashes to forward slashes for URLs
            rel_path = rel_path.replace("\\", "/")
            
            # Simple heuristic for type
            asset_type = "video" if f.endswith(".mp4") else "image"
            
            assets.append({
                "path": f"/static/{rel_path}",
                "name": os.path.basename(f),
                "type": asset_type,
                "full_path": rel_path
            })
    return assets

@app.get("/data/{category}/{filename}")
def read_data_file(category: str, filename: str):
    """
    Read a JSON file.
    Category: characters, environments, styles
    """
    if category not in ["characters", "environments", "styles"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    file_path = os.path.join(DATA_DIR, category, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file_path, "r") as f:
        content = f.read()
    
    return {"content": content}

@app.post("/data/{category}/{filename}")
def save_data_file(category: str, filename: str, request: FileSaveRequest):
    """
    Save a JSON file.
    """
    if category not in ["characters", "environments", "styles"]:
        raise HTTPException(status_code=400, detail="Invalid category")
        
    file_path = os.path.join(DATA_DIR, category, filename)
    
    # Simple validation that it is parsable JSON
    try:
        json.loads(request.content)
    except json.JSONDecodeError:
         raise HTTPException(status_code=400, detail="Invalid JSON content")

    with open(file_path, "w") as f:
        f.write(request.content)
    
    return {"status": "success"}

@app.get("/files/{category}")
def list_files(category: str):
    """List all json files in a category."""
    if category not in ["characters", "environments", "styles"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    dir_path = os.path.join(DATA_DIR, category)
    if not os.path.exists(dir_path):
        return []
        
    files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
    return files