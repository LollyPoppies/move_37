import json
import os

def load_json_data(directory, file_id):
    """Helper to load JSON data from a specific data directory."""
    if not file_id:
        return {}
    
    # Remove .json extension if provided in file_id
    if file_id.endswith(".json"):
        file_id = file_id[:-5]
        
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", directory, f"{file_id}.json"))
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    print(f"WARNING: File {file_id}.json not found at {path}")
    return {}

def parse_scene(scene_data: dict):
    """
    Implements the 5-part formula for optimal control:
    [Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]
    """
    # 1. Cinematography
    shot_type = scene_data.get('cinematography', 'medium_shot')
    cinematography_data = load_json_data("cinematography", "default")
    cinematography = cinematography_data.get(shot_type, shot_type.replace("_", " ").capitalize())

    # 2. Subject (Character)
    character_id = scene_data.get('character_id')
    character_data = load_json_data("characters", character_id)
    subject_name = character_data.get('name', character_id or 'Unknown Character')
    traits = character_data.get('physical_traits', {})
    hair = traits.get('hair', '')
    eyes = traits.get('eyes', '')
    clothing = character_data.get('clothing', '')
    subject = f"{subject_name}"
    if hair or eyes or clothing:
        details = ", ".join(filter(None, [hair, eyes, clothing]))
        subject += f" ({details})"

    # 3. Action
    action = scene_data.get('action', 'standing still')

    # 4. Context (Environment)
    env_id = scene_data.get('environment_id')
    env_data = load_json_data("environment_sheets", env_id)
    location = env_data.get('location', 'unspecified location')
    weather = env_data.get('weather', '')
    context = f"in {location}"
    if weather:
        context += f" during {weather}"

    # 5. Style & Ambiance
    style_id = scene_data.get('style_id') or character_data.get('style_id')
    style_data = load_json_data("styles", style_id)
    art_style = style_data.get('art_style', 'Cinematic')
    lighting = style_data.get('lighting', '')
    camera = style_data.get('camera_language', {})
    lens = camera.get('lens', '')
    
    ambiance = f"{art_style} style"
    if lighting:
        ambiance += f", {lighting} lighting"
    if lens:
        ambiance += f", shot on {lens}"

    # Construct final prompt
    prompt = f"{cinematography}, {subject}, {action}, {context}. {ambiance}."
    return prompt

def create_prompt_from_sheet(sheet_json: dict):
    """Main entry point for prompt generation. Supports scene and legacy formats."""
    if 'scenes' in sheet_json:
        # Sequence format
        prompts = []
        for scene in sheet_json['scenes']:
            prompts.append(parse_scene(scene))
        return "\n\n".join(prompts)
    
    # Legacy character sheet format (wrapped to use parse_scene logic)
    # We try to extract character_id if it's there, otherwise we use the name
    char_id = sheet_json.get('character_id') or sheet_json.get('name', 'legacy').lower()
    scene_mock = {
        "character_id": char_id,
        "cinematography": "medium_shot",
        "action": "posing",
        "style_id": sheet_json.get('style_id')
    }
    return parse_scene(scene_mock)
def create_character_reference_prompts(character_data: dict):
    """
    Generates 3 specialized prompts for Veo character references:
    1. Hero Shot (Frontal)
    2. 3/4 Profile
    3. Full Back
    """
    name = character_data.get('name', 'Unknown')
    traits = character_data.get('physical_traits', {})
    hair = traits.get('hair', '')
    eyes = traits.get('eyes', '')
    clothing = character_data.get('clothing', '')
    
    # Get style info if possible
    style_id = character_data.get('style_id')
    style_data = load_json_data("styles", style_id)
    art_style = style_data.get('art_style', 'Cinematic')
    
    base_description = f"{name}"
    if hair or eyes or clothing:
        details = ", ".join(filter(None, [hair, eyes, clothing]))
        base_description += f" ({details})"
    
    prompts = {
        "front": f"The 'Hero' Shot (Frontal). Clear, eye-level view of the face and upper body of {base_description}. This defines the primary identity. {art_style} style, high detail.",
        "side": f"The 3/4 Profile of {base_description}. Crucial for movement, showing the bridge of the nose, jawline, and how hair sits on the side of the head. {art_style} style, high detail.",
        "back": f"Full Back view of {base_description}. Defines the silhouette and clothing details. {art_style} style, high detail."
    }
    
    return prompts
