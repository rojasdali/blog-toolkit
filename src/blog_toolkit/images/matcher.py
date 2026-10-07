"""Image matching logic and AI prompt generator for uncataloged topics."""

from blog_toolkit.images.catalog import ImageCatalog
from blog_toolkit.images.types import ImageItem


class ImageMatcher:
    """Matches post topics to real brand photography or generates AI prompts."""

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

    def select_best_image(
        self,
        topic: str,
        category: str,
        used_images: set[str] | list[str] | None = None,
    ) -> ImageItem:
        """Find the most relevant unique image from the catalog."""
        topic_lower = topic.lower()
        used_set = set(used_images or [])

        cat_matches = [img for img in self.catalog.images if img.category == category]
        pool = self._filter_unused(cat_matches, used_set) if cat_matches else self.catalog.images

        for img in pool:
            for tag in img.tags:
                if tag.lower() in topic_lower:
                    return img
        if pool:
            return pool[0]

        all_pool = self._filter_unused(self.catalog.images, used_set)
        for img in all_pool:
            for tag in img.tags:
                if tag.lower() in topic_lower:
                    return img

        return all_pool[0] if all_pool else self.catalog.images[0]

    def generate_ai_image_prompt(
        self,
        topic: str,
        category: str,
        brand_name: str,
        visual_inspo: dict[str, str] | None = None,
    ) -> str:
        """Generate high-converting prompt for AI image generators if needed."""
        inspo = visual_inspo or {}
        equipment = inspo.get(
            "equipment",
            "High-end Electrolux commercial washers and dryers in the background"
            if "laundry" in brand_name.lower()
            else "modern professional commercial equipment in the background",
        )
        return (
            f"Hyper-realistic editorial photo for '{brand_name}'. "
            f"Scene: {topic}. {equipment}, "
            f"warm natural lighting, sparkling clean interior, 8k resolution, documentary photography style, "
            f"shot on Sony A7R V 35mm f/1.8, vibrant natural colors, authentic and inviting atmosphere."
        )
