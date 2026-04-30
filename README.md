# AI Character Conversation Framework

A developer-oriented framework for building real-time AI character experiences with text, voice, and Live2D support.

---

## What is this?

This project is an open-source framework for building AI character interaction systems.

It provides a modular foundation combining:

- Multi-LLM conversation (routing + fallback)
- Voice input/output (STT / TTS)
- Live2D (VTube Studio) integration
- Emotion-aware response handling
- Character-level expression mapping

The goal is to let developers focus on features, not infrastructure.

---

## Minimum Conversation UX

v2.0 focuses on making the current AI character conversation flow understandable and usable across text, Live2D, and voice presets.

The minimum supported conversation flow is:

```text
User input
-> LLM response
-> text display
-> optional TTS output
-> optional emotion parsing
-> optional VTS expression trigger
```

This means the framework is expected to provide a clear path from user input to character response, including text display, voice output, and Live2D expression control when those features are enabled.

The goal of v2.0 is not to provide a fully optimized real-time voice runtime yet.
The goal is to provide a clear, stable foundation for AI character conversation that can be extended in later versions.

---

## Conversation States

The framework uses simple user-facing conversation states to make the runtime behavior easier to understand.

```text
waiting   -> ready for text input or fallback input
listening -> waiting for voice input
thinking  -> generating an LLM response
speaking  -> playing TTS output
exiting   -> shutting down the session
```

In v2.0, these states are mainly treated as runtime feedback for developers and users.
A full internal conversation state machine is intentionally left for a future version.

---

## First Run

For the first run, start with:

```env
APP_PRESET=text_chat
```

`text_chat` is the safest starting point because it has the fewest dependencies and is the easiest way to confirm that the framework is working correctly.

Recommended order:

1. `text_chat` — confirm the basic text conversation flow
2. `text_vts` — confirm text input with Live2D / VTS integration without voice
3. `voice_vts` — try the full voice + Live2D experience

---


## Public Text Chat Facade

As of v2.4.0, the framework exposes a small public API for text-only chat usage and app-style integration.

This is intended for developers who want to use the project as a framework from their own Python code, without starting the full interactive runtime.

Minimal framework API example:

```python
from framework import create_text_chat_session

session = create_text_chat_session()
response = session.ask("Hello. Please answer briefly.")
print(response)
```

You can also pass a text-only preset and character explicitly:

```python
from framework import create_text_chat_session

session = create_text_chat_session(
    preset="text_chat",
    character_name="default",
)

print(session.ask("こんにちは。短く返して"))
```

v2.4.0 also supports direct provider/model selection from the facade:

```python
from framework import create_text_chat_session

session = create_text_chat_session(
    provider="openai",
    model="gpt-4o-mini",
)

print(session.ask("こんにちは。1文で短く返して。"))
```

As of v2.5.0, text chat sessions expose stable public metadata through `session.info`:

```python
session = create_text_chat_session(provider="openai", model="gpt-4o-mini")

print(session.info.preset)
print(session.info.character_name)
print(session.info.provider)
print(session.info.model)
print(session.info.output_language_code)
```

`session.info` is intended for external apps that need to inspect the created session without depending on internal runtime objects.
It intentionally does not expose `RuntimeConfig`.

Supported public provider names include:

- `openai`
- `gemini`
- `grok`

`gemini` and `grok` are public aliases. Internally, provider definitions are still owned by `llm.factory` and `registry/llm.py`.

If `provider` is omitted, the facade keeps the default chat route with fallback.
If `provider` is passed without `model`, the facade resolves the default model from `registry/llm.py`.

For app-style integration, catch public facade errors at the application boundary:

```python
from framework import FacadeError, create_text_chat_session

try:
    session = create_text_chat_session(provider="openai", model="gpt-4o-mini")
    print(session.ask("Hello."))
except FacadeError as e:
    print(f"Framework integration error: {e}")
```

For an offline-safe error handling example, run:

```powershell
python examples/app_error_handling.py
```

