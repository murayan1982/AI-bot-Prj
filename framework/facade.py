from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Generator

from llm.base import BaseLLM

if TYPE_CHECKING:
    from config.loader import RuntimeConfig


LANGUAGE_NAMES = {
    "ja": "Japanese",
    "en": "English",
}

EMOTION_TAG_INSTRUCTION = """At the beginning of every assistant response, output exactly one emotion tag:
[emotion:neutral], [emotion:happy], [emotion:sad], [emotion:angry], [emotion:surprised], or [emotion:confused].
After the tag, write the normal response text.
Do not output multiple emotion tags."""


class TextChatSession:
    """Public text-chat session facade.

    This class is the small public entry point for developers who want to use
    the framework as a library instead of launching the interactive main loop.
    It owns one LLM instance and exposes simple text-only turn methods.
    """

    def __init__(self, llm: BaseLLM):
        self._llm = llm

    def ask(self, text: str) -> str:
        """Send one text turn and return the full assistant response."""
        return "".join(self.ask_stream(text))

    def ask_stream(self, text: str) -> Generator[str, None, None]:
        """Send one text turn and yield assistant response chunks."""
        for chunk, _emotions in self._llm.ask_stream(text):
            if chunk:
                yield chunk

    def reset(self) -> None:
        """Reset provider-owned conversation state when supported."""
        self._llm.reset_session()


def _build_system_instruction(config: "RuntimeConfig") -> str:
    """Build the same language/system instruction used by the runtime layer."""
    base_system_prompt = config.system_prompt.strip()
    output_language_name = LANGUAGE_NAMES.get(
        config.output_language_code,
        "English",
    )

    language_instruction = (
        f"You MUST write your entire response in {output_language_name}. "
        f"All explanations, headings, bullet points, and sentences must be in "
        f"{output_language_name}. "
        f"You are NOT allowed to output any other language. "
        f"If you generate content in another language, you must immediately rewrite it in "
        f"{output_language_name}. "
        f"Keep only code, commands, file paths, URLs, and proper nouns unchanged."
    )

    instruction_parts = [language_instruction]

    if config.emotion_enabled:
        instruction_parts.append(EMOTION_TAG_INSTRUCTION)

    if base_system_prompt:
        instruction_parts.append(base_system_prompt)

    return "\n\n".join(instruction_parts)


def _as_text_chat_config(config: "RuntimeConfig") -> "RuntimeConfig":
    """Force text-only runtime flags for the public text-chat facade."""
    return replace(
        config,
        app_preset="text_chat",
        input_voice_enabled=False,
        output_voice_enabled=False,
        vts_enabled=False,
        tts_provider="none",
        allow_text_fallback_during_stt=False,
        vts_emotion_enabled=False,
    )


def _build_catalog_llm(llm_name: str, system_instruction: str) -> BaseLLM:
    """Build one catalog LLM without importing the full runtime builder."""
    from llm.factory import create_llm
    from registry.llm import LLM_CATALOG

    if llm_name not in LLM_CATALOG:
        raise ValueError(f"Unknown LLM catalog entry: {llm_name}")

    llm_config = LLM_CATALOG[llm_name]

    return create_llm(
        provider=llm_config["provider"],
        model=llm_config["model"],
        system_instruction=system_instruction,
    )


def _build_text_chat_llm(system_instruction: str) -> BaseLLM:
    """Build the public facade's text-chat LLM path."""
    from llm.fallback_llm import FallbackLLM
    from registry.llm import LLM_ROUTES

    route_config = LLM_ROUTES["chat"]
    primary = _build_catalog_llm(route_config["primary"], system_instruction)
    fallback = _build_catalog_llm(route_config["fallback"], system_instruction)

    return FallbackLLM(primary, fallback)


def create_text_chat_session() -> TextChatSession:
    """Create a text-only chat session without starting the app runtime loop."""
    from config.loader import load_runtime_config

    config = _as_text_chat_config(load_runtime_config())
    system_instruction = _build_system_instruction(config)
    llm = _build_text_chat_llm(system_instruction)
    return TextChatSession(llm)
