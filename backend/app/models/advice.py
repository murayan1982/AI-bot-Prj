from pydantic import BaseModel

from app.models.character import CharacterContext
from app.models.sleep import SleepSummary


class AdviceRequest(BaseModel):
    character: CharacterContext
    sleep: SleepSummary
    mood: str


class AdviceResponse(BaseModel):
    message: str
    character_name: str