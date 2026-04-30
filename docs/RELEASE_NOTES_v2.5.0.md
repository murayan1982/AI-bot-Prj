# Release Notes - v2.5.0

## App Integration Readiness

v2.5.0 improves the public text facade for external application integration.

## Added

- Added `TextChatSessionInfo` as a small public info model for app integrations.
- Added `TextChatSession.info`.
- Added `docs/app_integration_contract.md` for external application integration guidance.
- Added direct provider/model live smoke check options:
  - `python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"`
- Exposed stable text facade metadata:
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

## Changed

- Updated public facade examples to show session info.
- Updated minimal app integration example to expose app-level `session_info`.
- Updated smoke checks for the public info model.
- Updated README with `session.info` usage and app integration boundary notes.
- Clarified that importing `framework` should not create provider clients.
- Linked the app integration contract from `docs/public_facade.md`.
- Updated `docs/public_facade.md` with default route and direct provider smoke check examples.

## Design notes

`TextChatSession.info` intentionally does not expose `RuntimeConfig`.

The public info model is limited to integration-safe metadata so application code
can inspect the session without depending on internal runtime configuration
details.

When the facade uses the default chat route, `provider` and `model` are hidden
as `None` and `route_name` is set to `"chat"`.

When the facade uses direct provider mode, `provider` and `model` expose the
resolved provider/model pair and `route_name` is `None`.

## Verification

Recommended release checks:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
python examples/minimal_app_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

Optional direct provider smoke check:

```powershell
python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
```

## Future note

A future version may add a framework-level voice-friendly output policy for
TTS-enabled sessions.

That policy should make LLM responses easier to read aloud while remaining
separate from character personality prompts.
