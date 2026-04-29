# Release Notes Draft: v2.4.0 Integration Stability

## Summary

v2.4.0 improves the public text chat facade so it is easier to embed the framework from external Python applications.

This release keeps the existing ready-to-run behavior intact while making the framework API boundary more stable for app integration.

## Highlights

- Added provider/model selection to the public text chat facade.
- Added public facade error classes for app-side error handling.
- Added a minimal app-style integration example.
- Updated public facade documentation and README usage examples.
- Preserved the existing `create_text_chat_session()` default behavior.
- Kept the v2.4.0 scope limited to text chat facade integration stability.

## Added

### Provider/model selection from the facade

`create_text_chat_session()` now accepts optional provider and model arguments.

```python
from framework import create_text_chat_session

session = create_text_chat_session(
    provider="openai",
    model="gpt-4o-mini",
)

print(session.ask("Hello!"))
```

When no provider is specified, the previous chat route/fallback behavior is preserved.

```python
from framework import create_text_chat_session

session = create_text_chat_session()
print(session.ask("Hello!"))
```

### Facade error boundary

The public facade now exposes dedicated error classes for external app integration.

```python
from framework import FacadeError, create_text_chat_session

try:
    session = create_text_chat_session(provider="openai")
    print(session.ask("Hello!"))
except FacadeError as exc:
    print(f"Framework integration error: {exc}")
```

Public facade error classes:

- `FacadeError`
- `FacadeConfigError`
- `FacadeProviderError`

### Minimal app integration example

Added:

```text
examples/minimal_app_text_chat.py
```

This example shows an app-style wrapper around the public facade rather than an interactive CLI-first runtime flow.

Example:

```powershell
python examples/minimal_app_text_chat.py
python examples/minimal_app_text_chat.py --provider openai --model gpt-4o-mini --message "Hello!"
```

## Changed

- Updated `README.md` to clarify the difference between ready-to-run usage and framework API usage.
- Updated `docs/public_facade.md` with provider selection, facade error handling, and minimal app integration notes.
- Updated `scripts/smoke_public_facade.py` to verify the public facade import boundary and minimal app example importability.

## Compatibility

The following existing usage remains valid:

```python
from framework import create_text_chat_session

session = create_text_chat_session()
print(session.ask("Hello!"))
```

The existing ready-to-run entry points remain unchanged:

```powershell
python main.py
run.bat
scripts/run_text_chat.bat
scripts/run_text_vts.bat
scripts/run_voice_vts.bat
```

## Out of scope for v2.4.0

The following are intentionally not included in this release:

- voice facade
- VTS facade
- TTS facade
- async streaming redesign
- multi-session manager
- web server / API server
- demo app implementation
- plugin API redesign

## Verification

Recommended checks before release:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
python examples/minimal_app_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

Optional live smoke check:

```powershell
python scripts/smoke_public_facade.py --ask "こんにちは。短く返して"
```

## Suggested commit summary

```text
v2.4.0 stabilizes the public text chat facade for external app integration.
It adds provider/model selection, public facade error classes, a minimal app-style example, and updated documentation while keeping the existing ready-to-run flow unchanged.
```
