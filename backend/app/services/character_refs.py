import os
import json
from .vertex_ai import generate_visual_from_sheet
from .parser import create_character_reference_prompts

def generate_character_references(character_id: str, data_dir: str = "data/characters", style_id: str = None, force: bool = False, num_images: int = 1, target_type: str = None):
    """
    Orchestrates the generation and saving of character references.
    Allows for style-specific overrides and subfolders.
    'force' will regenerate images even if they already exist.
    'num_images' controls how many images per angle (head/full_body/side/back) to generate.
    'target_type' if provided, will only generate that specific angle (e.g., 'head').
    """
    # 1. Load Character Data
    char_path = os.path.join(data_dir, f"{character_id}.json")
    if not os.path.exists(char_path):
        raise FileNotFoundError(f"Character file not found: {char_path}")
    
    with open(char_path, "r") as f:
        character_data = json.load(f)
    
    # Use provided style_id or fallback to character's default style
    effective_style = style_id or character_data.get("style_id", "default_style")
    
    # 2. Generate Prompts
    prompts = create_character_reference_prompts(character_data, style_id=style_id)
    
    # Filter prompts if a target_type is specified
    if target_type:
        if target_type not in prompts:
            raise ValueError(f"Invalid reference type: {target_type}. Valid types are: {list(prompts.keys())}")
        prompts = {target_type: prompts[target_type]}
        print(f"Targeting specific reference type: {target_type}")
    
    # 3. Setup Folders
    # We now use a subfolder for the style to avoid overwriting or mixing styles
    ref_folder = os.path.join(data_dir, f"{character_id}_refs", effective_style)
    os.makedirs(ref_folder, exist_ok=True)
    
    import time
    image_references = {}
    for ref_type, prompt in prompts.items():
        # ... logic to generate images ...
        # Determine filenames and relative paths
        type_images_paths = []
        img_filenames = []
        for i in range(num_images):
            suffix = f"_{i+1}" if num_images > 1 else ""
            filename = f"{ref_type}{suffix}.jpg"
            img_filenames.append(filename)
            type_images_paths.append(f"{character_id}_refs/{effective_style}/{filename}")
        
        # Check if all exist
        all_exist = all(os.path.exists(os.path.join(ref_folder, f)) for f in img_filenames)
        
        if all_exist and not force:
            print(f"Skipping {ref_type} reference (all {num_images} images already exist)")
            image_references[ref_type] = type_images_paths[0] if num_images == 1 else type_images_paths
            continue

        print(f"\nGenerating {num_images} variant(s) for {ref_type} reference in style: {effective_style}...")
        print(f"DEBUG: Character Reference Prompt: {prompt}")
        
        from vertexai.preview.vision_models import ImageGenerationModel
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
        
        images = model.generate_images(
            prompt=prompt,
            number_of_images=num_images,
            aspect_ratio="1:1",
            add_watermark=False,
            safety_filter_level="block_only_high",
            person_generation="allow_all",
            negative_prompt=character_data.get("negative_prompt"),
        )
        
        for idx, image in enumerate(images):
            save_path = os.path.join(ref_folder, img_filenames[idx])
            image.save(save_path)
            print(f"Saved {img_filenames[idx]} reference to {save_path}")
        
        # Store as string if only one, or list if multiple
        image_references[ref_type] = type_images_paths[0] if num_images == 1 else type_images_paths
        
        # Small delay to avoid 429 Quota Exceeded
        print("Waiting 5 seconds for quota reset...")
        time.sleep(5)

    # 5. Update JSON
    # We now store reference images mapped by style_id to support multiple styles
    if "reference_images" not in character_data or not isinstance(character_data["reference_images"], dict):
        character_data["reference_images"] = {}
        
    # If the current structure is the old one (not keyed by style), migrate it or just nest it
    # We check if the first level of keys looks like style IDs or reference types (front/side/back)
    first_key = next(iter(character_data["reference_images"].keys()), None)
    if first_key in ["front", "side", "back", "head", "full_body"]:
        # Legacy format detected, migrate to style-keyed format
        old_refs = character_data["reference_images"]
        old_style = character_data.get("style_id", "legacy")
        character_data["reference_images"] = {old_style: old_refs}

    character_data["reference_images"][effective_style] = image_references
    
    with open(char_path, "w") as f:
        json.dump(character_data, f, indent=4)
    
    print(f"Updated {char_path} with reference images for style '{effective_style}'.")
    return image_references
