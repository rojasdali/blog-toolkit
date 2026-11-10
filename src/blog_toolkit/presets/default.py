"""Generic agnostic default preset for BrandProfile."""

from typing import Any

from blog_toolkit.core.ruleset import BrandProfile

DEFAULT_DATA: dict[str, Any] = {
    "brand_name": "Modern Brand",
    "tagline": "Premium Quality Services & Reliable Solutions",
    "brand_voice": "Professional, authoritative, helpful, and concise.",
    "target_audience": "Local customers and commercial clients seeking high-quality reliable service.",
    "location_context": {
        "address": "123 Main Street",
        "city": "Miami",
        "state": "FL",
        "zip": "33101",
        "landmark": "Downtown Center",
        "parking": "Dedicated customer parking",
        "phone": "(305) 555-0100",
        "hours": "Mon-Sat 9AM-6PM",
        "neighborhoods_served": ["Miami", "Downtown", "Brickell"],
    },
    "services": [
        "Core Service Package",
        "Express Turnaround",
        "Commercial & Bulk Accounts",
    ],
    "key_differentiators": [
        "State-of-the-art technology",
        "Experienced and dedicated team",
        "Transparent upfront pricing",
    ],
    "pricing_facts": ["Transparent flat and volume rates published upfront"],
    "cutoff_time": "Same-day service for orders placed before 12:00 PM",
    "forbidden_terms": ["cheap quality", "unreliable", "hidden fees"],
    "primary_language": "en",
    "target_languages": ["en", "es"],
    "author_name": "Editorial Team",
    "categories": [
        {"slug": "guides", "label_es": "Guías", "label_en": "Guides"},
        {"slug": "tips", "label_es": "Consejos", "label_en": "Tips"},
        {"slug": "industry", "label_es": "Industria", "label_en": "Industry"},
    ],
    "posts_per_week": 1.0,
}


def get_default_profile() -> BrandProfile:
    """Instantiate generic default BrandProfile."""
    return BrandProfile(**DEFAULT_DATA)
