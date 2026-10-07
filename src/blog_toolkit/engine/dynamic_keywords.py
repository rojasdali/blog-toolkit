"""Dynamic keyword ingestion and striking-distance topic formulator."""

import re

from blog_toolkit.engine.deduplicator import ContentDeduplicator
from blog_toolkit.engine.types import ExistingPostSummary, PlannedTopic, StrikingKeyword

INTENT_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"comfor|edred|manta|blanket", re.I), "comforters"),
    (re.compile(r"commer|negoc|airbnb|uniform|restaur", re.I), "commercial"),
    (re.compile(r"wash\s*(&|and)?\s*fold|fluff|drop\s*off|libra|doblado", re.I), "wash-and-fold"),
    (re.compile(r"coin|moneda|auto|self", re.I), "self-service"),
]


def detect_category(query: str) -> str:
    """Classify search query into a relevant content category."""
    for pattern, cat in INTENT_MAP:
        if pattern.search(query):
            return cat
    return "self-service"


def formulate_slug(query: str) -> str:
    """Create a clean hyphenated URL slug from search query."""
    clean = re.sub(r"[^a-zA-Z0-9\s-]", "", query.lower())
    slug = re.sub(r"[\s_]+", "-", clean).strip("-")
    if not any(geo in slug for geo in ["hialeah", "miami", "medley"]):
        slug = f"{slug}-hialeah"
    return slug[:60]


def formulate_topic(query: str, category: str) -> str:
    """Formulate an engaging Spanish title for the target query."""
    q_lower = query.lower()
    if "coin" in q_lower or "moneda" in q_lower:
        return "Lavandería con Monedas en Hialeah: Autoservicio Rápido y Lavadoras Gigantes"
    if "fluff" in q_lower or "drop off" in q_lower:
        return f"Servicio Drop-Off en Hialeah: {query.title()} y Lavado por Libra"
    if "commercial" in q_lower or "comercial" in q_lower:
        return f"Lavandería Comercial en Hialeah: Servicio para Negocios y {query.title()}"
    return f"Guía de Lavandería en Hialeah: {query.title()} en Plaza de Sedano's"


def pick_striking_topic(
    keywords: list[StrikingKeyword],
    existing: list[ExistingPostSummary],
    target_date: str,
) -> PlannedTopic | None:
    """Find the highest-opportunity striking keyword that does not duplicate existing posts."""
    dedup = ContentDeduplicator(existing)
    candidates = [k for k in keywords if 8.0 <= k.position <= 25.0 and k.impressions >= 3]
    sorted_kw = sorted(candidates, key=lambda k: k.impressions, reverse=True)

    for item in sorted_kw:
        cat = detect_category(item.query)
        slug = formulate_slug(item.query)
        topic = formulate_topic(item.query, cat)
        target_kws = [item.query, f"{item.query} hialeah", "lavanderia sedanos hialeah"]

        is_dup, _, _ = dedup.is_duplicate(topic, target_kws, slug)
        if not is_dup:
            return PlannedTopic(
                topic=topic,
                slug=slug,
                category=cat,
                target_keywords=target_kws,
                target_date=target_date,
                rationale=f"GSC Striking Distance: #{item.position:.1f} with {item.impressions} impressions",
            )
    return None
