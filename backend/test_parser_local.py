import sys
import os
import json
import argparse

# Ensure the current directory (backend) is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.parser import create_prompt_from_sheet

def test_parser():
    parser = argparse.ArgumentParser(description="Test parser.py with a character sheet JSON.")
    parser.add_argument("file_path", nargs="?", help="Path to the character sheet JSON file.")
    args = parser.parse_args()

    if args.file_path:
        try:
            with open(args.file_path, 'r') as f:
                sheet_data = json.load(f)
            print(f"Loaded character sheet from: {args.file_path}")
        except FileNotFoundError:
            print(f"Error: File not found at {args.file_path}")
            return
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {args.file_path}")
            return
    else:
        # Fallback to local sample if no file provided
        default_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'character_sheets', 'kaelen.json')
        if os.path.exists(default_path):
            print(f"No file provided, using default: {default_path}")
            with open(default_path, 'r') as f:
                sheet_data = json.load(f)
        else:
            print("No file provided and default 'kaelen.json' not found. Using hardcoded sample.")
            sheet_data = {
                "physical_traits": {
                    "hair": "messy brown",
                    "eyes": "green"
                },
                "style": {
                    "art_style": "Studio Ghibli watercolor"
                },
                "clothing": "worn adventurer's cloak and leather armor"
            }

    print("Input Character Data:")
    print(sheet_data)
    print("\nGenerating Prompt...")

    try:
        result = create_prompt_from_sheet(sheet_data)
        print("\n--- Output Prompt ---")
        print(result)
        print("---------------------")
    except KeyError as e:
        print(f"Error: Missing key in input data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_parser()
