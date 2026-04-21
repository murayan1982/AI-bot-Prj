from __future__ import annotations
from abc import ABC

class BasePlugin(ABC):
    """
    Base class for runtime plugins.

    Plugins share a small lifecycle contract:
    - setup(runtime)
    - on_start(runtime)
    - on_stop(runtime)

    More granular runtime events are handled separately through
    runtime["hooks"] and emit(), usually registered during setup().
    """

    name: str = "base_plugin"
    enabled: bool = True

    def setup(self, runtime: dict[str, Any]) -> None:
        """
        Called once when the plugin is registered or initialized.

        Override this method if the plugin needs access to runtime resources
        or wants to register event hooks through runtime["hooks"].
        """
        pass

    def on_start(self, runtime: dict[str, Any]) -> None:
        """
        Called when the application/runtime starts.
        """
        pass

    def on_stop(self, runtime: dict[str, Any]) -> None:
        """
        Called when the application/runtime stops.
        """
        pass