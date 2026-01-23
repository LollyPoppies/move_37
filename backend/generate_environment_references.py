import argparse
import sys
import os

# Add backend to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from app.services.environment_refs import generate_environment_references

def main():
    parser = argparse.ArgumentParser(description="Generate environment reference images for Veo.")
    parser.add_argument("environment_id", help="The ID of the environment (e.g., 'Neon_Alleway' if Neon_Alleway.json exists in data/environments/)")
    parser.add_argument("--data-dir", default="data/environments", help="Directory containing environment JSON files.")
    
    args = parser.parse_args()
    
    try:
        print(f"Starting environment reference generation for: {args.environment_id}")
        image_refs = generate_environment_references(args.environment_id, args.data_dir)
        print("\nSuccess!")
        print(f"Environment images generated and saved. JSON updated.")
        for ref_type, path in image_refs.items():
            print(f"  - {ref_type}: {path}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
