"""Tests for BrandRuleset loading and validation."""

import pytest

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.core.types import BlogPost, BlogSection, PostLocaleContent


@pytest.fixture
def el_laundry_ruleset() -> BrandRuleset:
    return BrandRuleset.from_preset("el_laundry")


@pytest.fixture
def valid_post() -> BlogPost:
    return BlogPost(
        slug="como-lavar-edredones-king",
        date="2026-10-01",
        read_time_minutes=4,
        featured=True,
        author="Equipo El Laundry",
        image="/images/blog/washers-commercial-electrolux.webp",
        category="comforters",
        es=PostLocaleContent(
            title="Cómo Lavar un Edredón King en Lavadoras Gigantes",
            excerpt="Aprende a lavar tu edredón king sin maltratar las plumas ni quemar el motor.",
            keywords=["edredon king", "lavadoras gigantes"],
            key_takeaways=["Usa lavadoras de 65 lbs", "No uses calor excesivo"],
            sections=[
                BlogSection(
                    heading="Por qué el tamaño de la máquina importa",
                    paragraphs=["Las lavadoras residenciales no tienen suficiente espacio."],
                    bullets=["Capacidad adecuada", "Centrifugado potente"],
                    callout="Usa siempre jabón suave.",
                )
            ],
            category_label="Edredones",
        ),
        en=PostLocaleContent(
            title="How to Wash a King Size Comforter in Giant Washers",
            excerpt="Learn how to wash your king comforter safely in high-capacity washers.",
            keywords=["king comforter", "giant washers"],
            key_takeaways=["Use 65lb washers", "Avoid excessive heat"],
            sections=[
                BlogSection(
                    heading="Why machine capacity matters",
                    paragraphs=["Home washers lack the drum volume needed."],
                    bullets=["Proper drum volume", "Fast extraction"],
                    callout="Always use mild detergent.",
                )
            ],
            category_label="Comforters",
        ),
    )


def test_load_presets(el_laundry_ruleset: BrandRuleset):
    assert el_laundry_ruleset.brand_name == "El Laundry"
    assert el_laundry_ruleset.primary_language == "es"
    assert len(el_laundry_ruleset.categories) >= 5
    assert "laundry mat" in el_laundry_ruleset.forbidden_phrases


def test_validate_clean_post(el_laundry_ruleset: BrandRuleset, valid_post: BlogPost):
    violations = el_laundry_ruleset.validate_post(valid_post)
    assert violations == []


def test_validate_forbidden_phrase(el_laundry_ruleset: BrandRuleset, valid_post: BlogPost):
    valid_post.es.title = "Visit our cheap laundry mat today"
    violations = el_laundry_ruleset.validate_post(valid_post)
    assert any("Forbidden phrase detected: 'laundry mat'" in v for v in violations)


def test_validate_invalid_category(el_laundry_ruleset: BrandRuleset, valid_post: BlogPost):
    valid_post.category = "non-existent-category"
    violations = el_laundry_ruleset.validate_post(valid_post)
    assert any("Unknown category" in v for v in violations)
