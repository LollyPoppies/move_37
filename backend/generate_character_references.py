import argparse
import sys
import os

# Add backend to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from app.services.character_refs import generate_character_references

def main():
    parser = argparse.ArgumentParser(description="Generate character reference images for Veo.")
    parser.add_argument("character_id", help="The ID of the character (e.g., 'kaelen' if kaelen.json exists in data/characters/)")
    parser.add_argument("--style", "-s", "-c", help="Optional style ID (e.g., 'noir', 'claymation') to override character's default.")
    parser.add_argument("--type", "-t", choices=["head", "full_body", "side", "back"], help="Optional specific reference type to generate.")
    parser.add_argument("--num-images", "-n", type=int, default=1, help="Number of images to generate per reference angle (default: 1).")
    parser.add_argument("--force", "-f", action="store_true", help="Force regeneration of images even if they exist.")
    parser.add_argument("--data-dir", default="data/characters", help="Directory containing character JSON files.")
    
    args = parser.parse_args()
    
    if args.num_images < 1:
        print("Error: --num-images must be at least 1.")
        sys.exit(1)
        
    try:
        print(f"Starting character reference generation for: {args.character_id}")
        if args.style:
            print(f"Style override: {args.style}")
        if args.type:
            print(f"Targeting reference type: {args.type}")
        if args.force:
            print("Force mode enabled: Regenerating existing images.")
        if args.num_images > 1:
            print(f"Generating {args.num_images} images per angle.")
            
        image_refs = generate_character_references(args.character_id, args.data_dir, style_id=args.style, force=args.force, num_images=args.num_images, target_type=args.type)
        print("\nSuccess!")
        print(f"Character images generated and saved. JSON updated.")
        for ref_type, path in image_refs.items():
            print(f"  - {ref_type}: {path}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
