import os
import json
from .vertex_ai import generate_visual_from_sheet
from .parser import create_character_reference_prompts

def generate_character_references(character_id: str, data_dir: str = "data/characters"):
    """
    Orchestrates the generation and saving of character references.
    """
    # 1. Load Character Data
    char_path = os.path.join(data_dir, f"{character_id}.json")
    if not os.path.exists(char_path):
        raise FileNotFoundError(f"Character file not found: {char_path}")
    
    with open(char_path, "r") as f:
        character_data = json.load(f)
    
    # 2. Generate Prompts
    prompts = create_character_reference_prompts(character_data)
    
    # 3. Setup Folders
    ref_folder = os.path.join(data_dir, f"{character_id}_refs")
    os.makedirs(ref_folder, exist_ok=True)
    
    import time
    image_references = {}
    for ref_type, prompt in prompts.items():
        img_filename = f"{ref_type}.jpg"
        img_path = os.path.join(ref_folder, img_filename)
        
        # Check if already exists to save quota
        if os.path.exists(img_path):
            print(f"Skipping {ref_type} reference (already exists at {img_path})")
            image_references[ref_type] = f"{character_id}_refs/{img_filename}"
            continue

        print(f"\nGenerating {ref_type} reference...")
        print(f"DEBUG: Character Reference Prompt: {prompt}")
        
        from vertexai.preview.vision_models import ImageGenerationModel
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
        
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            add_watermark=False,
            safety_filter_level="block_only_high",
            person_generation="allow_all",
        )
        
        images[0].save(img_path)
        image_references[ref_type] = f"{character_id}_refs/{img_filename}"
        print(f"Saved {ref_type} reference to {img_path}")
        
        # Small delay to avoid 429 Quota Exceeded
        print("Waiting 5 seconds for quota reset...")
        time.sleep(5)

    # 5. Update JSON
    character_data["reference_images"] = image_references
    with open(char_path, "w") as f:
        json.dump(character_data, f, indent=4)
    
    print(f"Updated {char_path} with reference images.")
    return image_references
