"""Environment and global runtime configuration for blog toolkit."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEPRECATED_MODELS = {"gemini-3.5-flash"}


def resolve_gemini_model(explicit_model: str | None = None) -> str:
    """Resolve Gemini model name, healing deprecated non-existent model IDs."""
    raw = (explicit_model or os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()
    if not raw or raw in DEPRECATED_MODELS:
        return DEFAULT_GEMINI_MODEL
    return raw


class ToolkitConfig:
    """Runtime configuration pulled from environment variables."""

    @classmethod
    def gemini_api_key(cls) -> str:
        """Retrieve Gemini API key from environment."""
        return os.getenv("GEMINI_API_KEY", "").strip()

    @classmethod
    def gemini_model(cls) -> str:
        """Retrieve active Gemini model (defaults to gemini-2.5-flash)."""
        return resolve_gemini_model()

    @classmethod
    def default_preset(cls) -> str:
        """Default preset to load if none specified."""
        return os.getenv("BLOG_TOOLKIT_PRESET", "el_laundry").strip()

    @classmethod
    def sync_path(cls) -> Path | None:
        """Default Next.js output sync path if defined."""
        raw = os.getenv("BLOG_TOOLKIT_SYNC_PATH", "").strip()
        return Path(raw) if raw else None
