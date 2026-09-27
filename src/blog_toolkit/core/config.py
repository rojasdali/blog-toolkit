"""Environment and global runtime configuration for blog toolkit."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class ToolkitConfig:
    """Runtime configuration pulled from environment variables."""

    @classmethod
    def gemini_api_key(cls) -> str:
        """Retrieve Gemini API key from environment."""
        key = os.getenv("GEMINI_API_KEY", "").strip()
        return key

    @classmethod
    def default_preset(cls) -> str:
        """Default preset to load if none specified."""
        return os.getenv("BLOG_TOOLKIT_PRESET", "el_laundry").strip()

    @classmethod
    def sync_path(cls) -> Path | None:
        """Default Next.js output sync path if defined."""
        raw = os.getenv("BLOG_TOOLKIT_SYNC_PATH", "").strip()
        return Path(raw) if raw else None
