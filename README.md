# AI Conversation Framework

A modular AI conversation framework for building AI character experiences with:

* Multi-LLM routing (Chat / Code)
* Preset-based runtime configuration
* Character-based system prompts
* Input / output language separation
* Voice input/output support (STT / TTS)
* Live2D / VTube Studio connection support
* Extensible plugin architecture

---

## Prerequisites

Before starting, ensure you have:

* Python 3.10+
* pip

Optional:

* ffmpeg
* Microphone (for STT)
* Speakers (for TTS)
* VTube Studio (for Live2D / VTS integration)

You also need at least one API key:

* OpenAI
* Google (Gemini)
* xAI (Grok)

---

## Quick Start

1. Clone this repository

```bash
git clone https://github.com/murayan1982/AI-bot-Prj
cd AI-bot-Prj
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env`

```bash
cp .env.example .env
```

4. Edit `.env`

Example:

```env
LLM_PROVIDER=google
GOOGLE_API_KEY=your_api_key_here
```

5. Run the default app

```bash
python main.py
```

Example:

```txt
User: hello
AI: Hi there! How can I help you today?
```

---

## Run Scripts

You can also start the framework with preset-specific batch files.

```bat
scripts/run_text_chat.bat
scripts/run_text_vts.bat
scripts/run_voice_vts.bat
```

These scripts set `APP_PRESET` and then run `main.py`.

---

## Presets

Presets define the runtime mode.

Examples:

* `default`
* `text_chat`
* `text_vts`
* `voice_vts`
* `bilingual_ja_en`

Preset files are located in:

```txt
presets/
```

A preset can configure:

* input language
* output language
* input voice on/off
* output voice on/off
* VTS on/off
* TTS provider
* character name

Example:

```json
{
  "input_language_code": "ja",
  "output_language_code": "en",
  "input_voice_enabled": false,
  "output_voice_enabled": false,
  "vts_enabled": false,
  "tts_provider": "none",
  "character_name": "default"
}
```

---

## Characters

Characters define profile data and system prompts.

Character files are located in:

```txt
characters/
```

Example:

```txt
characters/default/
  profile.json
  system.txt
```

`profile.json` defines character metadata.

`system.txt` defines the character's system prompt.

---

## Language Settings

The framework supports separate input and output languages.

Example:

```json
{
  "input_language_code": "ja",
  "output_language_code": "en"
}
```

This allows configurations such as:

```txt
User input: Japanese
AI output: English
```

The runtime adds an output-language instruction to the final system prompt.

---

## Plugin System

The framework includes a minimal plugin system.

Plugin files are located in:

```txt
plugins/
```

Current built-in plugin:

```txt
plugins/builtin/console_logger.py
```

The plugin manager is initialized during runtime startup.

Example runtime log:

```txt
[Plugin:console_logger] setup complete
[Plugin:console_logger] runtime started
```

---

## Live2D / VTube Studio Support (Connection Support Only in v1.4)

For example:

```txt
text_vts
voice_vts
```

When VTube Studio is running and its API is enabled, the runtime can connect and show:

```txt
Live2D: Enabled
```

If VTube Studio is not running or the API connection fails, the app continues running without Live2D:

```txt
Live2D: Disabled
```

The framework attempts to connect during startup.
If the connection fails, Live2D is disabled for that session and the app continues normally.

### Note

v1.4 supports VTS connection and preset-based enable/disable behavior.

Emotion tags and automatic expression control are not included in v1.4.
They are planned for v1.5.

---

## Voice Setup Notes

To use STT/TTS features:

* Install ffmpeg

Windows:

```bash
choco install ffmpeg
```

Mac:

```bash
brew install ffmpeg
```

Also ensure your microphone and speakers are properly recognized by your OS.

Some audio libraries may require additional system-level setup.

---

## Routing Logic

The framework automatically switches between Chat and Code modes.

How it works:

* Keyword-based detection
* If input matches strong code-related keywords, Code mode is used
* Otherwise, Chat mode is used

Example:

```txt
"write python code" -> Code
"how are you" -> Chat
```

---

## Configuration Priority

Runtime configuration is loaded using the following priority:

APP_PRESET is loaded from `.env` or the environment.
Runtime values are then loaded from preset and character files.

Currently, environment variables are mainly used to select the active preset.
Preset and character files define the runtime behavior.

---

## Features

* Multi-LLM support
* Chat / Code routing
* RuntimeConfig-based configuration
* Preset-based startup modes
* Character-based system prompts
* Input/output language separation
* STT / TTS support
* VTube Studio connection support
* Minimal plugin system

---

## Commercial Usage

You are allowed to:

* Sell applications built using this framework
* Create AI characters for streaming
* Provide paid AI services or SaaS
* Distribute applications that include this framework as part of a larger system
* Sell or distribute plugins, extensions, characters, presets, or add-ons that work with this framework, as long as they do not redistribute the framework itself

You are NOT allowed to:

* Resell this framework itself
* Redistribute source code as a standalone product
* Repackage and sell with minor modifications
* Publish this framework as a competing framework or template
* Redistribute this framework as a base project for other developers

If you distribute a product that includes this framework,
you must follow the redistribution requirements in `LICENSE.txt`
and provide proper attribution to the original author.

---

## Attribution

When using this framework in a product or service,
you must include attribution to the original author.

Example:

```txt
Powered by AI Conversation Framework by murayan
```

This can be placed in:

* Application credits
* Website footer
* Video descriptions

---

## Notes

* Model names may change over time
* Please refer to each provider’s official documentation
* Emotion tag and automatic Live2D expression control are planned for v1.5
* Roadmap items are planned features and may change depending on development priorities.

---

## License

This project is licensed under a custom commercial license.

See `LICENSE.txt` for details.
