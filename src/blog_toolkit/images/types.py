"""Image catalog domain types."""

from pydantic import BaseModel, Field, field_validator


class ImageItem(BaseModel):
    """Cataloged image asset for blog posts."""

    path: str = Field(description="Relative path or URL to the image")
    alt_es: str = Field(description="Descriptive alt text in Spanish")
    alt_en: str = Field(description="Descriptive alt text in English")
    tags: list[str] = Field(default_factory=list, description="Keywords and tags")
    category: str | None = Field(default=None, description="Preferred category slug")

    @field_validator("path")
    @classmethod
    def _validate_non_empty_path(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("ImageItem path must be non-empty under Zero Fake AI Policy.")
        return cleaned
