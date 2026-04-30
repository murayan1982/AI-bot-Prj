# Public Facade

The public facade is the stable entry point for using AI Character Framework as a library.

It is designed for application code that wants to call the framework directly without launching `main.py` or the full interactive runtime loop.

Current public API:

```python
from framework import create_text_chat_session

session = create_text_chat_session(
    preset="text_chat",
    character_name="default",
)

print(session.info)

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

Use `main.py` or the preset run scripts for full runtime features such as voice input, voice output, and VTS integration.

## Public API

### `create_text_chat_session()`

Creates a `TextChatSession` without starting the full runtime loop.

```python
from framework import create_text_chat_session

session = create_text_chat_session()
```

Optional preset and character arguments:

```python
session = create_text_chat_session(
    preset="text_chat",
    character_name="default",
)
```

`preset` must point to a text-only compatible preset.

As of v2.4.0, the facade also accepts direct provider/model selection:

```python
session = create_text_chat_session(
    provider="openai",
    model="gpt-4o-mini",
)
```

Arguments:

- `preset`: optional text-only preset name. When omitted, `APP_PRESET` is used if available; otherwise `text_chat` is used.
- `character_name`: optional character override. When omitted, the character configured by the selected preset is used.
- `provider`: optional direct LLM provider override. When omitted, the facade uses the default chat route with fallback.
- `model`: optional model override for the selected provider. Ignored when `provider` is omitted.

Supported public provider names include:

- `openai`
- `gemini`
- `grok`

`gemini` and `grok` are public aliases. Internally, provider definitions are still owned by `llm.factory` and `registry/llm.py`.

If `provider` is passed without `model`, the facade resolves the default model from `registry/llm.py`.


### `TextChatSession.info`

`TextChatSession.info` exposes stable, app-safe metadata about the created text
chat session.

```python
session = create_text_chat_session(provider="openai", model="gpt-4o-mini")

print(session.info.provider)
print(session.info.model)
print(session.info.output_language_code)
```

The info object is a `TextChatSessionInfo` instance.

Fields:

- `preset`: selected text-only preset name
- `character_name`: selected character name
- `input_language_code`: input language code
- `output_language_code`: output language code
- `llm_mode`: either `default_route` or `direct_provider`
- `provider`: resolved provider in direct provider mode, otherwise `None`
- `model`: resolved model in direct provider mode, otherwise `None`
- `route_name`: `chat` in default route mode, otherwise `None`
- `supports_streaming`: whether `ask_stream()` is part of this facade
- `supports_reset`: whether `reset()` is part of this facade
- `supports_voice`: always `False` for the text facade
- `supports_vts`: always `False` for the text facade

`TextChatSession.info` intentionally does not expose internal `RuntimeConfig`.

In default route mode, internal primary/fallback provider details are not exposed.
This keeps application code independent from the framework's internal routing and
fallback configuration.

In direct provider mode, `provider` and `model` expose the resolved provider/model
pair requested by application code.

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

For an app-oriented streaming example, run:

```powershell
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

The example prints chunks as they arrive and keeps the app code limited to public
`framework` imports.

### `TextChatSession.reset()`

Resets provider-owned conversation state when the underlying provider supports it.

```python
session.reset()
```

Stateless providers may treat this as a no-op.

## Public errors

The facade exposes public error classes so application code can catch framework integration errors at a clear boundary.

```python
from framework import FacadeError, create_text_chat_session

try:
    session = create_text_chat_session(provider="openai", model="gpt-4o-mini")
    print(session.ask("Hello."))
except FacadeError as e:
    print(f"Framework integration error: {e}")
```

Public info classes:

- `TextChatSessionInfo`: stable public session metadata for app integrations

Public error classes:

- `FacadeError`: base exception for public facade integration errors
- `FacadeConfigError`: raised when the selected preset or character is invalid for the text-only facade
- `FacadeProviderError`: raised when provider/model resolution or provider creation fails

### Streaming example

Use this example when you want to see the simplest app-style streaming loop:

```powershell
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini
```

It demonstrates this shape:

