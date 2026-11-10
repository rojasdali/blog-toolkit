"""Backward-compatible re-export of blog_toolkit.presets."""

from blog_toolkit.presets import (
    BUILTIN_PRESETS,
    DEFAULT_DATA,
    EL_LAUNDRY_DATA,
    get_default_profile,
    get_el_laundry_profile,
    get_preset_data,
)

__all__ = [
    "BUILTIN_PRESETS",
    "DEFAULT_DATA",
    "EL_LAUNDRY_DATA",
    "get_default_profile",
    "get_el_laundry_profile",
    "get_preset_data",
]
