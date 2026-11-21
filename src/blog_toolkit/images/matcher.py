"""Authentic brand photography matching logic under Zero Fake AI Policy."""

from blog_toolkit.images.catalog import ImageCatalog
from blog_toolkit.images.types import ImageItem


def _first_tag_match(candidates: list[ImageItem], topic_lower: str) -> ImageItem | None:
    """Return the first candidate image with a tag matching the lowercased topic."""
    for img in candidates:
        if any(tag.lower() in topic_lower for tag in img.tags):
            return img
    return None


class ImageMatcher:
    """Matches post topics strictly to authentic cataloged brand photography."""

    def __init__(self, catalog: ImageCatalog):
        self.catalog = catalog

    def _filter_unused(
        self,
        candidates: list[ImageItem],
        used_set: set[str],
    ) -> list[ImageItem]:
        """Prioritize images not currently used by existing posts."""
        unused = [img for img in candidates if img.path not in used_set]
        return unused if unused else candidates

    def is_authentic_image(self, image_path: str) -> bool:
        """Return True only when normalized image_path exists in the catalog."""
        if not isinstance(image_path, str):
            return False
        normalized = image_path.strip()
        return bool(normalized) and normalized in {img.path for img in self.catalog.images}

    def validate_image_path(self, image_path: str) -> ImageItem:
        """Return the cataloged ImageItem or raise ValueError for uncataloged paths."""
        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError(
                "Uncataloged or synthetic image path rejected by Zero Fake AI Policy: "
                f"{image_path!r}"
            )
        normalized = image_path.strip()
        for item in self.catalog.images:
            if item.path == normalized:
                return item
        raise ValueError(
            f"Uncataloged or synthetic image path rejected by Zero Fake AI Policy: {image_path!r}"
        )

    def select_best_image(
        self,
        topic: str,
        category: str,
        used_images: set[str] | list[str] | None = None,
    ) -> ImageItem:
        """Find the most relevant unique image from the authentic catalog."""
        if not self.catalog.images:
            raise ValueError(
                "Authentic image catalog is empty; AI image generation is prohibited "
                "under Zero Fake AI Policy."
            )
        topic_lower = topic.lower()
        used_set = set(used_images or [])

        cat_matches = [img for img in self.catalog.images if img.category == category]
        candidates = cat_matches if cat_matches else self.catalog.images
        pool = self._filter_unused(candidates, used_set)
        return _first_tag_match(pool, topic_lower) or pool[0]

    def resolve_authentic_image(
        self,
        topic: str,
        category: str,
        candidate_path: str | None = None,
        used_images: set[str] | list[str] | None = None,
    ) -> ImageItem:
        """Return the catalog match for candidate_path or fall back to select_best_image."""
        if candidate_path and self.is_authentic_image(candidate_path):
            return self.validate_image_path(candidate_path)
        return self.select_best_image(topic, category, used_images=used_images)
