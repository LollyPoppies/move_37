import json
import os

def create_prompt_from_sheet(sheet_json: dict):
    """Converts your structured character JSON into a rich AI prompt."""
    # 1. Extract high-level data
    name = sheet_json.get('name')
    clothing = sheet_json.get('clothing')
    
    # 2. Extract nested traits
    traits = sheet_json.get('physical_traits', {})
    
    # 3. Handle Style (Local or External)
    style = sheet_json.get('style', {})
    style_id = sheet_json.get('style_id')
    
    if style_id:
        # Load external style
        # Path assumes we are in backend/app/services/
        style_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "styles", f"{style_id}.json"))
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                style = json.load(f)
        else:
            print(f"WARNING: Style file {style_id}.json not found at {style_path}")

    # 4. Extract style details
    art_style = style.get('art_style', 'Cinematic Anime')
    lighting = style.get('lighting', 'cinematic high-contrast')
    camera = style.get('camera_language', {})
    lens = camera.get('lens', '35mm')
    
    # 5. Assign specific variables used in the template
    hair = traits.get('hair', 'unspecified hair')
    eyes = traits.get('eyes', 'unspecified eyes')
    physique = traits.get('physique', 'average build')
    
    # 6. Construct the template
    prompt = (
        f"[Subject: {name}] "
        f"[Identity Anchors: {hair}, {eyes}, {physique}] "
        f"[Outfit: {clothing}] "
        f"[Style: {art_style}] "
        f"[Lighting: {lighting}] "
        f"[Camera: {lens}]"
    )
    
    return prompt