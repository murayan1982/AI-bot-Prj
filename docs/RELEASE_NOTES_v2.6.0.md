# Release Notes - v2.6.0

## App Integration Examples

v2.6.0 focuses on small examples that make the public text facade easier to use
from external applications.

## Added

- Added `examples/app_error_handling.py`.
- Added `examples/app_streaming_text_chat.py`.
- Added offline-safe examples for catching:
  - `FacadeConfigError`
  - `FacadeProviderError`
- Added optional live mode to the error handling example:
  - `python examples/app_error_handling.py --live --provider openai --model gpt-4o-mini`
- Added smoke import coverage for the new error handling example.
- Added smoke import coverage for the new streaming example.

## Changed

- Updated `docs/public_facade.md` with app-level error handling and streaming examples.
- Updated README with the new error handling and streaming examples.
- Kept the example boundary focused on public `framework` imports.

## Design notes

`examples/app_error_handling.py` is intentionally offline-safe by default.

The default run demonstrates facade errors without creating provider clients or
calling external LLM APIs. This makes the error boundary easy to test even before
API keys are configured.

External apps may catch `FacadeError` as the generic framework integration
boundary, or catch `FacadeConfigError` / `FacadeProviderError` when more specific
user-facing messages are useful.

`examples/app_streaming_text_chat.py` demonstrates the minimal streaming shape
for application code that wants to render chunks as they arrive. It uses
`session.ask_stream(...)` and keeps provider-specific metadata hidden behind the
public text facade.

## Verification

Recommended checks:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/app_error_handling.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
```

Optional live checks:

```powershell
python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
python examples/app_error_handling.py --live --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
python examples/app_streaming_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```
