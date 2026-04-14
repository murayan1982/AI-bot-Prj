from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class RuntimeConfig:
    app_preset: str
    input_language_code: str
    output_language_code: str


def load_preset_file(preset_name: str) -> dict:
    preset_path = Path("presets") / f"{preset_name}.json"

    if not preset_path.exists():
        raise FileNotFoundError(f"Preset file not found: {preset_path}")

    with preset_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_runtime_config() -> RuntimeConfig:
    load_dotenv()

    preset_name = os.getenv("APP_PRESET", "default")
    preset_data = load_preset_file(preset_name)

    config = RuntimeConfig(
        app_preset=preset_data.get("app_preset", preset_name),
        input_language_code=preset_data.get("input_language_code", "ja"),
        output_language_code=preset_data.get("output_language_code", "ja"),
    )

    print(f"[Config] Loaded preset: {preset_name}")
    return config


if __name__ == "__main__":
    config = load_runtime_config()
    print(config)