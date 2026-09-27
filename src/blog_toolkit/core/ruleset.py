"""Brand ruleset definitions and validation for blog generation."""

import json
from pathlib import Path

from pydantic import BaseModel, Field

from blog_toolkit.core.types import BlogPost


class CategoryItem(BaseModel):
    """Category taxonomy item."""

    slug: str
    label_es: str
    label_en: str


class BrandRuleset(BaseModel):
    """Configurable brand voice, geographic context, and editorial rules."""

    brand_name: str
    tagline: str = ""
    brand_voice: str
    target_audience: str
    location_context: dict[str, str | list[str]] = Field(default_factory=dict)
    services: list[str] = Field(default_factory=list)
    key_differentiators: list[str] = Field(default_factory=list)
    forbidden_phrases: list[str] = Field(default_factory=list)
    primary_language: str = "es"
    target_languages: list[str] = Field(default_factory=lambda: ["es", "en"])
    author_name: str = "Editorial Team"
    categories: list[CategoryItem] = Field(default_factory=list)
    posts_per_week: float = 1.5

    @classmethod
    def from_file(cls, path: str | Path) -> "BrandRuleset":
        """Load brand ruleset from a JSON file."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Ruleset file not found: {file_path}")
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    @classmethod
    def from_preset(cls, preset_name: str) -> "BrandRuleset":
        """Load a built-in brand preset by name."""
        base_dir = Path(__file__).resolve().parent.parent.parent.parent / "presets"
        preset_file = base_dir / f"{preset_name}.json"
        if not preset_file.exists():
            raise FileNotFoundError(f"Preset '{preset_name}' not found at {preset_file}")
        return cls.from_file(preset_file)

    def validate_post(self, post: BlogPost) -> list[str]:
        """Audit a generated post against brand rules and forbidden phrases."""
        violations: list[str] = []
        raw_text = (
            f"{post.es.title} {post.es.excerpt} {post.en.title} {post.en.excerpt} "
            f"{' '.join([s.heading + ' ' + ' '.join(s.paragraphs) for s in post.es.sections])} "
            f"{' '.join([s.heading + ' ' + ' '.join(s.paragraphs) for s in post.en.sections])}"
        ).lower()

        for forbidden in self.forbidden_phrases:
            if forbidden.lower() in raw_text:
                violations.append(f"Forbidden phrase detected: '{forbidden}'")

        valid_slugs = [c.slug for c in self.categories]
        if valid_slugs and post.category not in valid_slugs:
            violations.append(f"Unknown category '{post.category}'. Expected one of {valid_slugs}")

        return violations
