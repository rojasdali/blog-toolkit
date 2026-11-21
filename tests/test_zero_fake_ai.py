"""Regression tests for Zero Fake AI Policy across ImageMatcher and BlogGenerator."""

from typing import Any
from unittest.mock import MagicMock

import pytest

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.client import GeminiClient
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.images.catalog import ImageCatalog
from blog_toolkit.images.matcher import ImageMatcher


def _base_post_dict(image: Any = None, *, include_image: bool = True) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "slug": "lavado-edredon-king-hialeah",
        "date": "2026-10-06",
        "read_time_minutes": 4,
        "featured": False,
        "author": "Equipo El Laundry",
        "category": "comforters",
        "es": {
            "title": "Cómo Lavar Edredones King en Hialeah",
            "excerpt": "Lava tu edredón en lavadoras industriales de 65 libras.",
            "keywords": ["lavar edredon king", "hialeah"],
            "key_takeaways": ["Lavadoras de 65 lbs", "Secado uniforme"],
            "sections": [{"heading": "Capacidad", "paragraphs": ["Espacio amplio."]}],
            "category_label": "Edredones",
        },
        "en": {
            "title": "How to Wash King Comforters in Hialeah",
            "excerpt": "Wash your King comforter in 65-pound commercial washers.",
            "keywords": ["wash king comforter", "hialeah"],
            "key_takeaways": ["65 lb commercial washers", "Even drying"],
            "sections": [{"heading": "Capacity", "paragraphs": ["Ample drum space."]}],
            "category_label": "Comforters",
        },
    }
    if include_image:
        payload["image"] = image
    return payload


def test_matcher_non_string_guards():
    matcher = ImageMatcher(ImageCatalog())
    bad_none: Any = None
    assert matcher.is_authentic_image(bad_none) is False
    assert matcher.is_authentic_image(123) is False  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Zero Fake AI Policy"):
        matcher.validate_image_path(bad_none)


def test_resolve_authentic_image_edge_cases():
    catalog = ImageCatalog()
    matcher = ImageMatcher(catalog)
    padded_valid = "  /images/blog/stain-removal-guide.webp  "
    assert matcher.resolve_authentic_image("Manchas", "care-guides", padded_valid).path == (
        "/images/blog/stain-removal-guide.webp"
    )

    commercial_imgs = [img.path for img in catalog.images if img.category == "commercial"]
    for candidate in (None, "", "   ", "https://fake-ai.example/gen.png"):
        resolved = matcher.resolve_authentic_image(
            "Servicio comercial",
            "commercial",
            candidate_path=candidate,
            used_images={commercial_imgs[0]},
        )
        assert resolved in catalog.images
        assert resolved.path != commercial_imgs[0]


def test_generator_strips_whitespace_padded_authentic_image():
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.generate_post_json.return_value = _base_post_dict(
        "  /images/blog/washers-commercial-electrolux.webp  "
    )
    gen = BlogGenerator(BrandRuleset.from_preset("el_laundry"), client=mock_client)
    post = gen.generate(GenerationRequest(topic="Edredones", category="comforters"))
    assert post.image == "/images/blog/washers-commercial-electrolux.webp"


def test_generator_handles_none_and_missing_gemini_image():
    mock_client = MagicMock(spec=GeminiClient)
    gen = BlogGenerator(BrandRuleset.from_preset("el_laundry"), client=mock_client)
    for payload in (_base_post_dict(None), _base_post_dict(include_image=False)):
        mock_client.generate_post_json.return_value = payload
        post = gen.generate(GenerationRequest(topic="Edredones", category="comforters"))
        assert gen.matcher.is_authentic_image(post.image)


def test_generator_image_override_validates_and_normalizes():
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.generate_post_json.return_value = _base_post_dict(
        "/images/blog/wash-and-fold-neat-stack.webp"
    )
    gen = BlogGenerator(BrandRuleset.from_preset("el_laundry"), client=mock_client)
    bad_overrides = ("https://oaidalleapiprodscus.blob.core.windows.net/fake.png", "   ", "")
    for bad_override in bad_overrides:
        req = GenerationRequest(topic="Edredones", category="comforters", image_override=bad_override)
        with pytest.raises(ValueError, match="Zero Fake AI Policy"):
            gen.generate(req)
    mock_client.generate_post_json.assert_not_called()

    valid_req = GenerationRequest(
        topic="Edredones",
        category="comforters",
        image_override="  /images/blog/stain-removal-guide.webp  ",
    )
    assert gen.generate(valid_req).image == "/images/blog/stain-removal-guide.webp"
