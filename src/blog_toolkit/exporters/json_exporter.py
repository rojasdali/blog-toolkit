"""JSON exporter producing raw structured documents."""

from blog_toolkit.core.types import BlogPost


class JsonExporter:
    """Exports a BlogPost to formatted JSON."""

    def export(self, post: BlogPost) -> str:
        """Convert post to formatted JSON string."""
        return post.model_dump_json(indent=2)
