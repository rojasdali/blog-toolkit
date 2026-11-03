"""Tests for ContentDeduplicator semantic cannibalization defense."""

from blog_toolkit.core.types import BlogPost, BlogSection, PostLocaleContent
from blog_toolkit.engine.deduplicator import (
    ContentDeduplicator,
    jaccard_similarity,
    normalize_tokens,
    sanitize_post_keywords,
)
from blog_toolkit.engine.types import ExistingPostSummary


def test_token_normalization_and_similarity():
    t1 = normalize_tokens("Cuánto Tiempo Realmente Ahorras con el Servicio de Lavado y Doblado en Hialeah")
    t2 = normalize_tokens("Guía de Lavado y Doblado en Hialeah: Cuánto Tiempo Realmente Ahorras")

    sim = jaccard_similarity(t1, t2)
    assert sim >= 0.70


def test_deduplicator_catches_semantic_duplicates():
    existing = [
        ExistingPostSummary(
            slug="cuanto-tiempo-ahorras-lavado-doblado-hialeah",
            titles=["Cuánto Tiempo Realmente Ahorras con el Servicio de Lavado y Doblado en Hialeah"],
            keywords=["cuanto tiempo ahorras lavado y doblado", "wash and fold hialeah fl"],
        )
    ]
    dedup = ContentDeduplicator(existing)

    # Near-identical topic
    is_dup, reason, matched = dedup.is_duplicate(
        topic="Guía de Lavado y Doblado en Hialeah: Cuánto Tiempo Realmente Ahorras",
        keywords=["lavado y doblado hialeah", "wash and fold fl"],
        slug="guia-lavado-doblado-ahorro-tiempo",
    )
    assert is_dup is True
    assert "Title similarity" in reason
    assert matched == "cuanto-tiempo-ahorras-lavado-doblado-hialeah"


def test_deduplicator_allows_unique_topics():
    existing = [
        ExistingPostSummary(
            slug="cuanto-tiempo-ahorras-lavado-doblado-hialeah",
            titles=["Cuánto Tiempo Realmente Ahorras con el Servicio de Lavado y Doblado en Hialeah"],
            keywords=["cuanto tiempo ahorras lavado y doblado", "wash and fold hialeah fl"],
        )
    ]
    dedup = ContentDeduplicator(existing)

    # Completely different topic
    is_dup, reason, matched = dedup.is_duplicate(
        topic="Las 5 Mejores Lavadoras para Edredones en Hialeah",
        keywords=["lavar edredón hialeah", "lavadoras grandes 60 lbs"],
        slug="mejores-lavadoras-edredones-hialeah",
    )
    assert is_dup is False
    assert matched is None


def test_sanitize_post_keywords_strips_cannibalized_primary_keywords():
    existing = [
        ExistingPostSummary(
            slug="donde-lavar-ropa-cerca-de-mi-hialeah",
            titles=["Dónde Lavar Ropa Cerca de Mí en Hialeah"],
            keywords=["closest laundromat near me", "coin laundromat near me"],
        )
    ]
    sec = BlogSection(heading="H1 text here", paragraphs=["Paragraph content here for testing."])
    post = BlogPost(
        slug="lavanderia-de-monedas-palm-springs-north",
        date="2026-11-03",
        read_time_minutes=4,
        featured=False,
        author="El Laundry Team",
        image="/images/blog/speed-queen-row.jpg",
        category="self-service",
        es=PostLocaleContent(
            slug="lavanderia-de-monedas-palm-springs-north",
            title="Lavandería de Monedas en Palm Springs North",
            excerpt="Guía completa de lavandería de monedas para residentes de Palm Springs North.",
            keywords=["lavandería de monedas palm springs north", "lavadoras grandes palm springs"],
            key_takeaways=["Point 1", "Point 2", "Point 3"],
            sections=[sec, sec, sec],
            category_label="Autoservicio",
        ),
        en=PostLocaleContent(
            slug="coin-laundromat-palm-springs-north",
            title="Coin Laundromat Near Palm Springs North",
            excerpt="Complete self-service coin laundromat guide for Palm Springs North residents.",
            keywords=["coin laundromat near me", "coin laundromat palm springs north", "palm springs north laundry"],
            key_takeaways=["Point 1", "Point 2", "Point 3"],
            sections=[sec, sec, sec],
            category_label="Self-Service",
        ),
    )

    sanitized = sanitize_post_keywords(post, existing)
    assert "coin laundromat near me" not in sanitized.en.keywords
    assert sanitized.en.keywords[0] == "coin laundromat palm springs north"
    assert len(sanitized.en.keywords) >= 3
