# config/settings.py
import os
from dotenv import load_dotenv
from .models import MODEL_MASTER

# read .env 
load_dotenv()

# --- Get API Key ---
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# --- Index Selection ---
SELECT_LLM_INDEX = 25
SELECT_VOICE_INDEX = 0
SELECT_TTS_MODEL_INDEX = 2

# ---  Mode Switches ---
STT_ENGINE = "text"        # "text", "google", "whisper"
TTS_ENGINE = "elevenlabs"  # "elevenlabs", "none"

# --- Dynamic Assignment ---
ACTIVE_LLM_MODEL = MODEL_MASTER["google"][SELECT_LLM_INDEX]
VOICE_ID = MODEL_MASTER["voices"][SELECT_VOICE_INDEX]["id"]
TTS_MODEL_ID = MODEL_MASTER["tts_models"][SELECT_TTS_MODEL_INDEX]

# --- STT Settings ---
LANGUAGE_CODE = "ja-JP"
LANG_MAP = {
    "ja-JP": "Japanese",
    "en-US": "English",
    "zh-CN": "Chinese",
    "ko-KR": "Korean",
    "fr-FR": "French",
    "de-DE": "German"
}
STT_LANGUAGE = LANGUAGE_CODE
TARGET_LANGUAGE = LANG_MAP.get(LANGUAGE_CODE, "English")

# --- Interaction Mode ---
# True: Use Voice, False: Use Text
INPUT_VOICE_ENABLED = False   # If True, STT starts
OUTPUT_VOICE_ENABLED = False  # If True, TTS speaks

# --- google safety settings ---
SAFETY_SETTINGS = {
    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
}

# --- VTube Studio Settings ---
VTS_TOKEN_PATH = os.path.join("config", "tokens", "vts_token.json")
