# Tasklist: v2.1.0 - Audio Pipeline Responsibility Cleanup

## Goal

Clarify the responsibility boundaries of the voice conversation pipeline
without changing the core conversation behavior.

v2.1 prepares the framework for later work on provider abstraction,
conversation state, latency-oriented streaming voice, interruption, and
runtime event expansion.

---

## Scope

In scope:

- review the current `voice_vts` flow
- clarify the role of `core/session.py`
- clarify the role of `core/pipeline.py`
- clean up user input flow
- clean up response streaming flow
- clean up TTS playback boundary
- review fallback and shutdown behavior

Out of scope:

- OpenAI provider support
- full STT / TTS provider abstraction
- conversation state machine
- interruption / barge-in implementation
- latency optimization
- multi-character conversation
- runtime event expansion

---

## Day1: Voice Flow Review & Scope Lock

- [ ] Review current `voice_vts` flow
- [ ] Confirm `core/session.py` owns the top-level conversation loop
- [ ] Confirm `core/pipeline.py` owns input / response / TTS playback helpers
- [ ] Identify where STT, LLM, TTS, emotion, and VTS are connected
- [ ] Confirm v2.1 does not change core behavior
- [ ] Confirm v2.2+ topics remain out of scope

Goal:
v2.1 scope is clear before touching implementation.

## Day1 Notes

Current responsibility boundaries:

- `core/session.py` owns the top-level conversation loop.
- `core/pipeline.py` owns user input collection, AI response processing, streaming display, optional TTS enqueue, and TTS playback wait.
- `stt/stt_engine.py` is currently provider-specific and should not be abstracted in v2.1.
- `tts/voice_engine.py` is currently provider-specific and should only be touched lightly in v2.1.
- VTS expression triggering is handled through runtime events and plugins, not directly owned by the session loop.

Confirmed out of scope for v2.1:

- OpenAI provider support
- full STT / TTS provider abstraction
- conversation state machine
- interruption / barge-in
- latency optimization
- multi-character conversation
- runtime event expansion

Day1 conclusion:

v2.1 should keep the current behavior stable and focus on clarifying the audio conversation pipeline responsibilities before moving into provider abstraction and conversation state work in later milestones.