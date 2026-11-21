"""Tests for BlogGenerator."""

from unittest.mock import MagicMock

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.client import GeminiClient
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.types import GenerationRequest


def _sample_post_payload(
    *,
    slug: str,
    date: str,
    image: str,
    category: str,
    title_es: str,
    title_en: str,
    read_time_minutes: int = 5,
    featured: bool = True,
) -> dict:
    return {
        "slug": slug,
        "date": date,
        "read_time_minutes": read_time_minutes,
        "featured": featured,
        "author": "Equipo El Laundry",
        "image": image,
        "category": category,
        "es": {
            "title": title_es,
            "excerpt": "Descubre cómo ahorrar horas semanales con lavado profesional.",
            "keywords": ["lavado y doblado", "hialeah"],
            "key_takeaways": ["Mismo día antes de las 2 PM", "Precios desde $1.40/lb"],
            "sections": [
                {
                    "heading": "Ahorro de Tiempo",
                    "paragraphs": ["Nuestra familia lava, seca y dobla con esmero."],
                    "bullets": ["Doblado prolijo"],
                    "callout": "Estacionamiento gratis al frente.",
                }
            ],
            "category_label": "Lavado y Doblado",
        },
        "en": {
            "title": title_en,
            "excerpt": "Discover how to save hours every week with professional laundry care.",
            "keywords": ["wash and fold", "hialeah"],
            "key_takeaways": ["Same day before 2 PM", "Prices from $1.40/lb"],
            "sections": [
                {
                    "heading": "Time Savings",
                    "paragraphs": ["Our family washes, dries, and folds with care."],
                    "bullets": ["Neat folding"],
                    "callout": "Free parking right in front.",
                }
            ],
            "category_label": "Wash & Fold",
        },
    }


def test_generator_with_mock_client():
    ruleset = BrandRuleset.from_preset("el_laundry")
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.generate_post_json.return_value = _sample_post_payload(
        slug="guia-lavado-doblado-hialeah",
        date="2026-10-05",
        image="/images/blog/wash-and-fold-neat-stack.webp",
        category="wash-and-fold",
        title_es="Guía Completa de Lavado y Doblado en Hialeah",
        title_en="Complete Guide to Wash and Fold in Hialeah",
    )

    generator = BlogGenerator(ruleset=ruleset, client=mock_client)
    req = GenerationRequest(
        topic="Guía Completa de Lavado y Doblado",
        category="wash-and-fold",
        target_date="2026-10-05",
    )
    post = generator.generate(req)

    assert post.slug == "guia-lavado-doblado-hialeah"
    assert post.category == "wash-and-fold"
    assert post.read_time_minutes == 5
    assert len(post.es.sections) == 1
    assert post.word_count("es") > 10


def test_generator_overrides_hallucinated_gemini_image():
    ruleset = BrandRuleset.from_preset("el_laundry")
    mock_client = MagicMock(spec=GeminiClient)
    mock_client.generate_post_json.return_value = _sample_post_payload(
        slug="lavado-edredon-king-hialeah",
        date="2026-10-06",
        image="https://fake-ai.example/gen.png",
        category="comforters",
        title_es="Cómo Lavar Edredones King en Hialeah",
        title_en="How to Wash King Comforters in Hialeah",
        read_time_minutes=4,
        featured=False,
    )

    generator = BlogGenerator(ruleset=ruleset, client=mock_client)
    req = GenerationRequest(
        topic="Cómo Lavar Edredones King en Hialeah",
        category="comforters",
        target_date="2026-10-06",
        image_override=None,
    )
    post = generator.generate(req)

    assert post.image != "https://fake-ai.example/gen.png"
    assert post.image.startswith("/images/blog/")
    assert generator.matcher.is_authentic_image(post.image)