This intentionally demonstrates `FacadeConfigError` and `FacadeProviderError`
without calling an external LLM API.

For a simple streaming example, run after setting provider API keys:

```powershell
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

The streaming example uses `session.ask_stream(...)` and prints chunks as they arrive.

The public facade is intentionally text-only for now.

Supported:

- `text_chat`
- other text-only compatible presets such as `bilingual_ja_en`
- direct provider/model selection for text chat
- app boundary error handling through `FacadeError`

Not supported through this facade yet:

- voice input
- TTS output
- Live2D / VTube Studio control
- full runtime session loop

Use `main.py` or the preset run scripts when you want the full runtime experience.
Use `framework.create_text_chat_session()` when you want a lightweight framework API for text chat.
Use `examples/minimal_app_text_chat.py` when you want to see the smallest app-style wrapper around the framework API.

For app integration, the intended public contract is:

- import from `framework`
- create sessions with `create_text_chat_session()`
- inspect public metadata through `session.info`
- send user text through `ask()` or `ask_stream()`
- catch `FacadeError` at the app boundary
- avoid depending on `RuntimeConfig` or other internal runtime objects

Importing `framework` should not start the runtime, connect to VTube Studio, initialize STT/TTS, or make network calls.
Provider clients are created only when `create_text_chat_session()` is called. Importing `framework` remains side-effect-light.

For more details, see:

- `docs/public_facade.md`
- `docs/app_integration_contract.md`
- `examples/public_text_chat.py`
- `examples/minimal_app_text_chat.py`
- `examples/app_error_handling.py`
- `examples/app_streaming_text_chat.py`

---

## Presets

### `text_chat`

Safe default preset for first run.

- Keyboard input
- Text output
- No Live2D
- No voice input/output

Use this preset to confirm that the base framework is working.

---

### `text_vts`

Preset for checking text-driven Live2D / VTS behavior without voice features.

- Keyboard input
- Text output
- Live2D enabled
- No voice input/output
- Emotion / VTS expression control enabled

Use this preset when you want to test character expression control before enabling STT or TTS.

---

### `voice_vts`

Full voice + Live2D preset.

- Voice input (STT)
- Text fallback during STT wait
- Text display
- Voice output (TTS)
- Live2D enabled
- Emotion / VTS expression control enabled

This preset provides the richest experience, but it also has the most runtime dependencies.
After confirming that `text_chat` or `text_vts` works correctly, move on to `voice_vts`.

---

### `bilingual_ja_en`

Example preset for bilingual-style testing.

- Japanese input
- English output
- No Live2D
- No voice input/output

Use this preset when you want to test language separation, such as Japanese input with English-only responses.

---

## Preset Experience Matrix

| Preset | Input | Output | Live2D | Emotion / VTS expression | Main purpose |
| --- | --- | --- | --- | --- | --- |
| `text_chat` | Keyboard | Text | Disabled | Disabled | Safest first-run and base LLM conversation check |
| `text_vts` | Keyboard | Text | Enabled | Enabled | Check Live2D expression flow without voice input/output |
| `voice_vts` | STT + text fallback | Text + TTS | Enabled | Enabled | Minimum full-stack voice + Live2D conversation check |
| `bilingual_ja_en` | Keyboard Japanese | Text English | Disabled | Disabled | Check input/output language separation |

These presets are representative user-facing conversation presets, not a complete test matrix for every possible STT / TTS / Live2D combination.
For v2.0, the presets are intentionally kept small and easy to understand.
Lower-level combinations such as STT-only or TTS-only can be added later as developer test presets if needed.

---

## Voice Mode Notes

`voice_vts` is intended as an upper-level preset after basic confirmation.

In `voice_vts`:

- STT is used for voice input
- TTS is used for voice output
- if voice input is not detected, text fallback can be used
- type `exit` or `quit` in text fallback to end the session normally
- use `Ctrl+C` for forced termination

This keeps voice mode easier to exit and more practical during testing.

`voice_vts` should be treated as the minimum full-stack conversation preset in v2.0.
It is useful for confirming voice input, LLM response, TTS output, emotion parsing, and Live2D expression control together.

It is not intended to represent the final low-latency voice architecture.
As of v2.1, the voice pipeline has been clarified around runtime responsibilities:
`core/session.py` owns the top-level conversation loop, while `core/pipeline.py`
handles user input collection, AI response processing, streaming display,
optional TTS enqueue, and TTS playback wait.

Provider abstraction, conversation state, latency-oriented streaming voice,
and interruption behavior remain future runtime topics.

---

## Current Features

- Multi-LLM support (Gemini / Grok / OpenAI)
- Automatic routing (chat vs code)
- Fallback handling
- Voice input (STT) / output (TTS)
- Live2D (VTube Studio) optional integration
- Emotion tag generation and parsing
- Character-level VTS hotkey mapping
- Plugin-based VTS emotion handling
- Clean modular architecture
- Public text chat facade for framework-style usage
- Facade-level provider/model selection for app integration
- Public facade error classes for application boundary handling

Note: OpenAI support is available as of v2.2.0.
As of v2.4.0, text facade users can select providers directly with `create_text_chat_session(provider=..., model=...)`.
When `provider` is omitted, the default route still uses the existing Gemini / Grok configuration.

---

## Architecture

```text
main.py
  ↓
