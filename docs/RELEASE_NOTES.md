## v3.0.0 - Advanced Runtime Foundation

### Summary

v3.0.0 introduces an advanced runtime foundation for more natural AI character conversation experiences.

This release focuses on:

- explicit runtime conversation state
- plugin-facing state change events
- interruption request boundaries
- manual interruption debug command support
- best-effort TTS stop handling
- voice-friendly prompt construction for TTS-enabled sessions
- lightweight regression tests for the new runtime boundaries
- advanced runtime documentation for developers extending the framework

### Added

- Added explicit runtime conversation states:
  - `idle`
  - `listening`
  - `thinking`
  - `responding`
  - `speaking`
  - `interrupted`
  - `exiting`
  - `error`
- Added `RuntimeState` as the mutable state object for one active runtime session.
- Added `on_state_change(old_state, new_state)` runtime event for plugins.
- Added state-aware plugin event documentation in `plugin_events.md`.
- Added interruption helper boundary:
  - `request_interruption(runtime)`
  - `clear_interruption(runtime)`
  - `is_interruption_requested(runtime)`
- Added a manual `/interrupt` debug command for verifying the interruption boundary.
- Added best-effort TTS stop boundary through `VoiceEngine.stop()`.
- Added voice-friendly output policy design in `voice_output_policy.md`.
- Added prompt builder boundary for final system instruction layers.
- Added voice output policy injection for TTS-enabled sessions.
- Added advanced runtime documentation in `advanced_runtime.md`.
- Added lazy TTS settings validation so text-only startup does not depend on voice provider settings.
- Added lightweight runtime boundary regression checks:
  - `scripts/test_prompt_builder.py`
  - `scripts/test_interruption_state.py`
  - `scripts/test_tts_stop_boundary.py`
  - `scripts/test_runtime_state_flow.py`
  - `scripts/test_session_interrupt_command.py`
  - `scripts/test_tts_settings_lazy_validation.py`

### Changed

- Separated assistant runtime states for:
  - waiting for LLM output: `thinking`
  - displaying assistant text: `responding`
  - waiting for TTS playback: `speaking`
- Kept final `idle` transitions owned by the session loop.
- Kept character prompts focused on character identity and behavior.
- Moved final system instruction construction into a prompt-building layer.
- Kept voice output policy disabled for text-only sessions by default.
- Kept public text facade behavior text-only and unchanged by default.
- Clarified plugin state ownership: plugins may observe runtime state but should not mutate it directly.
- Clarified that `/interrupt` is a development debug route, not full concurrent voice barge-in.
- Delayed TTS voice configuration validation until TTS runtime initialization so `text_chat` remains the safest first-run preset.

### Documentation

- Added `advanced_runtime.md` for the v3.0 runtime foundation.
- Added `voice_output_policy.md` for TTS-friendly output policy design.
- Updated README validation checks to include the new runtime boundary tests.
- Updated the v3.0 roadmap with the completed runtime foundation work.

### Verification

Run the standard checks before tagging the release:

```powershell
python -m compileall -q .
python scripts/test_prompt_builder.py
python scripts/test_interruption_state.py
python scripts/test_tts_stop_boundary.py
python scripts/test_runtime_state_flow.py
python scripts/test_session_interrupt_command.py
python scripts/test_tts_settings_lazy_validation.py
python scripts/smoke_public_facade.py
python examples/app_error_handling.py
python examples/public_text_chat.py
python examples/minimal_app_text_chat.py
```

Optional release package sanity check:

```powershell
python scripts/check_release_package.py
```

Manual runtime checks:

```powershell
python main.py
```

Confirmed with `APP_PRESET=text_chat`:

- no voice output policy is added
- state flow reaches `listening -> thinking -> responding -> idle`
- `/interrupt` transitions through `listening -> interrupted -> idle`

Confirmed with `APP_PRESET=voice_vts`:

- voice output policy is added
- state flow reaches `responding -> speaking -> idle`
- TTS-enabled prompt construction keeps language instruction, voice output policy, emotion tag instruction, and character prompt separated

### Notes

The interruption support in this release is a foundation layer.

It does not yet provide full concurrent voice barge-in, microphone listening while TTS is speaking, provider-level LLM request cancellation, or production-grade interruption UX.

Those remain future v3.x topics.

### Notes for GitHub Release

When publishing the release, copy the relevant contents of this file into the GitHub Release page.

After the next version starts, this file may be updated for the next current release.  
Past release details are preserved by the corresponding Git tag and GitHub Release.
