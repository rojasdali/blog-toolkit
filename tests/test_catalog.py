"""Tests for ImageCatalog and ImageMatcher under Zero Fake AI Policy."""

import pytest

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


def test_no_ai_image_prompt_method():
    assert not hasattr(ImageMatcher, "generate_ai_image_prompt")
    ai_attrs = [
        attr
        for attr in dir(ImageMatcher)
        if "ai_image_prompt" in attr.lower() or "generate_ai_" in attr.lower()
    ]
    assert ai_attrs == []


def test_matcher_rejects_empty_catalog():
    empty_catalog = ImageCatalog(images=[])
    assert empty_catalog.images == []
    matcher = ImageMatcher(empty_catalog)

    with pytest.raises(ValueError, match="Zero Fake AI Policy"):
        matcher.select_best_image(topic="Lavado de ropa", category="wash-and-fold")


def test_matcher_validates_authentic_images():
    catalog = ImageCatalog()
    matcher = ImageMatcher(catalog)
    valid_path = catalog.images[0].path

    assert matcher.is_authentic_image(valid_path) is True
    assert matcher.is_authentic_image(f"  {valid_path}  ") is True
    assert matcher.validate_image_path(valid_path) == catalog.images[0]

    for fake_path in [
        "",
        "   ",
        "https://fake-ai.example/gen.png",
        "/images/blog/ai-generated-fantasy.webp",
    ]:
        assert matcher.is_authentic_image(fake_path) is False
        with pytest.raises(ValueError, match="Zero Fake AI Policy"):
            matcher.validate_image_path(fake_path)


def test_matcher_authentic_catalog_only_for_uncataloged_topic():
    catalog = ImageCatalog()
    matcher = ImageMatcher(catalog)

    img = matcher.select_best_image(
        topic="Cómo impermeabilizar chaquetas de montaña",
        category="unknown-category",
    )
    assert img in catalog.images
    assert img.path.startswith("/images/blog/")
    assert img.path.endswith(".webp")
    assert img.alt_es.strip()
    assert img.alt_en.strip()


def test_matcher_avoids_used_images_and_falls_back():
    catalog = ImageCatalog()
    matcher = ImageMatcher(catalog)
    commercial_images = [img for img in catalog.images if img.category == "commercial"]
    assert len(commercial_images) >= 2

    first_pick = matcher.select_best_image(
        topic="Servicio comercial de lavandería",
        category="commercial",
        used_images={commercial_images[0].path},
    )
    assert first_pick.path != commercial_images[0].path
    assert first_pick in commercial_images

    all_used = {img.path for img in commercial_images}
    fallback_pick = matcher.select_best_image(
        topic="Servicio comercial de lavandería",
        category="commercial",
        used_images=all_used,
    )
    assert fallback_pick in commercial_images


def test_default_catalog_entries_valid_paths_and_alt_text():
    catalog = ImageCatalog()
    paths = [img.path for img in catalog.images]
    assert len(paths) == len(set(paths))
    for img in catalog.images:
        assert img.path.startswith("/images/blog/")
        assert img.path.endswith(".webp")
        assert img.alt_es.strip()
        assert img.alt_en.strip()
        assert len(img.tags) > 0
