# Roadmap: Toward v3.0 - Advanced Conversation Runtime

## Goal

After v2.0 established the minimum AI character conversation UX, the framework has also gained a clearer public text facade and external app integration path through the v2.5.0 and v2.6.0 releases.

The next major direction is to evolve the framework from a simple input -> response flow into a more natural real-time conversation runtime, while keeping the public documentation and distribution package clean enough for new developers to understand.

v3.0 focuses on improving the runtime foundation for:

- voice conversation flow
- conversation state
- provider abstraction
- latency-oriented response design
- interruption / barge-in
- multi-character conversation
- extensible runtime events
- documentation structure that separates quick-start usage from advanced design details

The goal is not to turn the framework into a finished commercial app.
The goal is to make the framework easier to extend toward richer AI character experiences.

---

## Current Position After v2.6.0

### v2.5.0 - App Integration Readiness

v2.5.0 clarified how external applications can use the public text facade.

Established foundation:

- `TextChatSession.info`
- `TextChatSessionInfo`
- public session metadata
- default route / direct provider mode distinction
- app integration contract docs
- no direct exposure of `RuntimeConfig`

### v2.6.0 - App Integration Examples

v2.6.0 made the public text facade easier to understand through small app-style examples.

Established examples:

- basic public text chat
- minimal app integration
- error handling
- streaming responses
- session reset
- session info display

### Remaining Pre-v3.0 Cleanup

Before expanding into heavier v3.0 runtime design, the project should clean up documentation and release package structure.

The README has accumulated version-specific notes over time. This makes it harder for new users to understand what the framework currently is and how to start.

The next cleanup should make the README a stable entry point, move version history into release notes, and keep release-operation files out of public distribution packages.

---

## [v2.7] Documentation Structure and Release Packaging Cleanup

### Goal

Make the public documentation and release package easier to understand before starting larger v3.0 runtime work.

### README Responsibility

`README.md` should be the project entry point.

It should explain:

- what the framework is
- who it is for
- what it can do now
- how to try it quickly
- how to use the public text facade at a minimal level
- where to find detailed docs
- license summary and distribution notes

It should avoid becoming:

- a version-by-version changelog
- a release checklist
- a long facade API reference
- a full design document
- an internal development log

Current release details should live in `docs/RELEASE_NOTES.md`.
Historical release notes are preserved by Git tags and GitHub Releases.
Detailed facade usage should live in `docs/public_facade.md`.
External app boundary rules should live in `docs/app_integration_contract.md`.

### Documentation Separation Policy

Recommended documentation roles:

- `README.md`
  - project overview
  - quick start
  - current feature summary
  - minimal public facade example
  - links to detailed docs

- `docs/public_facade.md`
  - public facade API details
  - `create_text_chat_session`
  - `TextChatSession`
  - `TextChatSessionInfo`
  - `ask`, `ask_stream`, `reset`
  - facade error classes
  - example list

- `docs/app_integration_contract.md`
  - external app integration boundary
  - what is public and stable
  - what is internal
  - why apps should not depend on `RuntimeConfig`

- `docs/RELEASE_NOTES.md`
  - version-specific changes
  - added / changed / fixed notes
  - verification commands used for that release
  - Historical release details are not accumulated on `main`.
  - Past release notes are preserved by Git tags and GitHub Releases.

- internal release-operation notes
  - may exist during development
  - should not be required by public README/docs
  - should not be linked from files included in public distribution packages unless intentionally included

### Release Checklist Policy

Release checklist files are internal release-operation notes.

They may be useful while preparing a release, but public distribution packages should not depend on them.

Rules:

- Do not link from public `README.md` to internal-only release checklist files.
- Do not link from public docs to files that are intentionally excluded from the distribution zip.
- Put public verification commands directly in release notes when useful.
- Keep distribution packages self-contained: every linked file in README/docs should exist in the package.
- Keep `__pycache__`, `.pyc`, `.env`, and repository metadata out of release zips.

### Packaging Hygiene

v2.7 should review build and release packaging behavior.

Tasks:

- Review build zip batch/scripts.
- Confirm which docs are included in public distribution packages.
- Confirm internal release-operation files are excluded or clearly marked.
- Add a package sanity check if useful.
- Check that README/docs links do not point to missing files.
- Check that generated files are not included accidentally.
- Document the intended release package contents.

### Out of Scope for v2.7

- voice / TTS output policy implementation
- audio pipeline rewrite
- STT / TTS provider abstraction implementation
- interruption / barge-in implementation
- multi-character runtime implementation
- demo app UI work

Goal:
The project has a clean README, clearer docs responsibility boundaries, and a safer release package process before v3.0 runtime work begins.

