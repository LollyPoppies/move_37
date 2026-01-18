import argparse
import sys
import os

# Add backend to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from app.services.character_refs import generate_character_references

def main():
    parser = argparse.ArgumentParser(description="Generate character reference images for Veo.")
    parser.add_argument("character_id", help="The ID of the character (e.g., 'kaelen' if kaelen.json exists in data/characters/)")
    parser.add_argument("--data-dir", default="data/characters", help="Directory containing character JSON files.")
    
    args = parser.parse_args()
    
    try:
        print(f"Starting character reference generation for: {args.character_id}")
        image_refs = generate_character_references(args.character_id, args.data_dir)
        print("\nSuccess!")
        print(f"Character images generated and saved. JSON updated.")
        for ref_type, path in image_refs.items():
            print(f"  - {ref_type}: {path}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
