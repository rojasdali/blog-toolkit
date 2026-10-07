"""Tests for dynamic striking keywords formulation and category detection."""

from blog_toolkit.engine.dynamic_keywords import (
    detect_category,
    formulate_slug,
    formulate_topic,
    pick_striking_topic,
)
from blog_toolkit.engine.types import ExistingPostSummary, StrikingKeyword


def test_detect_category_mapping():
    assert detect_category("coin laundry near me") == "self-service"
    assert detect_category("lavado y doblado por libra") == "wash-and-fold"
    assert detect_category("drop off laundry miami") == "wash-and-fold"
    assert detect_category("commercial linen cleaning medley") == "commercial"
    assert detect_category("king size comforter washer") == "comforters"


def test_formulate_slug():
    slug = formulate_slug("drop off laundry service miami lakes")
    assert "drop-off-laundry-service-miami-lakes" in slug
    assert " " not in slug


def test_formulate_topic():
    t1 = formulate_topic("coin laundry near me", "self-service")
    assert "Monedas" in t1
    t2 = formulate_topic("commercial linen cleaning", "commercial")
    assert "Comercial" in t2


def test_pick_striking_topic_skips_covered_and_picks_untapped():
    existing = [
        ExistingPostSummary(
            slug="servicio-lavanderia-comercial-hialeah-b2b",
            titles=["Servicio de Lavandería Comercial en Hialeah: Soluciones B2B"],
            keywords=["commercial laundry service hialeah"],
        )
    ]
    keywords = [
        # Already covered
        StrikingKeyword(query="commercial laundry service hialeah", position=11.2, impressions=18),
        # Untapped opportunity
        StrikingKeyword(query="drop off laundry service miami lakes", position=14.0, impressions=12),
    ]

    picked = pick_striking_topic(keywords, existing, "2026-10-10")
    assert picked is not None
    assert "drop-off" in picked.slug
    assert picked.category == "wash-and-fold"
    assert "miami-lakes" in picked.slug
