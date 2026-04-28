from app.engines.base import ConversationEngine
from app.models.advice import AdviceRequest, AdviceResponse


class MockConversationEngine(ConversationEngine):
    """
    Development-only conversation engine.

    This engine returns a deterministic response without calling
    any external LLM provider or the framework.
    """

    def create_advice(self, request: AdviceRequest) -> AdviceResponse:
        sleep_hours = request.sleep.total_sleep_minutes // 60
        sleep_minutes = request.sleep.total_sleep_minutes % 60

        message = (
            f"{request.character.display_name}です。"
            f"昨夜の睡眠は{sleep_hours}時間{sleep_minutes}分くらいですね。"
            f"今の気分は「{request.mood}」として受け取りました。"
            "今日は無理に詰め込みすぎず、軽めのタスクから始めるのがよさそうです。"
        )

        return AdviceResponse(
            message=message,
            character_name=request.character.display_name,
        )