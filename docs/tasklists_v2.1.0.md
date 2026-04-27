---

## Day2: Input Flow Cleanup

- [x] Clarify `get_user_input()` responsibility with docstring
- [x] Keep the function signature focused on input-related dependencies
- [x] Keep keyboard input, voice input, and text fallback paths readable
- [x] Avoid introducing runtime-wide dependencies
- [x] Avoid STT provider abstraction

Goal:
User input collection is easier to understand without changing behavior.

## Day2 Notes

- `get_user_input()` intentionally receives only input-related dependencies:
  `use_stt`, `stt`, and `allow_text_fallback_during_stt`.
- The helper does not depend on the full runtime dictionary.
- Keyboard input, voice input, and optional text fallback remain part of the same input boundary.
- Conversation state handling remains out of scope for v2.1.

---

## Day3: Response Flow Cleanup

- [x] Clarify `process_ai_response()` responsibility
- [x] Separate small response-flow helpers where useful
- [x] Clarify display chunk handling
- [x] Clarify TTS enqueue behavior
- [x] Keep event emission order and core behavior stable
- [x] Confirm `voice_vts` still runs correctly

Goal:
AI response processing is easier to read while preserving the existing streaming, display, TTS, and event flow.

## Day3 Notes

- `process_ai_response()` remains the assistant turn coordinator.
- Emotion emission, display output, and TTS queueing are clearer boundaries.
- VTS remains connected through runtime events and plugins.
- Provider abstraction, latency optimization, and interruption behavior remain out of scope.

---

## Day4: TTS Playback Boundary Cleanup

- [x] Clarify `VoiceEngine` public boundary
- [x] Clarify `speak()` responsibility
- [x] Clarify `flush()` responsibility
- [x] Clarify `is_speaking_active` responsibility
- [x] Clarify `stop_immediately()` as a future interruption-facing boundary
- [x] Avoid TTS provider abstraction

Goal:
The runtime pipeline can depend on a clear TTS playback boundary without taking ownership of provider-specific behavior.

## Day4 Notes

- `VoiceEngine` currently owns ElevenLabs-backed TTS generation and local playback.
- The runtime pipeline should only rely on `speak()`, `flush()`, `is_speaking_active`, and `stop_immediately()`.
- `stop_immediately()` is kept as a future interruption-facing boundary.
- Full interruption / barge-in behavior remains out of scope for v2.1.

---

## Day5: Fallback / Shutdown Flow Review

- [ ] Review empty input behavior
- [ ] Review STT timeout / empty voice result behavior
- [ ] Review text fallback behavior
- [ ] Review `exit` / `quit` shutdown behavior
- [ ] Review `KeyboardInterrupt` behavior
- [ ] Confirm unexpected errors are emitted through `on_error`
- [ ] Confirm no LLM response is processed after `exit` / `quit`

Goal:
Fallback and shutdown paths are understandable and do not break the session loop.

## Day5 Notes

Fallback / shutdown flow review:

- Empty input is ignored and the session waits for the next turn.
- STT timeout or empty voice result can return to the loop safely.
- Text fallback can pass normal text into the same session flow.
- `exit` / `quit` breaks the session loop before LLM response processing.
- Unexpected exceptions are emitted through `on_error` and do not immediately kill the session loop.
- `KeyboardInterrupt` exits the session loop.

Note:

- `exit` / `quit` are currently emitted through `on_user_input` before shutdown.
  This is acceptable for v2.1 because plugins can observe all user input.
  Future command handling may choose to process session commands before plugin events.