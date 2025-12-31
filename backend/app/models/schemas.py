from pydantic import BaseModel
from typing import List, Optional

class CharacterSheet(BaseModel):
    name: str
    age_range: str
    hair_details: str
    eye_color: str
    clothing_description: str
    art_style: str = "Cinematic Anime"
    physical_traits: List[str] = []

class EnvironmentSheet(BaseModel):
    location_name: str
    lighting: str
    time_of_day: str
    mood: str
    weather: Optional[str] = "Clear"