```python
from framework import FacadeError, create_text_chat_session

try:
    session = create_text_chat_session(provider="openai", model="gpt-4o-mini")
    for chunk in session.ask_stream("Hello. Please answer briefly."):
        print(chunk, end="", flush=True)
except FacadeError as e:
    print(f"Framework integration error: {e}")
```

### Reset example

Use this example when your app needs a user-facing "new conversation" or
"clear chat" action:

```powershell
python examples/app_reset_text_chat.py --provider openai --model gpt-4o-mini
```

It demonstrates this shape:

```python
from framework import FacadeError, create_text_chat_session

try:
    session = create_text_chat_session(provider="openai", model="gpt-4o-mini")
    print(session.ask("Hello. Please answer briefly."))
    session.reset()
    print(session.ask("Start a new short greeting."))
except FacadeError as e:
    print(f"Framework integration error: {e}")
```

`reset()` resets provider-owned conversation state when the underlying provider
supports it. App code should call it through the public `TextChatSession`, not
through internal provider or runtime objects.

### Error handling example

For an app-oriented example of catching public facade errors, run:

```powershell
python examples/app_error_handling.py
```

The default mode is offline-safe. It intentionally demonstrates:

- `FacadeConfigError` for a preset that is not compatible with the text facade
- `FacadeProviderError` for an unsupported direct provider name

You can also use the same example for an optional live turn after setting API keys:

```powershell
python examples/app_error_handling.py --live --provider openai --model gpt-4o-mini
```

External apps should normally catch `FacadeError` at the framework boundary, and
may catch `FacadeConfigError` or `FacadeProviderError` when they want more
specific user-facing messages.

## Supported presets

The text facade accepts text-only presets such as:

- `text_chat`
- `bilingual_ja_en`
- other presets where voice input, voice output, VTS, and TTS are disabled

Presets such as `voice_vts` and `text_vts` are rejected by the facade because they require runtime systems outside the text-only public API.

## App integration contract

For a more explicit boundary between external application code and framework internals, see:

- `docs/app_integration_contract.md`

The short version is:

- import from `framework`
- create sessions with `create_text_chat_session()`
- inspect public metadata through `session.info`
- send user text through `ask()` or `ask_stream()`
- catch `FacadeError` at the app boundary
- do not depend on `RuntimeConfig` or internal runtime objects

## Minimal app integration example

Use this example when you want to see how an external application might wrap the framework API:

```powershell
python examples/minimal_app_text_chat.py
```

With provider/model override:

```powershell
python examples/minimal_app_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

The example shows this shape:

```python
from framework import FacadeError, create_text_chat_session

class MinimalTextChatApp:
    def __init__(self):
        self._session = create_text_chat_session(provider="openai", model="gpt-4o-mini")

    @property
    def session_info(self):
        return self._session.info

    def reply(self, user_text: str) -> str:
        return self._session.ask(user_text)
```

This is intentionally different from `examples/public_text_chat.py`, which only demonstrates the smallest direct facade call.

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

Optional live LLM check using the default chat route:

```powershell
python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"
```

Optional live LLM check using direct provider mode:

```powershell
python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
```

Minimal direct facade example:

```powershell
python examples/public_text_chat.py
```

Minimal app-style integration example:

```powershell
python examples/minimal_app_text_chat.py
```

Offline error handling example:

```powershell
python examples/app_error_handling.py
```

Provider-selected app-style example:

```powershell
python examples/minimal_app_text_chat.py --provider openai --model gpt-4o-mini
```


## Future notes

### Voice-friendly output policy

A future version may add a framework-level output policy for TTS-enabled
sessions.

The goal is to make LLM responses easier for speech synthesis to read aloud.

This should be treated as output-quality guidance, not character personality.
It should avoid unnecessary symbols, dense Markdown, tables, and excessive
abbreviations while keeping code, commands, file paths, URLs, environment
variable names, and proper nouns unchanged when necessary.

The policy should be enabled only when audio/TTS output is active.

## v2.6.0 verification

Recommended checks before tagging v2.6.0:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/app_error_handling.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
```

Optional live checks after provider API keys are configured:

```powershell
python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
python examples/app_error_handling.py --live --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
python examples/app_reset_text_chat.py --provider openai --model gpt-4o-mini
```
