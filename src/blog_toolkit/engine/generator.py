"""End-to-end BlogGenerator orchestrating research, AI generation, and validation."""

from datetime import datetime

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.core.types import BlogPost
from blog_toolkit.engine.client import GeminiClient
from blog_toolkit.engine.prompts import build_system_prompt, build_user_prompt
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.images.catalog import ImageCatalog
from blog_toolkit.images.matcher import ImageMatcher


class BlogGenerator:
    """Orchestrates structured blog post generation using brand rules and Gemini."""

    def __init__(
        self,
        ruleset: BrandRuleset,
        catalog: ImageCatalog | None = None,
        client: GeminiClient | None = None,
    ):
        self.ruleset = ruleset
        self.catalog = catalog or ImageCatalog()
        self.matcher = ImageMatcher(self.catalog)
        self.client = client or GeminiClient()

    def generate(self, req: GenerationRequest) -> BlogPost:
        """Generate, validate, and return a bilingual BlogPost."""
        # 1. Select or validate cover image under Zero Fake AI Policy
        if req.image_override is not None:
            image_path = self.matcher.validate_image_path(req.image_override).path
        else:
            image_path = self.matcher.select_best_image(
                req.topic, req.category, used_images=req.used_images
            ).path

        # 2. Build prompts
        system_prompt = build_system_prompt(self.ruleset)
        user_prompt = build_user_prompt(req, self.ruleset, image_path)

        # 3. Call Gemini
        raw_dict = self.client.generate_post_json(system_prompt, user_prompt)

        # 4. Fill defaults and enforce canonical authentic cover image
        if "slug" not in raw_dict:
            raw_dict["slug"] = req.topic.lower().replace(" ", "-")
        raw_dict["date"] = req.target_date or datetime.now().strftime("%Y-%m-%d")
        if req.image_override is not None:
            raw_dict["image"] = image_path
        else:
            raw_image = raw_dict.get("image")
            raw_dict["image"] = self.matcher.resolve_authentic_image(
                req.topic,
                req.category,
                candidate_path=raw_image if isinstance(raw_image, str) else None,
                used_images=req.used_images,
            ).path
        if "author" not in raw_dict:
            raw_dict["author"] = self.ruleset.author_name
        if "category" not in raw_dict:
            raw_dict["category"] = req.category

        # 5. Parse into BlogPost
        post = BlogPost(**raw_dict)

        # 6. Audit against brand rules
        violations = self.ruleset.validate_post(post)
        if violations:
            violation_msg = "; ".join(violations)
            raise ValueError(f"Generated post violated brand ruleset: {violation_msg}")

        return post
