"""Tests for ContentDeduplicator semantic cannibalization defense."""

from blog_toolkit.engine.deduplicator import (
    ContentDeduplicator,
    jaccard_similarity,
    normalize_tokens,
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
