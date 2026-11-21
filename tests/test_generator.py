"""Tests for BlogGenerator."""

from unittest.mock import MagicMock

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.client import GeminiClient
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.types import GenerationRequest


def test_generator_with_mock_client():
    ruleset = BrandRuleset.from_preset("el_laundry")
    mock_client = MagicMock(spec=GeminiClient)

    mock_client.generate_post_json.return_value = {
        "slug": "guia-lavado-doblado-hialeah",
        "date": "2026-10-05",
        "read_time_minutes": 5,
        "featured": True,
        "author": "Equipo El Laundry",
        "image": "/images/blog/wash-and-fold-neat-stack.webp",
        "category": "wash-and-fold",
        "es": {
            "title": "Guía Completa de Lavado y Doblado en Hialeah",
            "excerpt": "Descubre cómo ahorrar horas semanales dejando tu ropa en manos de profesionales.",
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
            "title": "Complete Guide to Wash and Fold in Hialeah",
            "excerpt": "Discover how to save hours every week by letting professionals handle your laundry.",
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

    mock_client.generate_post_json.return_value = {
        "slug": "lavado-edredon-king-hialeah",
        "date": "2026-10-06",
        "read_time_minutes": 4,
        "featured": False,
        "author": "Equipo El Laundry",
        "image": "https://fake-ai.example/gen.png",
        "category": "comforters",
        "es": {
            "title": "Cómo Lavar Edredones King en Hialeah",
            "excerpt": "Lava tu edredón King en nuestras lavadoras industriales de 65 libras.",
            "keywords": ["lavar edredon king", "hialeah"],
            "key_takeaways": ["Lavadoras de 65 lbs", "Secado uniforme"],
            "sections": [
                {
                    "heading": "Capacidad Industrial",
                    "paragraphs": ["Espacio amplio para un lavado profundo y sin daños."],
                    "bullets": ["Ciclo suave disponible"],
                    "callout": "Visítanos en Sedano's Plaza.",
                }
            ],
            "category_label": "Edredones",
        },
        "en": {
            "title": "How to Wash King Comforters in Hialeah",
            "excerpt": "Wash your King comforter in our 65-pound commercial washers.",
            "keywords": ["wash king comforter", "hialeah"],
            "key_takeaways": ["65 lb commercial washers", "Even drying"],
            "sections": [
                {
                    "heading": "Commercial Capacity",
                    "paragraphs": ["Ample drum space for deep cleaning without damage."],
                    "bullets": ["Gentle cycle available"],
                    "callout": "Visit us at Sedano's Plaza.",
                }
            ],
            "category_label": "Comforters",
        },
    }

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
