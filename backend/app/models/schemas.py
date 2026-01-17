from pydantic import BaseModel
from typing import List, Optional

class CharacterSheet(BaseModel):
    character_id: Optional[str] = None
    name: str
    physical_traits: dict
    style_id: Optional[str] = None
    clothing: str

class EnvironmentSheet(BaseModel):
    location_name: str
    lighting: str
    time_of_day: str
    mood: str
    weather: Optional[str] = "Clear"