import os
import vertexai
from .parser import create_prompt_from_sheet
from dotenv import load_dotenv
from vertexai.preview.vision_models import ImageGenerationModel

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "move-37")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_visual_from_sheet(sheet_data: dict, sheet_type: str = "character"):
    
    # 1. Generate Prompt
    print("DEBUG: Starting Prompt Generation...")
    refined_prompt = create_prompt_from_sheet(sheet_data)
    print(f"DEBUG: Refined Prompt: {refined_prompt[:50]}...")

    # 2. Generate Image
    print("DEBUG: Starting Image Generation...")
    imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    images = imagen_model.generate_images(
        prompt=refined_prompt,
        number_of_images=1,
        aspect_ratio="16:9" if sheet_type == "environment" else "1:1",
        add_watermark=False,
        safety_filter_level="block_only_high",
        person_generation="allow_all",
    )
    print(f"DEBUG: Generated {len(images)} images.")

    # 3. Save Image
    output_dir = os.path.join(os.getcwd(), 'output', 'characters')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{sheet_data.get('name', 'asset')}.png"
    output_filename = os.path.join(output_dir, filename)
    
    images[0].save(location=output_filename)
    
    return output_filename