# Release Checklist - v2.6.0

## Release theme

v2.6.0 focuses on app integration examples for the public text facade.

This release should make it easier for external app developers to understand how
to use error handling, streaming, reset, and session metadata without depending
on internal runtime modules.

## Scope check

Included:

- `examples/app_error_handling.py`
- `examples/app_streaming_text_chat.py`
- `examples/app_reset_text_chat.py`
- smoke import coverage for app integration examples
- README and `docs/public_facade.md` updates
- `docs/RELEASE_NOTES_v2.6.0.md`

Out of scope:

- voice input changes
- TTS output policy implementation
- Live2D / VTube Studio changes
- RuntimeConfig public exposure
- UI framework demo app implementation
- provider abstraction redesign

## Required checks

Run these before tagging:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/app_error_handling.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
```

Expected smoke coverage includes:

- public framework import boundary
- no runtime/audio/VTS import side effects
- text facade accepts `text_chat`
- text facade rejects `voice_vts`
- provider/model argument resolution without creating clients
- `TextChatSessionInfo` public metadata
- minimal app example import
- error handling example import
- streaming text chat example import
- reset text chat example import

## Optional live checks

Run after provider API keys are configured:

```powershell
python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
python examples/app_error_handling.py --live --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
python examples/app_reset_text_chat.py --provider openai --model gpt-4o-mini
```

## Public API boundary

Confirm the examples import from the public facade only:

```python
from framework import ...
```

The examples should not import from:

- `runtime`
- `core`
- `audio`
- `vts`
- provider implementation modules

## Repository hygiene

Check that generated files and local secrets are not accidentally tracked:

```powershell
git status
git diff --check
git ls-files | findstr /i "__pycache__ .pyc"
git ls-files | findstr /i ".env"
```

The `findstr` checks should not return tracked `__pycache__`, `.pyc`, or local
`.env` files.

## Distribution sanity check

Before creating a public distribution zip, confirm that the archive contains the
new examples and docs:

```text
examples/app_error_handling.py
examples/app_streaming_text_chat.py
examples/app_reset_text_chat.py
docs/RELEASE_NOTES_v2.6.0.md
docs/release_checklist_v2.6.0.md
```

Also confirm the archive does not include local-only files such as:

```text
.env
__pycache__/
*.pyc
```

## Tagging

After all checks pass and the working tree is clean:

```powershell
git status
git tag v2.6.0
git push origin FW_v2.6.0
git push origin v2.6.0
```

If releasing from `main`, merge the release branch first, then tag from the
release commit on `main`.
