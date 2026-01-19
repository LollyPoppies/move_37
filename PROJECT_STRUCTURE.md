# Project Structure

This document provides a high-level overview of the **Move 37** project structure and functionality.

## Overview

Move 37 is a creative project that uses Vertex AI to generate visuals based on structured JSON data definitions (Character Sheets and Environment Sheets). The backend uses FastAPI to expose endpoints for batch rendering.

## Directory Layout

### Root Directory

- **`backend/`**: Contains the core application logic, API, and AI integration services.
- **`data/`**: Stores the structured JSON files that define the content to be generated.
- **`renders/`**: Destination directory for generated image assets.
- **`requirements.txt`**: Python dependencies (FastAPI, Google Cloud AI Platform, Pydantic, etc.).
- **`README.md`**: Project initialization and basic info.

### `backend/`

The backend is structured as a Python package.

- **`app/`**: Main application package.
  - **`main.py`**: The entry point for the FastAPI application. Defines the `/batch-render` endpoint which orchestrates the reading of JSON files and calls the generation service.
  - **`models/`**: Pydantic data models.
    - **`schemas.py`**: Defines `CharacterSheet` and `EnvironmentSheet` schemas for data validation.
  - **`services/`**: logic for external integrations and data processing.
    - **`parser.py`**: Contains `create_prompt_from_sheet`. This function transforms the structured JSON data into a descriptive natural language prompt optimized for the image generation model.
    - **`vertex_ai.py`**: Handles the connection to Google Vertex AI. Validates credentials, initializes the `ImageGenerationModel`, and sends the prompt to generate images.

- **Test Scripts**:
  - **`test_parser_local.py`**: A CLI script to test the prompt generation logic without making API calls. Useful for debugging how JSON data is converted to text prompts.
  - **`test_vertex_local.py`**: A script to test the integration with Vertex AI.

### `data/`

Contains the source of truth for the creative assets.

- **`characters/`**: JSON files defining characters (e.g., *kaelen.json*).
- **`environment_sheets/`**: JSON files defining settings/locations.

## Data Flow

1. **Input**: A JSON file in `data/characters` defines a character's traits (hair, eyes, outfit, style).
2. **Parsing**: The `/batch-render` endpoint triggers the process. `services.parser` reads the JSON and constructs a detailed text prompt.
3. **Generation**: `services.vertex_ai` receives the prompt and calls Google's Imagen model via Vertex AI.
4. **Output**: The generated images are returned (and potentially saved/served).
