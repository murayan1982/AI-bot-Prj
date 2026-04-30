# Roadmap: v5.0.0 - Realtime Voice Runtime Foundation

v5.0.0 focuses on realtime voice interaction behavior.

The main goal is to make the framework feel closer to a live AI character conversation by improving interruption, cancellation boundaries, TTS control, and voice-oriented runtime flow.

This roadmap assumes v4.0.0 has already strengthened the app-facing SDK boundary.

## Positioning

v3.0.0 introduced the advanced runtime foundation:

- conversation state tracking
- state change events
- interruption request boundary
- TTS stop boundary
- voice output policy

v4.0.0 strengthens app-facing SDK integration:

- public session APIs
- app-safe metadata
- app examples
- app-facing state/event direction

v5.0.0 builds on both by implementing deeper realtime voice behavior behind stable control boundaries.

## Theme

```text
Realtime Voice Runtime Foundation
```

Alternative release label:

```text
Interruptible Voice Runtime
```

In practical terms:

```text
Make voice/TTS sessions interruptible, observable, and easier to control from apps and runtime code.
```

## Primary goals

- Improve interruption behavior during response generation and voice playback.
- Make TTS playback easier to stop, flush, and recover from.
- Clarify runtime state transitions for voice sessions.
- Prepare voice sessions for future always-on microphone barge-in.
- Keep app-facing control aligned with the SDK boundary introduced in v4.0.0.
- Improve manual testing flow for `voice_vts` and `text_vts` presets.

## Non-goals

v5.0.0 should still avoid becoming too broad.

Out of scope unless explicitly promoted:

- full production always-on microphone system
- wake word detection
- complex VAD tuning
- mobile app integration
- GUI overlay
- advanced memory system
- SSML editor
- pronunciation dictionary UI
- guaranteed provider-level hard cancellation for every LLM/TTS provider

Some provider-level cancellation can be implemented where practical, but the framework should expose a best-effort and predictable behavior rather than overpromising.

## Realtime voice scope

v5.0.0 should focus on the core runtime experience:

```text
user input -> LLM response -> streamed text -> TTS queue/playback -> Live2D expression
```

The key improvement is interruption:

```text
while responding or speaking:
    app/runtime requests interrupt
    framework stops or short-circuits what it safely can
    state transitions to interrupted/recovering/idle
    next user input can continue cleanly
```

## Interruption design direction

The public/app-facing action should remain simple:

```python
session.interrupt()
```

Internal runtime behavior may involve several layers:

- mark interruption requested
- stop streaming response loop when possible
- stop or flush TTS playback
- avoid sending more text to TTS after interruption
- optionally reset VTS expression to neutral
- emit state/event notifications
- return to a safe idle/listening state

The internal implementation should avoid mixing these meanings:

- cancel current LLM generation
- stop active TTS playback
- clear queued TTS segments
- stop accepting current input
- reset whole conversation
- close the session

Those should remain separate responsibilities even if `interrupt()` coordinates several of them.

## Runtime state direction

Existing v3.0.0 states:

- `idle`
- `listening`
- `thinking`
- `responding`
- `speaking`
- `interrupted`
- `exiting`
- `error`

v5.0.0 should validate whether these are enough.

Possible additions only if necessary:

- `cancelling`
- `recovering`

Avoid adding states unless they make implementation or debugging clearer.

Expected voice/TTS flow:

```text
idle -> listening -> thinking -> responding -> speaking -> idle
```

Expected interruption flow:

```text
responding -> interrupted -> idle
```

or:

```text
speaking -> interrupted -> idle
```

If cleanup takes meaningful time:

```text
speaking -> interrupted -> recovering -> idle
```

## TTS runtime direction

v5.0.0 should make TTS control more explicit.

Candidate internal TTS responsibilities:

- enqueue text chunks
- play queued speech
- stop active playback when possible
- flush queued text/audio
- clear pending text buffer
- report whether TTS is currently speaking

Potential methods:

```python
tts.speak(text)
tts.stop()
tts.flush()
tts.is_speaking()
```

The exact public/internal boundary should be decided during implementation.

Important:

- App code should not directly control provider-specific TTS internals.
- The session/runtime should own TTS coordination.
- Provider-specific stop behavior can be best-effort.

## LLM streaming cancellation direction

v5.0.0 should improve the streaming response loop so interruption requests are checked while chunks are being produced.

Expected behavior:

- if interruption is requested, stop yielding further chunks when possible
- avoid sending additional chunks to TTS after interruption
- return a controlled result rather than crashing
- emit an interruption-related event/state transition

Provider-specific hard cancellation may vary.

The minimum acceptable behavior is cooperative cancellation at the framework loop boundary.

## Voice input direction

v5.0.0 may improve the voice input flow, but full always-on barge-in is not required unless promoted into scope.

Recommended v5.0.0 scope:

- keep existing voice input preset behavior working
- make speaking/responding interruption manually testable
- prepare interfaces for future microphone-triggered interruption

Future v5.x or v6.0.0 scope:

- microphone listening while speaking
- VAD-based interruption
- wake word support
- background input monitor

## VTS / Live2D direction

VTS should remain optional.

During interruption, the framework may optionally:

- stop applying new expression changes
- reset expression to neutral
- emit a VTS-related debug message

Avoid making successful VTS connection a requirement for v5.0.0 runtime interruption tests.

## App SDK connection