---

## [v3.0] Advanced Conversation Runtime

v3.0 is the milestone for advanced conversation runtime.

It should make the framework ready for more natural real-time AI character interactions while preserving the simple text facade and current quick-start path.

Focus:

- clearer audio pipeline responsibilities
- provider abstraction
- conversation state management
- latency-aware streaming voice flow
- voice-friendly output policy design
- interruption / barge-in foundation
- backchannel / minimal reactive response design
- multi-character conversation design
- richer plugin / hook integration points
- README/docs that explain both the simple start and advanced extension path

---

## v3.0 Workstream 1 - Audio Pipeline Responsibility Cleanup

- Clarify STT / LLM / TTS responsibility boundaries.
- Make the voice conversation loop easier to read and extend.
- Separate listening, thinking, speaking, fallback, and shutdown concerns.
- Keep provider-specific behavior out of the main runtime flow where possible.
- Prepare the pipeline for future async and latency improvements.
- Review how `voice_vts` handles:
  - voice input
  - text fallback
  - TTS output
  - shutdown
  - VTS / emotion side effects

Goal:
The audio conversation pipeline is easier to maintain and ready for future latency work.

---

## v3.0 Workstream 2 - Provider Abstraction Foundation

- Clarify STT provider boundaries.
- Clarify TTS provider boundaries.
- Revisit LLM provider / route / fallback responsibilities.
- Keep provider registry separate from runtime behavior.
- Keep provider-specific configuration out of the core conversation loop where possible.
- Document how developers can switch or add providers.
- Review existing and future registry responsibilities:
  - `registry/llm.py`
  - `registry/tts.py`
  - future STT provider registry if needed

Goal:
LLM / STT / TTS providers can be handled as framework-level configuration rather than hardcoded runtime assumptions.

---

## v3.0 Workstream 3 - Conversation State Foundation

- Define conversation states such as:
  - idle
  - listening
  - thinking
  - responding
  - speaking
  - interrupted
  - exiting
- Clarify how runtime state is displayed to the user.
- Clarify how runtime state is represented internally.
- Make conversation state easier to expose through hooks / plugins.
- Review how state should interact with:
  - text input
  - voice input
  - text fallback
  - TTS output
  - VTS expression changes
  - shutdown flow
- Prepare for interruption and backchannel behavior.

Goal:
Conversation state becomes a clear runtime concept.

### Day1 - Runtime Conversation State Foundation

Goal:
Introduce explicit runtime conversation state before heavier voice, interruption, and plugin expansion work.

Implemented direction:

- Add `ConversationState` and `RuntimeState`.
- Add `on_state_change` runtime event.
- Track high-level session states:
  - `idle`
  - `listening`
  - `thinking`
  - `responding`
  - `speaking`
  - `interrupted`
  - `exiting`
  - `error`
- Keep `thinking`, `responding`, and `speaking` separate:
  - `thinking`: waiting for LLM output
  - `responding`: displaying assistant text response
  - `speaking`: waiting for queued TTS playback
- Keep final return to `idle` in the session loop instead of the pipeline.

Expected text-only flow:

```text
idle -> listening -> thinking -> responding -> idle
```

Expected TTS flow:

```text
idle -> listening -> thinking -> responding -> speaking -> idle
```

---

### Day2 - State-aware Plugin Contract

Goal:
Document and stabilize the plugin-facing runtime event contract introduced by the runtime state foundation.

Implemented:

- Add `docs/plugin_events.md`.
- Document lifecycle methods separately from runtime event hooks.
- Document `on_state_change(old_state, new_state)`.
- Document conversation state values and ownership.
- Clarify that plugins may observe runtime state but should not mutate it directly.
- Keep examples documentation-only for now to avoid expanding the public example surface too early.

---

### Day3 - Interruption Boundary Foundation

Goal:
Prepare the runtime and response pipeline for future barge-in and interruption handling.

Implemented direction:

- Add an interruption request flag to `RuntimeState`.
- Add helper functions for requesting, clearing, and checking interruption.
- Clear pending interruption at the beginning of each user turn.
- Add interruption checks around LLM streaming and TTS playback boundaries.
- Transition to `interrupted` when an interruption request is observed.
- Keep actual audio cancellation and automatic voice barge-in for later work.

---

### Day4 - Minimal Interruption State Tests

Goal:
Lock down the interruption helper behavior introduced by Day3.

Implemented direction:

- Add `scripts/test_interruption_state.py`.
- Verify initial runtime state and interruption flag.
- Verify `request_interruption()` transitions to `interrupted` and emits `on_state_change`.
- Verify `clear_interruption()` clears only the interruption flag.
- Keep state reset ownership in the session loop through explicit state transitions.

