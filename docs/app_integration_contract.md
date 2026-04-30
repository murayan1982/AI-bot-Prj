# App Integration Contract

This document describes the intended boundary between external application code and AI Character Framework.

The goal is to let apps use the framework as a library without depending on internal runtime details.

## Recommended import boundary

Application code should import from `framework`:

```python
from framework import FacadeError, create_text_chat_session
```

Avoid importing directly from internal packages such as `core`, `runtime`, `llm`, `tts`, `stt`, or `live2d` for app-facing text chat integrations.

## Session creation

Create a text chat session explicitly:

```python
session = create_text_chat_session()
```

For direct provider mode:

```python
session = create_text_chat_session(
    provider="openai",
    model="gpt-4o-mini",
)
```

If `provider` is omitted, the facade uses the default chat route with fallback.
If `provider` is provided, the facade uses direct provider mode.

## Public session metadata

Use `session.info` to inspect app-safe metadata:

```python
info = session.info

print(info.preset)
print(info.character_name)
print(info.llm_mode)
print(info.provider)
print(info.model)
print(info.output_language_code)
```

`session.info` is a `TextChatSessionInfo` instance.
It intentionally does not expose `RuntimeConfig`.

Apps may rely on these fields as the public text facade metadata contract:

- `preset`
- `character_name`
- `input_language_code`
- `output_language_code`
- `llm_mode`
- `provider`
- `model`
- `route_name`
- `supports_streaming`
- `supports_reset`
- `supports_voice`
- `supports_vts`

In default route mode:

```python
info.llm_mode == "default_route"
info.provider is None
info.model is None
info.route_name == "chat"
```

In direct provider mode:

```python
info.llm_mode == "direct_provider"
info.provider == "openai"
info.model == "gpt-4o-mini"
info.route_name is None
```

## Sending user input

Use `ask()` for one-turn full responses:

```python
response = session.ask("Hello. Please answer briefly.")
print(response)
```

Use `ask_stream()` when the application wants incremental chunks:

```python
for chunk in session.ask_stream("Hello. Please answer briefly."):
    print(chunk, end="")
```

Use `reset()` when the application wants to reset provider-owned conversation state:

```python
session.reset()
```

Stateless providers may treat reset as a no-op.

## Error boundary

Catch public facade errors at the app boundary:

```python
try:
    session = create_text_chat_session(provider="openai", model="gpt-4o-mini")
    response = session.ask("Hello.")
except FacadeError as exc:
    print(f"Framework integration error: {exc}")
```

Public facade errors are:

- `FacadeError`
- `FacadeConfigError`
- `FacadeProviderError`

## What apps should not depend on

External apps should not depend on:

- `RuntimeConfig` shape
- internal route/fallback provider details
- provider implementation classes
- runtime session loop internals
- STT/TTS/VTS internals through the text facade

Those details may change across framework versions.

## Text facade scope

The current public facade is text-only.

Supported:

- text input
- text output
- optional direct provider/model selection
- public session metadata
- public facade error classes

Not supported through this facade yet:

- voice input
- TTS output
- Live2D / VTube Studio control
- full interactive runtime loop

Use `main.py` or the preset run scripts for full runtime behavior.

## Future note - Voice-friendly output policy

A future version may add a framework-level output policy for TTS-enabled sessions.

The goal would be to make LLM responses easier for speech synthesis to read aloud.
This should be treated as output-quality guidance, not character personality.

The policy should avoid unnecessary symbols, dense Markdown, tables, and excessive abbreviations while preserving code, commands, file paths, URLs, environment variable names, and proper nouns when necessary.

This should be enabled only when audio/TTS output is active.
