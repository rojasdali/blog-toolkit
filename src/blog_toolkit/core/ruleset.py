"""Brand profile / ruleset definitions and preset loading for blog generation."""

import json
from pathlib import Path

from pydantic import BaseModel, Field, model_validator

from blog_toolkit.core.types import BlogPost


class CategoryItem(BaseModel):
    """Category taxonomy item."""

    slug: str
    label_es: str
    label_en: str


class BrandRuleset(BaseModel):
    """Configurable brand voice, pricing facts, cutoff policies, and editorial guardrails."""

    brand_name: str
    tagline: str = ""
    brand_voice: str
    target_audience: str
    location_context: dict[str, str | list[str]] = Field(default_factory=dict)
    services: list[str] = Field(default_factory=list)
    key_differentiators: list[str] = Field(default_factory=list)
    forbidden_terms: list[str] = Field(default_factory=list)
    forbidden_phrases: list[str] = Field(default_factory=list)
    pricing_facts: list[str] = Field(default_factory=list)
    cutoff_time: str = ""
    primary_language: str = "es"
    target_languages: list[str] = Field(default_factory=lambda: ["es", "en"])
    author_name: str = "Editorial Team"
    categories: list[CategoryItem] = Field(default_factory=list)
    posts_per_week: float = 1.5
    visual_identity_inspo: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _sync_forbidden_lists(self) -> "BrandRuleset":
        merged: list[str] = []
        seen: set[str] = set()
        for term in [*self.forbidden_terms, *self.forbidden_phrases]:
            key = term.strip().lower()
            if key and key not in seen:
                merged.append(term.strip())
                seen.add(key)
        self.forbidden_terms = list(merged)
        self.forbidden_phrases = list(merged)
        return self

    def effective_forbidden_terms(self) -> list[str]:
        """Return deduplicated union of forbidden terms and phrases."""
        return list(self.forbidden_terms)

    @classmethod
    def from_file(cls, path: str | Path) -> "BrandRuleset":
        """Load brand profile from a JSON file."""
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Ruleset file not found: {file_path}")
        with open(file_path, encoding="utf-8") as f:
            return cls(**json.load(f))

    @classmethod
    def from_preset(cls, preset_name: str) -> "BrandRuleset":
        """Load a built-in brand preset from Python module or packaged JSON."""
        from blog_toolkit.presets import get_preset_data

        data = get_preset_data(preset_name)
        return cls(**data)

    def validate_post(self, post: BlogPost, strict_aeo: bool = False) -> list[str]:
        """Audit a generated post against brand profile rules and forbidden terms."""
        from blog_toolkit.engine.validator import validate_post_content

        return validate_post_content(post, self, strict_aeo=strict_aeo)


BrandProfile = BrandRuleset
