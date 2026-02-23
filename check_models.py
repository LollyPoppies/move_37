import os
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "move-37")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

def check_model(model_id, region):
    try:
        print(f"Checking {model_id} in {region}...")
        vertexai.init(project=PROJECT_ID, location=region)
        model = GenerativeModel(model_id)
        response = model.generate_content("test")
        print(f"SUCCESS: {model_id} in {region}")
        return True
    except Exception as e:
        print(f"FAILED: {model_id} in {region}: {e}")
        return False

regions = ["us-central1", "us-east4", "europe-west1", "europe-west4"]
model_ids = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-flash-002", "models/gemini-1.5-flash"]

for region in regions:
    for model_id in model_ids:
        if check_model(model_id, region):
            break