v5.0.0 should use v4.0.0 app-facing boundaries where possible.

Example desired control shape:

```python
session = create_character_session(preset="voice_vts")

session.on_state_change(handle_state_change)
session.start()
session.interrupt()
session.close()
```

If a full voice session facade is still not ready, v5.0.0 can keep this as a design target and implement runtime-level behavior first.

The important rule:

```text
Do not expose internal runtime details just to make interruption controllable.
```

## Documentation targets

Update or add:

- `docs/roadmap_feature_v5.0.0.md`
- `docs/advanced_runtime.md`
- `docs/voice_output_policy.md`
- `docs/public_facade.md` or app SDK docs if voice APIs become public
- `docs/RELEASE_NOTES.md`

Docs should clearly distinguish:

- supported interruption behavior
- best-effort provider-specific behavior
- future full barge-in work

## Example targets

Possible examples:

- `examples/runtime_interrupt_demo.py`
- `examples/voice_tts_interrupt_demo.py`
- `examples/app_interrupt_session.py`

Manual preset checks:

```powershell
python main.py
scripts/run_text_vts.bat
scripts/run_voice_vts.bat
```

The exact example set depends on whether v5.0.0 exposes a public voice session API or keeps the work inside the runtime loop.

## Testing targets

Tests should cover:

- interruption request state transition
- clearing interruption flag
- TTS stop/flush boundary
- streaming loop cooperative cancellation
- state flow after interruption
- no crash when interrupting while idle
- no crash when TTS provider has nothing to stop
- no crash when VTS is unavailable
- examples importability
- release package checks

Existing v3.0.0 tests are a useful base:

- `scripts/test_interruption_state.py`
- `scripts/test_session_interrupt_command.py`
- `scripts/test_tts_stop_boundary.py`
- `scripts/test_runtime_state_flow.py`

v5.0.0 may add:

```powershell
python scripts/test_streaming_interrupt_boundary.py
python scripts/test_tts_interrupt_flow.py
python scripts/test_voice_runtime_state_flow.py
```

## Suggested Day plan

### Day 1 - Roadmap and scope lock

- Add v5.0.0 roadmap.
- Define v5.0.0 as Realtime Voice Runtime Foundation.
- Clarify what is and is not full barge-in.

Acceptance:

- Roadmap clearly separates v5.0.0 from future always-on microphone work.

### Day 2 - Runtime interruption inventory

- Review existing interruption helpers.
- Review `/interrupt` command behavior.
- Review state transitions.
- Identify where response generation and TTS playback can be interrupted.

Acceptance:

- Current interruption boundaries are documented before implementation.

### Day 3 - Interruption controller design

- Design a runtime-level interruption coordinator if needed.
- Keep public `interrupt()` simple.
- Keep internal cancellation responsibilities separated.

Acceptance:

- Interruption behavior has one clear owner.

### Day 4 - Streaming response cancellation

- Add cooperative cancellation checks to streaming response flow.
- Ensure interrupted streaming does not keep sending text to TTS.

Acceptance:

- Streaming can stop cleanly when interruption is requested.

### Day 5 - TTS stop and flush behavior

- Strengthen TTS stop boundary.
- Separate stop active playback from flush queued speech if useful.
- Keep behavior safe when no TTS provider is active.

Acceptance:

- Interrupting speech does not crash and does not continue queued playback unexpectedly.

### Day 6 - State transition hardening

- Validate state transitions for responding/speaking interruption.
- Add tests for idle/listening/thinking/responding/speaking interruption behavior.

Acceptance:

- Runtime returns to a safe state after interruption.

### Day 7 - Manual runtime demos

- Add or update manual interruption demo.
- Test text_vts and voice_vts behavior as far as possible.
- Keep VTS connection failure non-fatal.

Acceptance:

- Developer can manually verify interruption behavior without complex setup.

### Day 8 - Docs update

- Update advanced runtime docs.
- Document supported vs best-effort interruption behavior.
- Document remaining limitations.

Acceptance:

- Docs do not overpromise full concurrent barge-in.

### Day 9 - Smoke tests and release checks

- Add/adjust tests for interruption, TTS stop, streaming cancellation, and state flow.
- Run compile and release package checks.

Acceptance:

- Automated checks pass.

### Day 10 - Final release cleanup

- Update release notes.
- Run full checks.
- Prepare v5.0.0 tag and release.

Acceptance:

- v5.0.0 can be described as the realtime voice runtime foundation.

## Release acceptance checklist

v5.0.0 is ready when:

- Runtime interruption has a clear owner and documented behavior.
- Response streaming can cooperatively stop on interruption.
- TTS playback/queue can be stopped or flushed safely where supported.
- State transitions after interruption are predictable.
- Voice/TTS interruption limitations are clearly documented.
- VTS remains optional and non-fatal.
- Manual runtime checks are available.
- Automated tests cover the core interruption boundaries.
- Release package checks pass.

## Follow-up versions

### v5.1.x candidates

- Better provider-specific cancellation.
- More robust TTS queue management.
- Voice session facade if not completed in v5.0.0.
- Additional app-facing voice examples.
- More detailed event telemetry.

### Future major version candidates

Possible v6.0.0 theme:

```text
Always-on Voice Barge-in / Voice Interaction UX
```

Potential future scope:

- microphone listening while speaking
- VAD-based interruption
- wake word support
- background input monitoring
- more natural turn-taking UX