runtime (init)
  ↓
session (loop)
  ↓
pipeline
  ├── LLM (router + fallback)
  ├── TTS
  ├── Hooks
  └── Emotion parsing
         ↓
plugins
  └── EmotionVTSPlugin
         ↓
VTS hotkey trigger
```

Main emotion flow:

```text
User input
-> LLM raw response
-> parse_emotion_response()
-> emotion + clean_text
-> display clean_text
-> TTS clean_text
-> resolve_emotion_hotkey()
-> VTS trigger_hotkey()
```

---

## Extensibility

This framework includes lightweight extension points for runtime customization.

- **Hooks** are event-style extension points used inside the runtime flow
- **Plugins** are lifecycle-oriented extensions used for setup, startup, shutdown, and integration behavior

This keeps the core runtime small while making it easier to add logging, integrations, or custom runtime behavior.

---

## Project Structure

```text
core/
  runtime.py
  session.py
  pipeline.py
  emotion.py
  events.py

llm/
  base.py
  builder.py
  factory.py
  router_llm.py
  fallback_llm.py
  gemini_engine.py
  grok_engine.py
  openai_engine.py

live2d/
  vts_client.py

plugins/
  base.py
  manager.py
  builtin/
    console_logger.py
    emotion_vts.py
    response_length_logger.py
  samples/
    simple_greeting.py

config/
  loader.py
  secrets.py
  defaults.py
  legacy.py

registry/
  llm.py
  tts.py

framework/
  __init__.py
  facade.py

examples/
  public_text_chat.py

scripts/
  smoke_public_facade.py

docs/
  public_facade.md
  roadmap_v3.0.md

characters/
  default/
    profile.json
    system.txt
    vts_hotkeys.json

presets/
  text_chat.json
  text_vts.json
  voice_vts.json
  bilingual_ja_en.json

stt/
tts/

main.py
```

---

## Character Customization

Character-related files define who the character is.
Preset and runtime settings define how the application runs.

A character is managed as one directory under `characters/`.

```text
characters/
  default/
    profile.json
    system.txt
    vts_hotkeys.json
