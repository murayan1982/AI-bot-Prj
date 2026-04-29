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

## Public API

### `create_text_chat_session()`

Creates a `TextChatSession` without starting the full runtime loop.

```python
from framework import create_text_chat_session

session = create_text_chat_session()
```

Optional arguments:

```python
session = create_text_chat_session(
    preset="text_chat",
    character_name="default",
)
```

`preset` must point to a text-only compatible preset.

### `TextChatSession.ask(text)`

Sends one text turn and returns the full assistant response as a string.

```python
response = session.ask("Hello. Please answer briefly.")
print(response)
```

### `TextChatSession.ask_stream(text)`

Sends one text turn and yields response chunks.

```python
for chunk in session.ask_stream("Hello. Please answer briefly."):
    print(chunk, end="")
```

This is a minimal streaming facade. Provider-specific emotion metadata is intentionally hidden from the public text API for now.

### `TextChatSession.reset()`

Resets provider-owned conversation state when the underlying provider supports it.

```python
session.reset()
```

Stateless providers may treat this as a no-op.

## Supported presets

The text facade accepts text-only presets such as:

- `text_chat`
- `bilingual_ja_en`
- other presets where voice input, voice output, VTS, and TTS are disabled

Presets such as `voice_vts` and `text_vts` are rejected by the facade because they require runtime systems outside the text-only public API.

## Import boundary

Importing `framework` should not:

- start the runtime loop
- connect to VTube Studio
- initialize STT/TTS
- create provider clients
- make network calls

Provider clients are created only when `create_text_chat_session()` is called.

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
