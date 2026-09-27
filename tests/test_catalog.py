"""Tests for ImageCatalog and ImageMatcher."""

from blog_toolkit.images.catalog import ImageCatalog
from blog_toolkit.images.matcher import ImageMatcher


def test_default_catalog_loads():
    catalog = ImageCatalog()
    assert len(catalog.images) >= 4


def test_matcher_selects_by_category():
    catalog = ImageCatalog()
    matcher = ImageMatcher(catalog)

    img = matcher.select_best_image(
        topic="Lavado de edredones gigantes",
        category="comforters",
    )
    assert "comforter" in img.path or "washers" in img.path


def test_ai_prompt_generation():
    catalog = ImageCatalog()
    matcher = ImageMatcher(catalog)

    prompt = matcher.generate_ai_image_prompt(
        topic="Toallas plegadas para spa",
        category="commercial",
        brand_name="El Laundry",
    )
    assert "El Laundry" in prompt
    assert "Toallas plegadas para spa" in prompt
    assert "Electrolux" in prompt
