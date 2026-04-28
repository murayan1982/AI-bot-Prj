from fastapi import FastAPI

from app.engines.base import ConversationEngine
from app.engines.mock_engine import MockConversationEngine
from app.models.advice import AdviceRequest, AdviceResponse
from app.models.character import CharacterPreset


app = FastAPI(
    title="Daily Rhythm Companion API",
    version="0.1.0",
)

conversation_engine: ConversationEngine = MockConversationEngine()


CHARACTER_PRESETS: list[CharacterPreset] = [
    CharacterPreset(
        character_id="gentle_mina",
        display_name="ミナ",
        description="やさしく落ち着いた朝の案内役。",
        personality_type="gentle",
        speaking_style="casual",
        advice_style="rest_focused",
    ),
    CharacterPreset(
        character_id="cheerful_sora",
        display_name="ソラ",
        description="明るく元気に背中を押してくれる相棒。",
        personality_type="cheerful",
        speaking_style="casual",
        advice_style="positive",
    ),
    CharacterPreset(
        character_id="cool_rei",
        display_name="レイ",
        description="落ち着いて短く実用的に助言する秘書タイプ。",
        personality_type="cool",
        speaking_style="concise",
        advice_style="practical",
    ),
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/characters", response_model=list[CharacterPreset])
def list_characters():
    return CHARACTER_PRESETS


@app.post("/advice", response_model=AdviceResponse)
def create_advice(request: AdviceRequest):
    return conversation_engine.create_advice(request)