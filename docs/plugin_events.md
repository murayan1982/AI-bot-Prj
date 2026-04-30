# Plugin Runtime Events

This document describes the runtime event hooks available to plugins.

Plugins have two integration surfaces:

1. Lifecycle methods
2. Runtime event hooks

## Lifecycle Methods

Lifecycle methods are defined by `BasePlugin`.

```python
setup(runtime)
on_start(runtime)
on_stop(runtime)
```

Use lifecycle methods for setup, startup, and shutdown behavior.

## Runtime Event Hooks

Runtime event hooks allow plugins to observe events emitted by the framework.

Supported events:

| Event | Callback Arguments | Description |
| --- | --- | --- |
| `on_user_input` | `user_input` | Emitted after one user input is received. |
| `on_llm_chunk` | `chunk` | Emitted when an LLM response chunk is produced. |
| `on_llm_complete` | `full_text` | Emitted after one assistant response is complete. |
| `on_emotion_detected` | `emotions` | Emitted when emotion tags are detected. |
| `on_state_change` | `old_state, new_state` | Emitted when the runtime conversation state changes. |
| `on_error` | `error` | Emitted when a runtime error is handled. |

## Conversation States

`on_state_change` receives `ConversationState` values.

| State | Meaning |
| --- | --- |
| `idle` | The session is idle between turns. |
| `listening` | The session is collecting user input. |
| `thinking` | The framework is waiting for LLM output. |
| `responding` | The assistant text response is being displayed or streamed. |
| `speaking` | The framework is waiting for queued TTS playback. |
| `interrupted` | Reserved for future interruption and barge-in handling. |
| `exiting` | The session is shutting down. |
| `error` | The session is handling an error. |

## State Ownership

Plugins should treat runtime state as read-only.

Plugins may observe state transitions through `on_state_change`, but should not directly
modify `runtime["state"]`.

State transitions are owned by the framework runtime, session loop, and response pipeline.

## Minimal Example

```python
from typing import Any

from core.events import EVENT_STATE_CHANGE
from plugins import BasePlugin


class StateLoggerPlugin(BasePlugin):
    name = "state_logger"

    def setup(self, runtime: dict[str, Any]) -> None:
        self.add_hook(runtime, EVENT_STATE_CHANGE, self.on_state_change)

    def on_state_change(self, old_state: Any, new_state: Any) -> None:
        old_value = getattr(old_state, "value", str(old_state))
        new_value = getattr(new_state, "value", str(new_state))
        print(f"state: {old_value} -> {new_value}")
```

## Notes

Runtime event hooks are observer hooks.

They are useful for logging, metrics, UI updates, external integrations, and debugging.
They should not be used to mutate core runtime state directly.