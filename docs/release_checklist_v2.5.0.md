# Release Checklist - v2.5.0

## Goal

Confirm that v2.5.0 is ready to release as an app integration readiness update for the public text facade.

## Scope

v2.5.0 includes:

- `TextChatSessionInfo`
- `TextChatSession.info`
- public session metadata for external app integration
- app integration contract documentation
- README and public facade documentation updates
- smoke checks for session info and optional direct provider live checks

v2.5.0 does not include:

- voice input support through the public text facade
- TTS output support through the public text facade
- Live2D / VTube Studio control through the public text facade
- full runtime loop changes
- voice-friendly output policy implementation

## Required checks

Run these before tagging the release:

```powershell
python -m compileall -q .
python scripts/smoke_public_facade.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
python examples/minimal_app_text_chat.py --provider openai --model gpt-4o-mini --message "こんにちは。1文で短く返して。"
```

## Optional direct provider smoke check

Run this when provider API keys are configured and a live check is desired:

```powershell
python scripts/smoke_public_facade.py --provider openai --model gpt-4o-mini --ask "こんにちは。短く返して"
```

Expected direct provider info shape:

```text
TextChatSessionInfo(... llm_mode='direct_provider', provider='openai', model='gpt-4o-mini', route_name=None, ...)
```

Expected default route info shape:

```text
TextChatSessionInfo(... llm_mode='default_route', provider=None, model=None, route_name='chat', ...)
```

## Documentation checks

Confirm these files are present and aligned:

- `README.md`
- `docs/public_facade.md`
- `docs/app_integration_contract.md`
- `docs/RELEASE_NOTES_v2.5.0.md`
- `examples/public_text_chat.py`
- `examples/minimal_app_text_chat.py`

## Public API boundary

The public `framework` package should expose:

- `create_text_chat_session`
- `TextChatSession`
- `TextChatSessionInfo`
- `FacadeError`
- `FacadeConfigError`
- `FacadeProviderError`

Importing `framework` should not start the runtime, connect to VTube Studio, initialize STT/TTS, or create provider clients.

## Repository cleanliness checks

Before building a distribution zip or creating a tag, confirm that only intended files are tracked:

```powershell
git status
git diff --check
git ls-files | findstr /i "__pycache__ .pyc"
```

Expected result for the last command:

```text
(no output)
```

Do not include generated cache files, local `.env` files, or temporary patch files in the release commit or distribution zip.

## Distribution zip sanity check

After creating the distribution zip, inspect the contents before uploading it.

```powershell
python -c "from pathlib import Path; from zipfile import ZipFile; zip_path=Path('dist/ai-character-framework_v2.5.0.zip'); names=ZipFile(zip_path).namelist(); bad=[n for n in names if '__pycache__' in n or n.endswith('.pyc') or n.endswith('/.env') or n == '.env']; assert not bad, bad[:10]; print(f'OK: {zip_path} contains {len(names)} entries')"
```

If your zip path is different, adjust `zip_path` before running the check.


## Release notes

Use `docs/RELEASE_NOTES_v2.5.0.md` as the source for the GitHub release summary.

Suggested tag:

```powershell
git tag v2.5.0
```
