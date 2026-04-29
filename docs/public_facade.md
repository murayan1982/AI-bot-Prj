# Public Facade

The public facade is the stable entry point for using AI Character Framework as a library.

Current public API:

```python
from framework import create_text_chat_session

session = create_text_chat_session(
    preset="text_chat",
    character_name="default",
)

response = session.ask("こんにちは。短く返して。")
print(response)
```

## Scope

`create_text_chat_session()` is intentionally text-only.

It does not launch:

- `main.py`
- the runtime loop
- STT
- TTS
- VTube Studio / Live2D control

Use `main.py` for full runtime features such as voice input, voice output, and VTS integration.

## Supported presets

The text facade accepts text-only presets such as:

- `text_chat`
- other presets where voice input, voice output, VTS, and TTS are disabled

Presets such as `voice_vts` and `text_vts` are rejected by the facade because they require runtime systems outside the text-only public API.

## Smoke checks

Offline-safe check:

```powershell
python scripts/smoke_public_facade.py
```

Optional live LLM check:

```powershell
python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"
```

Minimal example:

```powershell
python examples/public_text_chat.py
```
