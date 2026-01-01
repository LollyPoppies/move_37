import os
import vertexai
from dotenv import load_dotenv
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.generative_models import GenerativeModel

# Load settings from .env file
load_dotenv()

# Configuration - Replace with your project details
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "move-37")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_visual_from_sheet(sheet_data: dict, sheet_type: str = "character"):
    """
    Translates a JSON sheet into a high-quality movie asset.
    sheet_type can be 'character' or 'environment'.
    """
    # 1. Use Gemini to turn JSON into a professional prompt
    # This ensures the 'non-creative' user gets a 'creative' result
    vision_model = GenerativeModel("gemini-1.5-flash")
    prompt_generator = vision_model.generate_content(
        f"Convert this {sheet_type} JSON into a cinematic prompt for an AI image generator. "
        f"Focus on lighting, art style, and specific details: {str(sheet_data)}"
    )
    refined_prompt = prompt_generator.text

    # 2. Use Imagen 3 to generate the actual image
    imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    
    images = imagen_model.generate_images(
        prompt=refined_prompt,
        number_of_images=1,
        aspect_ratio="16:9" if sheet_type == "environment" else "1:1",
        add_watermark=False # Set to True for production safety
    )

    # 3. Save locally (for now)
    output_filename = f"{sheet_data.get('name', 'asset')}.png"
    images[0].save(location=output_filename)
    
    return output_filename

if __name__ == "__main__":
    print("Running vertex_ai.py test...")
    
    # Check for Project ID
    if os.getenv("GCP_PROJECT_ID") is None and PROJECT_ID == "move-37":
        print("WARNING: Using default Project ID 'move-37'. This may not work if you don't have access to it.")
        print("Tip: Set the GCP_PROJECT_ID environment variable or create a .env file.")

    # Test data
    test_sheet = {
        "name": "Test Character",
        "description": "A futuristic robot with glowing neon blue eyes and a metallic finish.",
        "type": "character"
    }
    
    try:
        result = generate_visual_from_sheet(test_sheet, "character")
        print(f"Success! Image generated: {result}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print(f"1. Current Project ID: {PROJECT_ID}")
        print("2. Make sure you have run: gcloud auth application-default login")
        print(f"3. Make sure the Vertex AI API is enabled for project '{PROJECT_ID}'")