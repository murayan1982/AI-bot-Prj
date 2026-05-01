"""Smoke checks for the public framework facade.

Default mode is offline-safe and does not call an LLM provider API:

    python scripts/smoke_public_facade.py

Optional live LLM check, requiring API keys in .env:

    python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"

Optional live LLM check with direct provider mode:

    python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


EXPECTED_PUBLIC_API = [
    "FacadeConfigError",
    "FacadeError",
    "FacadeProviderError",
    "TextChatSession",
    "TextChatSessionInfo",
    "create_text_chat_session",
]

FORBIDDEN_IMPORTS_AFTER_FRAMEWORK_IMPORT = [
    "core.runtime",
    "core.session",
    "core.pipeline",
    "stt.stt_engine",
    "tts.voice_engine",
    "live2d.vts_client",
]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_import_boundary() -> None:
    import framework

    _assert(
        list(framework.__all__) == EXPECTED_PUBLIC_API,
        f"Unexpected framework.__all__: {framework.__all__!r}",
    )

    imported_forbidden_modules = [
        module_name
        for module_name in FORBIDDEN_IMPORTS_AFTER_FRAMEWORK_IMPORT
        if module_name in sys.modules
    ]
    _assert(
        not imported_forbidden_modules,
        "framework import should not load runtime/audio/VTS modules: "
        f"{imported_forbidden_modules}",
    )

    print("[OK] import framework exposes the expected public API")
    print("[OK] import framework does not load runtime/audio/VTS modules")


def check_text_only_config_boundary() -> None:
    # This intentionally checks the internal facade boundary without creating an
    # actual LLM instance, so it can run without provider API keys.
    from framework.facade import FacadeConfigError, _load_facade_config

    text_config = _load_facade_config(
        preset="text_chat",
        character_name="default",
    )
    _assert(text_config.app_preset == "text_chat", "text_chat preset was not loaded")
    _assert(not text_config.input_voice_enabled, "text_chat should not enable voice input")
    _assert(not text_config.output_voice_enabled, "text_chat should not enable voice output")
    _assert(not text_config.vts_enabled, "text_chat should not enable VTS")
    _assert(text_config.tts_provider == "none", "text_chat should not enable TTS")

    try:
        _load_facade_config(
            preset="voice_vts",
            character_name="default",
        )
    except FacadeConfigError as e:
        _assert(
            "text-only presets only" in str(e),
            f"Unexpected voice_vts validation error: {e}",
        )
    else:
        raise AssertionError("voice_vts should be rejected by the text facade")

    print("[OK] text_chat is accepted by the text facade boundary")
    print("[OK] voice_vts is rejected by the text facade boundary")


def check_provider_model_resolution() -> None:
    # This checks facade provider/model argument handling without creating
    # provider clients or requiring API keys.
    from framework.facade import FacadeProviderError, _resolve_provider_model

    _assert(
        _resolve_provider_model("openai", None) == ("openai", "gpt-4o-mini"),
        "openai should resolve to the registered default model",
    )
    _assert(
        _resolve_provider_model("gemini", "custom-gemini-model")
        == ("google", "custom-gemini-model"),
        "gemini alias should resolve to internal google provider",
    )
    _assert(
        _resolve_provider_model("grok", "custom-grok-model")
        == ("xai", "custom-grok-model"),
        "grok alias should resolve to internal xai provider",
    )

    try:
        _resolve_provider_model("unknown-provider", None)
    except FacadeProviderError as e:
        _assert(
            "Unsupported facade provider" in str(e),
            f"Unexpected provider validation error: {e}",
        )
    else:
        raise AssertionError("unknown provider should be rejected")

    print("[OK] facade provider/model arguments resolve without creating clients")


def check_session_info_model() -> None:
    # Session info is built from facade arguments and RuntimeConfig without
    # creating provider clients or exposing the internal RuntimeConfig object.
    from framework import TextChatSessionInfo
    from framework.facade import _build_text_chat_info, _load_facade_config

    config = _load_facade_config(
        preset="text_chat",
        character_name="default",
    )

    default_info = _build_text_chat_info(
        config=config,
        provider=None,
        model=None,
    )
    _assert(isinstance(default_info, TextChatSessionInfo), "info should use public type")
    _assert(default_info.preset == "text_chat", "info should expose preset")
    _assert(default_info.character_name == "default", "info should expose character")
    _assert(default_info.llm_mode == "default_route", "default mode should use route")
    _assert(default_info.route_name == "chat", "default route name should be chat")
    _assert(default_info.provider is None, "default route should hide provider")
    _assert(default_info.model is None, "default route should hide model")
    _assert(default_info.api_version == "4.0", "info should expose API version")
    _assert(default_info.session_type == "text_chat", "info should expose session type")
    _assert(default_info.supports_streaming, "text facade should support streaming")
    _assert(default_info.supports_reset, "text facade should support reset")
    _assert(not default_info.supports_interrupt, "text facade should not expose interrupt support yet")
    _assert(not default_info.supports_events, "text facade should not expose event callbacks yet")
    _assert(not default_info.supports_close, "text facade should not expose close support yet")
    _assert(not default_info.supports_voice_input, "text facade should not expose voice input support")
    _assert(not default_info.supports_voice_output, "text facade should not expose voice output support")
    _assert(not default_info.supports_live2d, "text facade should not expose Live2D support")
    
    direct_info = _build_text_chat_info(
        config=config,
        provider="gemini",
        model="custom-gemini-model",
    )
    _assert(isinstance(direct_info, TextChatSessionInfo), "info should use public type")
    _assert(direct_info.llm_mode == "direct_provider", "direct mode should be explicit")
    _assert(direct_info.provider == "google", "provider aliases should be normalized")
    _assert(direct_info.model == "custom-gemini-model", "model override should be exposed")
    _assert(direct_info.route_name is None, "direct provider mode should not expose route")
    _assert(direct_info.api_version == "4.0", "direct info should expose API version")
    _assert(direct_info.session_type == "text_chat", "direct info should expose session type")
    _assert(direct_info.supports_streaming, "direct info should support streaming")
    _assert(direct_info.supports_reset, "direct info should support reset")
    _assert(not direct_info.supports_voice_input, "direct info should not expose voice input support")
    _assert(not direct_info.supports_voice_output, "direct info should not expose voice output support")
    _assert(not direct_info.supports_live2d, "direct info should not expose Live2D support")

    print("[OK] TextChatSessionInfo exposes stable public session metadata")


def _load_example_module(filename: str, module_name: str):
    """Import an example file by path without running it as a script."""
    import importlib.util

    example_path = PROJECT_ROOT / "examples" / filename
    spec = importlib.util.spec_from_file_location(module_name, example_path)
    _assert(spec is not None and spec.loader is not None, "Could not load example spec")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _assert_no_forbidden_runtime_imports(context: str) -> None:
    imported_forbidden_modules = [
        module_name
        for module_name in FORBIDDEN_IMPORTS_AFTER_FRAMEWORK_IMPORT
        if module_name in sys.modules
    ]
    _assert(
        not imported_forbidden_modules,
        f"{context} should not load runtime/audio/VTS modules: "
        f"{imported_forbidden_modules}",
    )


def check_minimal_app_example_import() -> None:
    # The app integration example should be importable without creating an LLM
    # client or loading the full runtime/audio/VTS stack.
    module = _load_example_module(
        "minimal_app_text_chat.py",
        "minimal_app_text_chat_smoke",
    )

    _assert(
        hasattr(module, "MinimalTextChatApp"),
        "minimal app example should expose MinimalTextChatApp",
    )
    _assert(
        hasattr(module, "build_app"),
        "minimal app example should expose build_app",
    )

    _assert_no_forbidden_runtime_imports("minimal app example import")
    print("[OK] minimal app integration example is importable")


def check_error_handling_example_import() -> None:
    # The error handling example should also be importable without creating
    # provider clients or loading the full runtime/audio/VTS stack.
    module = _load_example_module(
        "app_error_handling.py",
        "app_error_handling_smoke",
    )

    _assert(
        hasattr(module, "run_invalid_preset_demo"),
        "error handling example should expose run_invalid_preset_demo",
    )
    _assert(
        hasattr(module, "run_invalid_provider_demo"),
        "error handling example should expose run_invalid_provider_demo",
    )

    _assert_no_forbidden_runtime_imports("error handling example import")
    print("[OK] error handling example is importable")


def check_streaming_example_import() -> None:
    # The streaming example should be importable without creating provider
    # clients or loading the full runtime/audio/VTS stack.
    module = _load_example_module(
        "app_streaming_text_chat.py",
        "app_streaming_text_chat_smoke",
    )

    _assert(
        hasattr(module, "StreamingTextChatApp"),
        "streaming example should expose StreamingTextChatApp",
    )
    _assert(
        hasattr(module, "build_app"),
        "streaming example should expose build_app",
    )

    _assert_no_forbidden_runtime_imports("streaming example import")
    print("[OK] streaming text chat example is importable")


def check_reset_example_import() -> None:
    # The reset example should be importable without creating provider clients
    # or loading the full runtime/audio/VTS stack.
    module = _load_example_module(
        "app_reset_text_chat.py",
        "app_reset_text_chat_smoke",
    )

    _assert(
        hasattr(module, "ResettableTextChatApp"),
        "reset example should expose ResettableTextChatApp",
    )
    _assert(
        hasattr(module, "build_app"),
        "reset example should expose build_app",
    )

    _assert_no_forbidden_runtime_imports("reset example import")
    print("[OK] reset text chat example is importable")


def check_live_text_turn(
    prompt: str,
    *,
    provider: str | None = None,
    model: str | None = None,
) -> None:
    from framework import create_text_chat_session

    session = create_text_chat_session(
        preset="text_chat",
        character_name="default",
        provider=provider,
        model=model,
    )
    response = session.ask(prompt)

    _assert(response.strip() != "", "LLM response was empty")
    print(f"[OK] facade returned one live text response: {session.info}")
    print(response)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run smoke checks for the public framework facade.",
    )
    parser.add_argument(
        "--ask",
        metavar="TEXT",
        help="Run an optional live LLM check with the provided prompt.",
    )
    parser.add_argument(
        "--provider",
        help="Optional provider override for the live LLM check.",
    )
    parser.add_argument(
        "--model",
        help="Optional model override for the live LLM check.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])

    check_import_boundary()
    check_text_only_config_boundary()
    check_provider_model_resolution()
    check_session_info_model()
    check_minimal_app_example_import()
    check_error_handling_example_import()
    check_streaming_example_import()
    check_reset_example_import()

    if args.ask:
        check_live_text_turn(
            args.ask,
            provider=args.provider,
            model=args.model,
        )
    else:
        print("[SKIP] live LLM check skipped; pass --ask to enable it")


if __name__ == "__main__":
    main()