```

Each character directory can contain the same three files.

---

### Character files

- `profile.json`
  - Basic character metadata such as name and description
  - Useful for identifying the character
  - This is not the main behavior prompt

- `system.txt`
  - The main system prompt that defines how the character speaks and behaves
  - Edit this first when you want to change personality, tone, or response style

- `vts_hotkeys.json`
  - Emotion / Live2D hotkey mappings used for VTS expression control
  - Only needed when using VTube Studio expression control

---

### Editing guide

- If you want to change the character's identity:
  - edit `characters/<character_name>/profile.json`

- If you want to change the character's tone, style, or behavior:
  - edit `characters/<character_name>/system.txt`

- If you want to change facial-expression or emotion mappings:
  - edit `characters/<character_name>/vts_hotkeys.json`

- If you want to switch which character is used:
  - edit `character_name` in `presets/*.json`

- If you want to change input/output mode or runtime behavior:
  - edit `APP_PRESET` in `.env`
  - edit `presets/*.json`

---

### Adding a new character

The simplest way to add a new character is to copy the default character directory.

1. Copy `characters/default/`
2. Rename the copied directory, for example `characters/my_character/`
3. Edit `profile.json`
4. Edit `system.txt`
5. Edit `vts_hotkeys.json` if you use VTube Studio expression control
6. Set `character_name` in `presets/*.json` to the new directory name

Example:

```text
characters/
  default/
    profile.json
    system.txt
    vts_hotkeys.json
  my_character/
    profile.json
    system.txt
    vts_hotkeys.json
```

Then update a preset:

```json
{
  "character_name": "my_character"
}
```

The directory name under `characters/` and the `character_name` value in the preset should match.

---

### Preset vs Character

A simple rule:

- Character = who the assistant is
- Preset / Runtime = how the system runs

Examples:

- Change speaking style -> character (`system.txt`)
- Change displayed name / description -> character (`profile.json`)
- Change emotion-to-VTS mapping -> character (`vts_hotkeys.json`)
- Change selected character -> preset (`character_name`)
- Change text/voice mode -> preset (`presets/*.json`)

---

## Setup

### 1. Clone

```bash
git clone https://github.com/murayan1982/ai-character-framework.git
cd ai-character-framework
```

---

### 2. Install

```bash
pip install -r requirements.txt
```

---

### 3. Environment Variables

Create `.env` from `.env.example`.

Windows:

```bash
copy .env.example .env
```

Mac / Linux:

```bash
cp .env.example .env
```

Then open `.env` and add your API keys.

Required for the default LLM route:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Optional LLM providers:

```env
XAI_API_KEY=your_xai_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Optional voice configuration:

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
VOICE_MASTER=[{"id":"your_voice_id_here","name":"MyVoice"}]
```

Notes:

- `GEMINI_API_KEY` is required for the current default route.
- `XAI_API_KEY` is used when Grok is enabled as a provider or fallback.
- `OPENAI_API_KEY` is used when OpenAI is selected as a provider.
- OpenAI support is available in v2.2.0, but OpenAI is not the default provider yet.
- Do not commit your `.env` file.

---

## Developer Flow

For regular development, start from the smallest working setup and then add features step by step.

Recommended flow:

1. Start with `APP_PRESET=text_chat`
2. Confirm the basic text conversation flow
3. Customize the character under `characters/*`
4. Switch to `text_vts` for Live2D expression checks, then `voice_vts` for voice + Live2D checks
5. Edit registry files only when you want to change LLM or TTS definitions

Use these files as the main entry points:

- `.env`
  - Selects the startup preset with `APP_PRESET`

- `presets/*.json`
  - Defines runtime mode such as text, voice, Live2D, language, and selected character

- `characters/*`
  - Defines character-specific identity, behavior, and VTS expression mapping

- `registry/llm.py`
  - Defines available LLM providers and routes

- `registry/tts.py`
  - Defines available TTS providers and models

- `framework/`
  - Provides the public facade for framework-style usage

- `examples/public_text_chat.py`
  - Shows the minimum public facade usage

- `examples/minimal_app_text_chat.py`
  - Shows a minimal app-style wrapper around the public text facade

A simple rule:

- Change who the assistant is -> edit `characters/*`
- Change how the framework runs -> edit `.env` or `presets/*.json`
- Change provider definitions -> edit `registry/*`

### LLM registry validation

v2.2.0 adds lightweight validation for LLM provider registry definitions.

You can check the LLM catalog and route definitions without creating provider clients or making network calls:

```bash
python -c "from llm.builder import validate_llm_registry; validate_llm_registry(); print('LLM registry OK')"
```

This validation checks provider names, model definitions, and route references.

It does not validate API keys.
Provider API keys are checked only when the corresponding provider is instantiated at runtime.

### Public facade smoke check

The public facade can be checked without running a live LLM request:

```bash
python scripts/smoke_public_facade.py
```

This checks that:

- `import framework` exposes the expected public API
- importing `framework` does not load runtime/audio/VTS modules
- `text_chat` is accepted by the text facade boundary
- `voice_vts` is rejected by the text facade boundary

To run a live one-turn LLM check through the facade, pass `--ask`:

```bash
python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"
```

---

## Runtime Configuration

Runtime behavior is controlled mainly by:

- `APP_PRESET`
- `presets/*.json`
- character files under `characters/*`

Character files and runtime settings have different responsibilities.

- `characters/*` defines who the character is
- `APP_PRESET` and `presets/*.json` define how the framework runs
- `RuntimeConfig` is assembled from both and becomes the runtime source of truth

Example:

```env
APP_PRESET=text_chat
```

The framework loads the selected preset and builds a `RuntimeConfig` object at startup.

---

### RuntimeConfig controls things like

- input language
- output language
- STT on/off
- TTS on/off
- VTS on/off
- emotion on/off
- VTS emotion on/off
- selected character
- selected character hotkey mapping

---

### Configuration Flow

Runtime behavior is configured in the following order:

1. `.env` selects the startup preset through `APP_PRESET`
2. `presets/*.json` defines the runtime mode
3. `characters/*` provides character-specific differences
4. `config/loader.py` assembles `RuntimeConfig`
5. Runtime behavior should read from `RuntimeConfig` as the source of truth

---

### What to edit for common changes

- Change startup mode:
  - `APP_PRESET` in `.env`
  - `presets/*.json`

- Change character-specific behavior:
  - `characters/<name>/profile.json`
  - `characters/<name>/system.txt`
  - `characters/<name>/vts_hotkeys.json`

- Change LLM definitions or route setup:
  - `registry/llm.py`

- Change TTS model definitions:
  - `registry/tts.py`

- Change developer-side defaults:
  - `config/defaults.py`

- Change API keys / secret values:
  - `.env`
  - `config/secrets.py`

- Review older compatibility paths:
  - `config/legacy.py`

---

### Recommended development starting point

Use `text_chat` as the safe default preset for regular development.

---

## v2.2 Provider Boundary Notes

v2.2.0 focuses on provider boundary cleanup.

The main focus is LLM provider extensibility:

- Gemini, Grok, and OpenAI are handled through the same `BaseLLM` interface
- LLM provider definitions are managed in `registry/llm.py`
- LLM provider construction is handled by `llm/factory.py`
- LLM route construction and validation are handled by `llm/builder.py`
- OpenAI provider support is available, but OpenAI is not the default provider in v2.2.0

The current default route remains Gemini / Grok based.

OpenAI can be used by adding `OPENAI_API_KEY` to `.env`.
For full runtime routing, select or edit the OpenAI catalog entry from `registry/llm.py`.
For public text facade usage, pass `provider="openai"` and an optional `model` to `create_text_chat_session()`.

STT and TTS provider abstraction are intentionally not redesigned in v2.2.0.

For now:

- STT runtime use is centered around `STTEngine.listen()`
- TTS runtime use is centered around `VoiceEngine.speak()`, `flush()`, `is_speaking_active`, and `stop_immediately()`
- full STT / TTS provider abstraction is left for a future milestone

---

## v2.6 App Integration Examples Notes

v2.6.0 focuses on small, copy-friendly examples for external app integration.

The first example is `examples/app_error_handling.py`, which shows how apps can
catch public facade errors without depending on internal runtime modules.

The second example is `examples/app_streaming_text_chat.py`, which shows how apps can
stream response chunks through `session.ask_stream(...)`.

The third example is `examples/app_reset_text_chat.py`, which shows how apps can
call `session.reset()` through a small app wrapper.

Offline-safe check:

```powershell
python examples/app_error_handling.py
```

Optional live check:

```powershell
python examples/app_error_handling.py --live --provider openai --model gpt-4o-mini
```

Streaming live check:

```powershell
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

Reset live check:

```powershell
python examples/app_reset_text_chat.py --provider openai --model gpt-4o-mini
```

Release checklist:

```text
docs/release_checklist_v2.6.0.md
```

---

## v2.5 App Integration Readiness Notes

v2.5.0 focuses on making the public text facade easier to inspect from external applications.

The main focus is public session metadata:

- `TextChatSession.info` exposes stable app-safe metadata
- `TextChatSessionInfo` is the public info model for text chat sessions
- default route mode hides internal provider/fallback details
- direct provider mode exposes the resolved provider/model pair
- external apps can inspect session capability flags such as `supports_streaming`, `supports_reset`, `supports_voice`, and `supports_vts`
- `RuntimeConfig` remains internal and should not be used as an app integration contract

Example:

```python
from framework import create_text_chat_session

session = create_text_chat_session(provider="openai", model="gpt-4o-mini")

print(session.info)
print(session.ask("Hello. Please answer briefly."))
```

Recommended integration docs:

- `docs/public_facade.md`
- `docs/app_integration_contract.md`
- `examples/minimal_app_text_chat.py`

Voice, TTS, Live2D / VTube Studio control, and the full runtime loop are still outside the public text facade scope.

---

## v2.4 Public Facade Integration Notes

v2.4.0 focuses on making the public text facade easier to embed in external applications.

The main focus is integration stability:

- `create_text_chat_session()` accepts optional `provider` and `model` arguments
- provider aliases such as `gemini` and `grok` are accepted at the public facade boundary
- the default no-argument behavior remains backward compatible
- facade-specific errors are exposed through `FacadeError`, `FacadeConfigError`, and `FacadeProviderError`
- `examples/minimal_app_text_chat.py` shows a tiny application wrapper around the framework API

Example:

```python
from framework import FacadeError, create_text_chat_session

try:
    session = create_text_chat_session(provider="openai", model="gpt-4o-mini")
    print(session.ask("Hello. Please answer briefly."))
except FacadeError as e:
    print(f"Framework integration error: {e}")
```

This facade is still intentionally text-only.
Voice, TTS, Live2D / VTube Studio control, and the full runtime loop should still be launched through `main.py` or the preset run scripts.

---

## v2.0 Scope and Future Work

v2.0 is the milestone for minimum AI character conversation UX.

In scope for v2.0:

- text / Live2D / voice preset experience review
- user input -> LLM response -> display / TTS / emotion / VTS flow review
- basic runtime feedback such as waiting, listening, thinking, speaking, and exiting
- preset purpose clarification
- character prompt / emotion / VTS expression consistency
- README and documentation alignment

Intentionally out of scope for v2.0:

- full STT / TTS provider abstraction
- full latency optimization
- interruption / barge-in
- multi-character conversation
- large audio pipeline redesign
- Web UI or settings screen

These topics are intentionally left for later versions after the minimum conversation experience is stable and easy to explain.
Advanced voice runtime topics are tracked in `docs/roadmap_v3.0.md`.

For v2.0, `voice_vts` should be understood as a minimum full-stack confirmation preset, not as a final low-latency voice architecture.

---

## Repository Naming

Repository name:

`ai-character-framework`

Project / README title:

`AI Character Conversation Framework`

This keeps the repository name short and practical while making the full project purpose clearer in the documentation.

---

## License

Please see `LICENSE.txt` for the full license terms.

This project is intended to be shared and used as a framework, but redistribution, reuse, or resale of the framework itself should follow the license terms carefully.

---

[Next Roadmap]

After v2.0, advanced conversation runtime topics are tracked in:

- `docs/roadmap_v3.0.md`