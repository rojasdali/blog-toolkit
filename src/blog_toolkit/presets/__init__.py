"""Built-in BrandProfile presets packaged inside blog_toolkit.presets."""

import json
from pathlib import Path
from typing import Any

from blog_toolkit.presets.default import DEFAULT_DATA, get_default_profile
from blog_toolkit.presets.el_laundry import EL_LAUNDRY_DATA, get_el_laundry_profile

BUILTIN_PRESETS: dict[str, dict[str, Any]] = {
    "el_laundry": EL_LAUNDRY_DATA,
    "default": DEFAULT_DATA,
}


def get_preset_data(preset_name: str) -> dict[str, Any]:
    """Resolve preset dictionary from Python registry or packaged JSON file."""
    if preset_name in BUILTIN_PRESETS:
        return dict(BUILTIN_PRESETS[preset_name])

    pkg_file = Path(__file__).resolve().parent / f"{preset_name}.json"
    if pkg_file.exists():
        return json.loads(pkg_file.read_text(encoding="utf-8"))

    repo_file = (
        Path(__file__).resolve().parent.parent.parent.parent / "presets" / f"{preset_name}.json"
    )
    if repo_file.exists():
        return json.loads(repo_file.read_text(encoding="utf-8"))

    raise FileNotFoundError(f"Preset '{preset_name}' not found in blog_toolkit.presets")


__all__ = [
    "BUILTIN_PRESETS",
    "DEFAULT_DATA",
    "EL_LAUNDRY_DATA",
    "get_default_profile",
    "get_el_laundry_profile",
    "get_preset_data",
]
