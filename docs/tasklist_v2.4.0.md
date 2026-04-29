# v2.4.0 Integration Stability Task List

## Goal

Move the public text-chat facade from "minimum usable API" to "stable enough to integrate from an external app."

v2.4.0 focuses on text chat integration stability only. Voice, TTS, VTS, web server/API server, and demo app implementation stay out of scope.

## Scope decisions

### 1. Provider selection is in scope

`create_text_chat_session()` should support explicit provider/model selection without breaking the existing default behavior.

Target shape:

```python
session = create_text_chat_session(
    provider="openai",
    model="gpt-4o-mini",
)
```

Default behavior remains unchanged:

```python
session = create_text_chat_session()
```

When no provider is specified, the facade continues to use the existing chat route / fallback behavior.

Design rule:

- `provider=None` means use framework default chat route
- `provider="openai" | "google" | "xai"` means build a single explicit provider client
- `model=None` with explicit provider may use the registry default for that provider if we define one clearly
- unsupported provider should raise a facade-level provider error

### 2. Facade-specific errors are in scope

The public facade should expose stable exceptions so external apps can catch framework-facing errors without depending on internal `ValueError`, `FileNotFoundError`, or provider implementation details.

Proposed error hierarchy:

```python
class FacadeError(Exception):
    """Base error for public facade failures."""

class FacadeConfigError(FacadeError):
    """Raised when facade configuration or preset selection is invalid."""

class FacadeProviderError(FacadeError):
    """Raised when provider/model selection or provider creation fails."""
```

Design rule:

- invalid text facade preset -> `FacadeConfigError`
- missing preset -> `FacadeConfigError`
- unsupported provider -> `FacadeProviderError`
- unknown model/catalog entry -> `FacadeProviderError`
- missing API key may remain provider-owned internally, but should be wrapped or documented as facade provider failure where practical

### 3. Minimal app integration example is in scope

Add an example that looks like "an app calling the framework," not like the framework's interactive CLI.

Candidate file:

```text
examples/minimal_app_text_chat.py
```

Expected style:

```python
from framework import create_text_chat_session

class MinimalChatApp:
    def __init__(self):
        self.session = create_text_chat_session(provider="openai")

    def reply(self, user_text: str) -> str:
        return self.session.ask(user_text)
```

This should become the reference shape for the future demo app repo.

### 4. Public session config exposure is in scope, but limited

Expose only integration-safe metadata. Do not expose the full internal `RuntimeConfig` object.

Possible shape:

```python
session.info
```

or:

```python
session.get_info()
```

Candidate fields:

- `preset`
- `character_name`
- `input_language_code`
- `output_language_code`
- `provider`
- `model`
- `uses_fallback_route`

Design rule:

- public metadata should be immutable or read-only
- avoid leaking internal runtime config shape
- avoid making external apps depend on private config internals

## Out of scope for v2.4.0

- voice facade
- VTS facade
- TTS facade
- async streaming redesign
- multi-session manager
- web server / API server
- demo app implementation
- plugin API redesign
- major registry redesign

## Day plan

### Day1: Task list and design lock

- [x] Create v2.4.0 task list
- [x] Confirm provider selection is in scope
- [x] Confirm facade-specific error types are in scope
- [x] Keep v2.4.0 limited to text-chat facade integration stability
- [ ] Commit task list

Suggested commit:

```bash
git add docs/tasklist_v2.4.0.md
git commit -m "docs: add v2.4.0 integration stability task list"
```

### Day2: Public API argument design

- [ ] Update `create_text_chat_session()` signature without breaking existing calls
- [ ] Add `provider` argument
- [ ] Add optional `model` argument
- [ ] Decide default model resolution per provider
- [ ] Keep existing route/fallback path when provider is omitted
- [ ] Add/adjust smoke checks for default path compatibility

### Day3: Facade error boundary

- [ ] Add facade error classes
- [ ] Export public error classes from `framework/__init__.py`
- [ ] Convert text-only preset rejection to `FacadeConfigError`
- [ ] Convert missing preset to `FacadeConfigError`
- [ ] Convert unsupported provider to `FacadeProviderError`
- [ ] Update smoke checks for error types

### Day4: Minimal app integration example

- [ ] Add `examples/minimal_app_text_chat.py`
- [ ] Keep it small and app-like
- [ ] Avoid requiring voice/TTS/VTS
- [ ] Add optional provider usage example
- [ ] Update smoke check if useful

### Day5: Public docs / README update

- [ ] Update `docs/public_facade.md`
- [ ] Add provider selection section
- [ ] Add facade error handling section
- [ ] Add minimal app integration section
- [ ] Update README public facade section
- [ ] Clearly separate `main.py` ready-to-run usage from framework API usage

### Day6: Full check and release notes draft

- [ ] Run compile check
- [ ] Run public facade smoke check
- [ ] Run public example
- [ ] Run minimal app example
- [ ] Draft v2.4.0 release notes

Suggested checks:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
```

### Day7: Release readiness

- [ ] Final README/docs consistency check
- [ ] Confirm no voice/VTS facade scope creep
- [ ] Confirm existing `main.py` behavior remains intact
- [ ] Confirm public API imports are intentional
- [ ] Tag v2.4.0

## Proposed public API after v2.4.0

```python
from framework import create_text_chat_session

# Existing default behavior remains valid.
session = create_text_chat_session()

# Explicit provider path for external app integration.
session = create_text_chat_session(
    provider="openai",
    model="gpt-4o-mini",
    preset="text_chat",
    character_name="default",
)

response = session.ask("Hello. Please answer briefly.")
```

## Proposed public error usage after v2.4.0

```python
from framework import (
    FacadeConfigError,
    FacadeProviderError,
    create_text_chat_session,
)

try:
    session = create_text_chat_session(provider="openai")
    response = session.ask("Hello")
except FacadeConfigError as e:
    print(f"Configuration error: {e}")
except FacadeProviderError as e:
    print(f"Provider error: {e}")
```

## Notes

The main architectural goal is to make the facade stable for an external demo app while keeping the full runtime path independent. `main.py` remains the ready-to-run entry point. `framework.create_text_chat_session()` becomes the app-integration entry point.
