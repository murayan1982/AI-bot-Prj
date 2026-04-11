# llm/grok_engine.py (イメージ)
import re
from xai_sdk import Client
from config.settings import XAI_API_KEY, ACTIVE_LLM_MODEL, TARGET_LANGUAGE

class GrokEngine:
    def __init__(self, system_instruction: str):
        self.client = Client(api_key=XAI_API_KEY)
        self.model_id = ACTIVE_LLM_MODEL
        # Gemini版と同様にTARGET_LANGUAGEを指示に含める
        self.base_instruction = f"{system_instruction}\n\nRespond in {TARGET_LANGUAGE}."
        
    def ask_stream(self, text: str):
        # xAI SDKでのストリーミング実装
        chat = self.client.chat.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": self.base_instruction},
                {"role": "user", "content": text}
            ],
            stream=True
        )
        
        buffer = ""
        tag_pattern = re.compile(r'\[([a-zA-Z0-9_]+)\]')
        
        for response, chunk in chat.stream():
            if chunk.content:
                buffer += chunk.content
                # 既存の感情タグ抽出ロジック（Gemini版から移植）
                if "[" in buffer and "]" in buffer:
                    emotions = tag_pattern.findall(buffer)
                    clean_text = tag_pattern.sub('', buffer)
                    yield clean_text, emotions
                    buffer = ""
                elif len(buffer) > 100:
                    yield buffer, []
                    buffer = ""