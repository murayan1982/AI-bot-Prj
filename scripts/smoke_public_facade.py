"""Smoke checks for the public framework facade.

Default mode is offline-safe and does not call an LLM provider API:

    python scripts/smoke_public_facade.py

Optional live LLM check, requiring API keys in .env:

    python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"
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



def check_minimal_app_example_import() -> None:
    # The app integration example should be importable without creating an LLM
    # client or loading the full runtime/audio/VTS stack.
    import importlib.util

    example_path = PROJECT_ROOT / "examples" / "minimal_app_text_chat.py"
    spec = importlib.util.spec_from_file_location(
        "minimal_app_text_chat_smoke",
        example_path,
    )
    _assert(spec is not None and spec.loader is not None, "Could not load example spec")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    _assert(
        hasattr(module, "MinimalTextChatApp"),
        "minimal app example should expose MinimalTextChatApp",
    )
    _assert(
        hasattr(module, "build_app"),
        "minimal app example should expose build_app",
    )

    imported_forbidden_modules = [
        module_name
        for module_name in FORBIDDEN_IMPORTS_AFTER_FRAMEWORK_IMPORT
        if module_name in sys.modules
    ]
    _assert(
        not imported_forbidden_modules,
        "minimal app example import should not load runtime/audio/VTS modules: "
        f"{imported_forbidden_modules}",
    )

    print("[OK] minimal app integration example is importable")

def check_live_text_turn(prompt: str) -> None:
    from framework import create_text_chat_session

    session = create_text_chat_session(
        preset="text_chat",
        character_name="default",
    )
    response = session.ask(prompt)

    _assert(response.strip() != "", "LLM response was empty")
    print("[OK] facade returned one live text response")
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
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])

    check_import_boundary()
    check_text_only_config_boundary()
    check_provider_model_resolution()
    check_minimal_app_example_import()

    if args.ask:
        check_live_text_turn(args.ask)
    else:
        print("[SKIP] live LLM check skipped; pass --ask to enable it")


if __name__ == "__main__":
    main()