---

### Day5 - TTS Stop Boundary

Goal:
Prepare TTS playback for future interruption and barge-in handling.

Implemented direction:

- Add a framework-level best-effort TTS stop boundary.
- Allow the response pipeline to request TTS stop when interruption is observed.
- Keep provider/player-specific hard cancellation as a later implementation detail.
- Avoid failing the session when a provider does not support immediate stop.
- Preserve the existing text-only flow and public text facade behavior.

---

### Day6 - Voice-Friendly Output Policy Design

Goal:
Design a separate runtime output policy for TTS-enabled sessions without mixing voice readability concerns into character prompts.

Planned direction:

- Add `docs/voice_output_policy.md`.
- Separate output language, character instruction, and voice output policy responsibilities.
- Define when the policy should apply.
- Keep text-only sessions unchanged by default.
- Keep provider-specific pronunciation handling out of scope.
- Prepare for a later prompt-builder implementation.

---

### Day7 - Voice Output Policy Prompt Boundary

Goal:
Prepare prompt construction so TTS-enabled sessions can receive voice-friendly output guidance without mixing it into character prompts.

Planned direction:

- Add a small prompt-building boundary for final system instruction layers.
- Keep output language instruction separate from character prompt.
- Add voice output policy only when voice/TTS output is active.
- Keep text-only sessions unchanged by default.
- Avoid provider-specific pronunciation handling in this layer.

---

### Day8 - Runtime Boundary Regression Tests

Goal:
Add small regression tests for the new v3.0 runtime boundaries before expanding the feature set further.

Implemented direction:

- Add a minimal TTS stop boundary test without requiring real TTS provider initialization.
- Add a minimal pipeline state flow test using a fake LLM.
- Verify the response pipeline transitions from `idle` to `thinking` to `responding`.
- Verify the TTS stop boundary clears active playback process, pending text buffer, and queued segments.
- Keep tests lightweight and runnable without API calls.

---

### Day9 - Interruption Debug Trigger Route

Goal:
Add a small development-only route for manually triggering the interruption boundary.

Implemented direction:

- Add a manual `/interrupt` debug command.
- Route the command through `request_interruption(runtime)`.
- Transition through `interrupted` and return to `idle`.
- Keep this separate from real concurrent barge-in behavior.
- Add a lightweight command detection test.

---

### Day10 - Advanced Runtime Behavior Documentation

Goal:
Document the v3.0 runtime foundation so the new state, interruption, TTS stop, and voice output policy behavior can be understood as one coherent feature set.

Implemented direction:

- Add `docs/advanced_runtime.md`.
- Document runtime conversation states and expected state flows.
- Document `on_state_change` as the plugin-facing state observation hook.
- Document the interruption helper boundary.
- Document the manual `/interrupt` debug command and its current limitation.
- Document the best-effort TTS stop boundary.
- Link to plugin event and voice output policy details.

---

### Day11 - v3.0.0 Release Notes and Verification Docs

Goal:
Prepare release-facing documentation for the v3.0.0 advanced runtime foundation.

Implemented direction:

- Add v3.0.0 draft notes to `docs/RELEASE_NOTES.md`.
- Summarize runtime state, interruption, TTS stop, and voice output policy changes.
- Document verification commands used for v3.0.0 development.
- Update README validation checks with the new runtime boundary tests.
- Keep full concurrent barge-in and provider-level cancellation documented as future v3.x work.

---

## v3.0 Workstream 4 - Voice-Friendly Output Policy Design

This is a design topic before implementation.

The framework should eventually support an output policy for TTS-enabled sessions so LLM responses are easier for speech synthesis to read aloud.

The policy should be treated as framework-level output-quality guidance, not character personality.

Design principles:

- Enable only when audio/TTS output is active.
- Keep character prompts focused on who the character is.
- Keep output policy focused on how responses should be spoken.
- Prefer natural spoken sentences.
- Avoid unnecessary symbols, dense Markdown, tables, and excessive abbreviations.
- Keep code, commands, file paths, URLs, environment variable names, and proper nouns unchanged when necessary.
- Do not override `output_language_code`.
- Keep the policy optional and easy to disable.

Open questions:

- Should this live in prompt builder, runtime config, preset config, or a dedicated output policy module?
- Should text-only sessions ever use it?
- Should voice presets enable it by default?
- How should it interact with code answers and developer-focused output?
- How should it interact with emotion tags and VTS expression control?

Goal:
The framework has a clear design path for TTS-friendly LLM output without mixing output formatting concerns into character personality.

---

## v3.0 Workstream 5 - Latency-Oriented Streaming Voice Foundation

