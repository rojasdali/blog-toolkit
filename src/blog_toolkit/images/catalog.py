"""Image catalog storage and scanning."""

import json
from pathlib import Path

from blog_toolkit.images.catalog_data import DEFAULT_EL_LAUNDRY_IMAGES
from blog_toolkit.images.types import ImageItem


class ImageCatalog:
    """Catalog of authenticated brand photography."""

    def __init__(self, images: list[ImageItem] | None = None):
        self.images = images or [ImageItem(**img) for img in DEFAULT_EL_LAUNDRY_IMAGES]

    @classmethod
    def from_file(cls, path: str | Path) -> "ImageCatalog":
        """Load image catalog from JSON."""
        file_path = Path(path)
        if not file_path.exists():
            return cls()
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return cls(images=[ImageItem(**d) for d in data])

    def add_image(self, item: ImageItem) -> None:
        """Add image to catalog."""
        self.images.append(item)
