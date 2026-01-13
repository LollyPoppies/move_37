import os
import vertexai
from .parser import create_prompt_from_sheet
from dotenv import load_dotenv
from vertexai.preview.vision_models import ImageGenerationModel

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "move-37")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_visual_from_sheet(sheet_data: dict, sheet_type: str = "character", number_of_images: int = 4):
    
    # 1. Generate Prompt
    print("DEBUG: Starting Prompt Generation...")
    refined_prompt = create_prompt_from_sheet(sheet_data)
    print(f"DEBUG: Refined Prompt: {refined_prompt[:50]}...")

    # 2. Generate Image
    print("DEBUG: Starting Image Generation...")
    imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    images = imagen_model.generate_images(
        prompt=refined_prompt,
        number_of_images=number_of_images,
        aspect_ratio="16:9",
        # You can't use a seed value and watermark at the same time.
        add_watermark=False,
        # seed=100,
        safety_filter_level="block_only_high",
        person_generation="allow_all",
    )
    print(f"Created output image using {len(images[0]._image_bytes)} bytes")

    # Return the list of image objects directly
    return images.images