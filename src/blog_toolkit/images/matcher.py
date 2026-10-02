"""Image matching logic and AI prompt generator for uncataloged topics."""

from blog_toolkit.images.catalog import ImageCatalog
from blog_toolkit.images.types import ImageItem


class ImageMatcher:
    """Matches post topics to real brand photography or generates AI prompts."""

    def __init__(self, catalog: ImageCatalog):
        self.catalog = catalog

    def select_best_image(self, topic: str, category: str) -> ImageItem:
        """Find the most relevant image from the catalog."""
        topic_lower = topic.lower()

        # 1. Exact category match
        cat_matches = [img for img in self.catalog.images if img.category == category]
        for img in cat_matches:
            for tag in img.tags:
                if tag.lower() in topic_lower:
                    return img
        if cat_matches:
            return cat_matches[0]

        # 2. Tag keyword matching
        for img in self.catalog.images:
            for tag in img.tags:
                if tag.lower() in topic_lower:
                    return img

        # 3. Fallback to first image
        return self.catalog.images[0]

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
