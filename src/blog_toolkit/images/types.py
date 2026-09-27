"""Image catalog domain types."""

from pydantic import BaseModel, Field


class ImageItem(BaseModel):
    """Cataloged image asset for blog posts."""

    path: str = Field(description="Relative path or URL to the image")
    alt_es: str = Field(description="Descriptive alt text in Spanish")
    alt_en: str = Field(description="Descriptive alt text in English")
    tags: list[str] = Field(default_factory=list, description="Keywords and tags")
    category: str | None = Field(default=None, description="Preferred category slug")
