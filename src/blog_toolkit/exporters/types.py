"""Exporter interfaces and types."""

from typing import Protocol

from blog_toolkit.core.types import BlogPost


class BlogExporter(Protocol):
    """Protocol for blog content exporters."""

    def export(self, post: BlogPost) -> str:
        """Export a BlogPost to a string format."""
        ...
