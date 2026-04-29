# Release Notes: v2.3.0

## Public Facade Foundation

v2.3.0 introduces the first public facade for using AI Character Framework as a lightweight Python library.

## Added

- Added `framework/` as the public facade package.
- Added `create_text_chat_session()` as the first public session factory.
- Added `TextChatSession` with:
  - `ask()` for one-turn text responses
  - `ask_stream()` for minimal chunk streaming
  - `reset()` for provider-owned conversation state reset
- Added `examples/public_text_chat.py` as the minimal facade usage example.
- Added `scripts/smoke_public_facade.py` for offline-safe public facade checks.
- Added `docs/public_facade.md` for public API documentation.
- Updated README with public text chat facade usage.

## Scope

The v2.3.0 facade is intentionally text-only.

It does not start:

- the full runtime loop
- STT
- TTS
- VTube Studio / Live2D control

Use `main.py` or the preset run scripts for full runtime behavior.

## Validation

The facade smoke check verifies that:

- `import framework` exposes the expected public API
- importing `framework` does not load runtime/audio/VTS modules
- `text_chat` is accepted by the facade boundary
- `voice_vts` is rejected by the facade boundary

Run:

```powershell
python scripts/smoke_public_facade.py
```

Optional live check:

```powershell
python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"
```