- Review how LLM streaming can connect to TTS output.
- Consider chunk / sentence / utterance boundaries.
- Clarify when TTS should start speaking.
- Align display / TTS / emotion / VTS timing.
- Review whether emotion parsing should happen:
  - before speech
  - per response
  - per utterance
  - after full response
- Build the structure for future latency improvements without over-optimizing yet.
- Keep the first implementation understandable and easy to debug.

Goal:
The framework has a clearer path toward faster-feeling voice responses.

---

## v3.0 Workstream 6 - Interruption / Barge-in Prototype

- Explore minimal interruption behavior.
- Review input detection while the character is speaking.
- Clarify TTS stop responsibility.
- Clarify LLM response cancel responsibility.
- Clarify state rollback or state transition behavior.
- Decide how interruption should be represented in runtime state.
- Keep the first version experimental and easy to disable.
- Treat this as a prototype before full stabilization.

Goal:
The framework has an entry point for more natural interruption behavior.

---

## v3.0 Workstream 7 - Backchannel / Minimal Reactive Response Design

- Explore lightweight backchannel behavior such as short acknowledgements.
- Clarify whether backchannel is:
  - generated by LLM
  - rule-based
  - plugin-driven
  - provider-specific
- Review how backchannel should interact with TTS.
- Review how backchannel should interact with VTS expressions.
- Keep the design optional and non-invasive.
- Avoid making the core runtime too complex too early.

Goal:
The framework has a design path for more natural listening and acknowledgement behavior.

---

## v3.0 Workstream 8 - Multi-Character Conversation Design

- Explore how multiple characters should be represented at runtime.
- Clarify speaker / character_id / voice / VTS mapping.
- Keep compatibility with the one-character-one-directory structure.
- Review whether each character should have:
  - profile
  - system prompt
  - voice settings
  - VTS hotkey mapping
  - memory scope
- Decide whether implementation should start as a prototype or remain design-only.
- Clarify how multi-character conversation should affect presets and runtime config.

Goal:
The framework has a clear design path toward multi-character conversation.

---

## v3.0 Workstream 9 - Runtime Event & Plugin Expansion

- Review existing hook / plugin responsibilities.
- Add or clarify runtime events for advanced conversation flow.
- Consider events such as:
  - on_state_change
  - on_listening_start
  - on_listening_end
  - on_thinking_start
  - on_speaking_start
  - on_speaking_end
  - on_interrupt
  - on_character_switch
- Keep the core runtime small.
- Avoid forcing all advanced behavior into the main pipeline.
- Make advanced behavior easier to prototype through plugins.

Goal:
Advanced conversation features can be extended through runtime events and plugins instead of hardcoded into the core.

---

## Documentation Principles for v3.0

- README should stay short and current-state oriented.
- Detailed advanced runtime design should live under `docs/`.
- Version-specific changes should stay in release notes.
- Internal release-operation files should not be required by public docs.
- Public examples should remain small and copy-friendly.
- The simple `text_chat` starting point should remain easy to find.
- Advanced voice/runtime features should be documented as stable, experimental, or future work.

---

## Runtime Design Principles

- Keep the framework developer-oriented.
- Prefer clear responsibility boundaries over early optimization.
- Keep `RuntimeConfig` as the runtime behavior source of truth.
- Keep public facade models separate from internal runtime config.
- Keep character files focused on who the character is.
- Keep presets focused on how the framework runs.
- Keep provider definitions separate from runtime behavior.
- Keep plugins and hooks as extension points, not required complexity.
- Add advanced conversation features incrementally.
- Prefer prototype flags for experimental behavior.
- Avoid breaking the simple `text_chat` starting point.

---

## Out of Scope Before v3.0

- Full commercial application UI
- Full Web UI / settings screen
- Cloud sync
- Large-scale memory database
- Fully optimized low-latency voice stack
- Fully polished multi-agent product experience
- Production-grade interruption handling
- Production-grade multi-character agent orchestration

These may become future v3.x or v4.0 topics.

---

## Expected Outcome

By v3.0, the framework should provide a clearer foundation for advanced AI character conversation experiences.

Expected state:

- README is cleaner and easier for new users to understand.
- public docs are separated by responsibility.
- distribution packages do not link to missing internal files.
- audio pipeline responsibilities are easier to understand.
- provider boundaries are clearer.
- conversation state is represented explicitly.
- TTS-friendly output policy has a clear design direction.
- latency-oriented streaming voice work has a clear path.
- interruption and backchannel have prototype-level entry points.
- multi-character conversation has a clear design direction.
- plugins / hooks can support more advanced runtime behavior.
- README / docs explain both the simple starting point and advanced extension path.
