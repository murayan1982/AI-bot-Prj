from __future__ import annotations

import os
from typing import TYPE_CHECKING, Generator

from llm.base import BaseLLM

if TYPE_CHECKING:
    from config.loader import RuntimeConfig


LANGUAGE_NAMES = {
    "ja": "Japanese",
    "en": "English",
}

DEFAULT_TEXT_CHAT_PRESET = "text_chat"

# Public-facing aliases for app developers. Internal provider identifiers remain
# owned by llm.factory / registry.llm.
PROVIDER_ALIASES = {
    "gemini": "google",
    "grok": "xai",
}

EMOTION_TAG_INSTRUCTION = """At the beginning of every assistant response, output exactly one emotion tag:
[emotion:neutral], [emotion:happy], [emotion:sad], [emotion:angry], [emotion:surprised], or [emotion:confused].
After the tag, write the normal response text.
Do not output multiple emotion tags."""


class FacadeError(Exception):
    """Base exception for public facade integration errors."""


class FacadeConfigError(FacadeError):
    """Raised when facade preset or text-only configuration is invalid."""


class FacadeProviderError(FacadeError):
    """Raised when facade provider/model resolution or creation fails."""


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


def _resolve_preset_name(preset: str | None) -> str:
    """Resolve facade preset priority: explicit argument -> .env -> default."""
    if preset:
        return preset

    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
    else:
        load_dotenv()

    return os.getenv("APP_PRESET", DEFAULT_TEXT_CHAT_PRESET)


def _is_text_only_config(config: "RuntimeConfig") -> bool:
    """Return whether a RuntimeConfig is compatible with the text facade."""
    return (
        not config.input_voice_enabled
        and not config.output_voice_enabled
        and not config.vts_enabled
        and config.tts_provider == "none"
    )


def _validate_text_only_config(config: "RuntimeConfig") -> None:
    """Reject presets that would require runtime systems outside the facade."""
    if _is_text_only_config(config):
        return

    raise FacadeConfigError(
        "create_text_chat_session() currently supports text-only presets only. "
        f"Preset '{config.app_preset}' enables one or more unsupported runtime features: "
        f"input_voice_enabled={config.input_voice_enabled}, "
        f"output_voice_enabled={config.output_voice_enabled}, "
        f"vts_enabled={config.vts_enabled}, "
        f"tts_provider={config.tts_provider!r}. "
        "Use a text-only preset such as 'text_chat', or launch main.py for full runtime features."
    )


def _load_facade_config(
    preset: str | None,
    character_name: str | None,
) -> "RuntimeConfig":
    """Build RuntimeConfig for the public facade without starting the runtime loop.

    Boundary rules:
    - explicit function arguments override preset / environment defaults
    - APP_PRESET is used only when preset is not passed
    - character_name overrides the character selected by the preset
    - only text-only presets are accepted by the public text-chat facade
    """
    from config.loader import (
        RuntimeConfig,
        load_character_data,
        load_preset_file,
        normalize_language_code,
    )

    preset_name = _resolve_preset_name(preset)

    try:
        preset_data = load_preset_file(preset_name)
    except FileNotFoundError as e:
        raise FacadeConfigError(
            f"Facade preset not found: {preset_name!r}. "
            "Pass an existing text-only preset name, such as 'text_chat'."
        ) from e

    resolved_character_name = character_name or preset_data.get(
        "character_name",
        preset_data.get("character", "default"),
    )

    try:
        character_data = load_character_data(resolved_character_name)
    except FileNotFoundError as e:
        raise FacadeConfigError(
            f"Facade character not found: {resolved_character_name!r}. "
            "Pass an existing character name or update the selected preset."
        ) from e

    config = RuntimeConfig(
        app_preset=preset_name,
        input_language_code=normalize_language_code(
            preset_data.get("input_language_code", "ja"),
            default="ja",
        ),
        output_language_code=normalize_language_code(
            preset_data.get("output_language_code", "ja"),
            default="en",
        ),
        input_voice_enabled=bool(preset_data.get("input_voice_enabled", False)),
        output_voice_enabled=bool(preset_data.get("output_voice_enabled", False)),
        vts_enabled=bool(preset_data.get("vts_enabled", False)),
        tts_provider=preset_data.get("tts_provider", "none"),
        allow_text_fallback_during_stt=bool(
            preset_data.get("allow_text_fallback_during_stt", False)
        ),
        emotion_enabled=bool(preset_data.get("emotion_enabled", False)),
        vts_emotion_enabled=bool(preset_data.get("vts_emotion_enabled", False)),
        character_name=resolved_character_name,
        character_profile=character_data.profile,
        system_prompt=character_data.system_prompt,
        vts_hotkeys=character_data.vts_hotkeys,
    )

    _validate_text_only_config(config)
    return config


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


def _build_catalog_llm(llm_name: str, system_instruction: str) -> BaseLLM:
    """Build one catalog LLM without importing the full runtime builder."""
    from llm.factory import create_llm
    from registry.llm import LLM_CATALOG

    if llm_name not in LLM_CATALOG:
        raise FacadeProviderError(f"Unknown LLM catalog entry: {llm_name}")

    llm_config = LLM_CATALOG[llm_name]

    try:
        return create_llm(
            provider=llm_config["provider"],
            model=llm_config["model"],
            system_instruction=system_instruction,
        )
    except ValueError as e:
        raise FacadeProviderError(str(e)) from e


def _normalize_provider(provider: str) -> str:
    """Normalize public provider aliases to internal provider identifiers."""
    normalized = provider.strip().lower()
    return PROVIDER_ALIASES.get(normalized, normalized)


def _resolve_default_model_for_provider(provider: str) -> str:
    """Resolve the first registry model matching a provider.

    The registry remains the owner of default provider/model pairs. The facade
    only selects an existing catalog model when an app passes provider without a
    model override.
    """
    from registry.llm import LLM_CATALOG

    for llm_config in LLM_CATALOG.values():
        if llm_config.get("provider") == provider:
            return llm_config["model"]

    raise FacadeProviderError(
        f"No default model is registered for provider {provider!r}. "
        "Pass both provider and model, or add the provider to registry.llm.LLM_CATALOG."
    )


def _resolve_provider_model(
    provider: str,
    model: str | None,
) -> tuple[str, str]:
    """Validate facade provider/model arguments and resolve model defaults."""
    from llm.factory import get_supported_llm_providers

    resolved_provider = _normalize_provider(provider)
    supported_providers = get_supported_llm_providers()

    if resolved_provider not in supported_providers:
        public_aliases = sorted(PROVIDER_ALIASES.keys())
        raise FacadeProviderError(
            f"Unsupported facade provider: {provider!r}. "
            f"Supported providers: {sorted(supported_providers)}. "
            f"Aliases: {public_aliases}."
        )

    resolved_model = model or _resolve_default_model_for_provider(resolved_provider)
    return resolved_provider, resolved_model


def _build_direct_provider_llm(
    provider: str,
    model: str | None,
    system_instruction: str,
) -> BaseLLM:
    """Build one explicitly selected provider/model for facade integration use."""
    from llm.factory import create_llm

    resolved_provider, resolved_model = _resolve_provider_model(
        provider=provider,
        model=model,
    )

    try:
        return create_llm(
            provider=resolved_provider,
            model=resolved_model,
            system_instruction=system_instruction,
        )
    except ValueError as e:
        raise FacadeProviderError(str(e)) from e


def _build_text_chat_llm(
    system_instruction: str,
    provider: str | None,
    model: str | None,
) -> BaseLLM:
    """Build the public facade's text-chat LLM path.

    When provider is omitted, the facade keeps the v2.3 behavior and uses the
    chat route with fallback. When provider is provided, it builds exactly one
    provider/model pair so external apps can choose their integration boundary.
    """
    if provider:
        return _build_direct_provider_llm(
            provider=provider,
            model=model,
            system_instruction=system_instruction,
        )

    from llm.fallback_llm import FallbackLLM
    from registry.llm import LLM_ROUTES

    route_config = LLM_ROUTES["chat"]
    primary = _build_catalog_llm(route_config["primary"], system_instruction)
    fallback = _build_catalog_llm(route_config["fallback"], system_instruction)

    return FallbackLLM(primary, fallback)


def create_text_chat_session(
    preset: str | None = None,
    character_name: str | None = None,
    provider: str | None = None,
    model: str | None = None,
) -> TextChatSession:
    """Create a text-only chat session without starting the app runtime loop.

    Args:
        preset: Optional text-only preset name. When omitted, APP_PRESET is used
            if available, otherwise 'text_chat' is used.
        character_name: Optional character override. When omitted, the character
            configured by the selected preset is used.
        provider: Optional direct LLM provider override. When omitted, the
            facade uses the default chat route with fallback.
        model: Optional model override for the selected provider. Ignored when
            provider is omitted.
    """
    config = _load_facade_config(
        preset=preset,
        character_name=character_name,
    )
    system_instruction = _build_system_instruction(config)
    llm = _build_text_chat_llm(
        system_instruction=system_instruction,
        provider=provider,
        model=model,
    )
    return TextChatSession(llm)
