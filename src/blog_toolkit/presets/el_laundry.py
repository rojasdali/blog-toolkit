"""El Laundry canonical preset populating BrandProfile fields."""

from typing import Any

from blog_toolkit.core.ruleset import BrandProfile

EL_LAUNDRY_DATA: dict[str, Any] = {
    "brand_name": "El Laundry",
    "tagline": "Lavandería Moderna en Hialeah · Monedas y Lavado y Doblado",
    "brand_voice": (
        "Cálido, experto, servicial, 100% familiar y honesto. Enfoque en la comunidad trabajadora "
        "de Hialeah, combinando maquinaria comercial Electrolux moderna con atención humana en tienda."
    ),
    "target_audience": (
        "Familias locales, profesionales ocupados, anfitriones de Airbnb, negocios y restaurantes de "
        "Hialeah que buscan ahorrar tiempo o lavar prendas gigantes con total confianza."
    ),
    "location_context": {
        "address": "2357 W 52nd St",
        "city": "Hialeah",
        "state": "FL",
        "zip": "33016",
        "landmark": "Plaza de Sedano's (Sedano's Plaza frente al estacionamiento)",
        "parking": "Estacionamiento amplio y gratuito justo al frente (150+ espacios)",
        "phone": "(786) 803-8622",
        "hours": "Lun-Vie 8AM-9PM · Sáb-Dom 7AM-9PM (Último lavado 8:00 PM)",
        "neighborhoods_served": [
            "Hialeah",
            "West Hialeah",
            "Miami Lakes",
            "Hialeah Gardens",
            "Palm Springs Mile",
        ],
    },
    "services": [
        "Lavado y Doblado (Wash & Fold) el mismo día dejando antes de las 2:00 PM ($1.00/lb Mar-Jue Especial de Mitad de Semana, $1.40/lb Lunes, $1.75/lb Vie-Dom; mínimo 15 lbs)",
        "Lavadoras Gigantes Electrolux de hasta 65 lbs para edredones King/Queen y cobijas pesadas ($9-$20 en drop-off; $4.00-$8.50 en autoservicio)",
        "Servicio Comercial de Lavandería B2B para Airbnb, peluquerías, spas, clínicas médicas, restaurantes y uniformes industriales",
        "Lavandería de Monedas (Autoservicio) moderna, rápida y con aire acondicionado (secadoras a $0.25 por 5-10 min)",
    ],
    "key_differentiators": [
        "Negocio familiar 100% local con personal siempre presente en tienda para ayudar",
        "Lavadoras de alta velocidad que exprimen mejor y secadoras dobles que secan en la mitad del tiempo",
        "Ambiente impecable, seguro, bien iluminado y con aire acondicionado potente",
        "Atención bilingüe con trato de familia",
    ],
    "pricing_facts": [
        "Wash & Fold Drop-Off: $1.00/lb Martes a Jueves (Midweek Special), $1.40/lb Lunes, $1.75/lb Viernes a Domingo (mínimo 15 lbs)",
        "Edredones / Comforters Drop-Off: $9–$20 tarifa plana según tamaño (Twin/Full/Queen/King)",
        "Autoservicio Lavadoras Gigantes 65 lbs (20 kg): $4.00–$8.50 por ciclo; Secadoras: $0.25 por 5–10 min",
    ],
    "cutoff_time": "2:00 PM para entrega el mismo día en Wash & Fold; Último lavado (Last Wash) 8:00 PM todos los días (cierre 9:00 PM)",
    "forbidden_terms": [
        "laundry mat",
        "tienda desatendida",
        "sin personal",
        "máquinas rotas",
        "precios ocultos",
        "planchado",
        "wi-fi",
        "wifi",
        "80 lbs",
        "$1.40/lb Lun-Jue",
        "$1.40/lb Mon-Thu",
        "24 horas",
        "open 24 hours",
    ],
    "primary_language": "es",
    "target_languages": ["es", "en"],
    "author_name": "Equipo El Laundry",
    "categories": [
        {"slug": "wash-and-fold", "label_es": "Lavado y Doblado", "label_en": "Wash & Fold"},
        {
            "slug": "comforters",
            "label_es": "Edredones y Ropa Pesada",
            "label_en": "Comforters & Heavy Items",
        },
        {
            "slug": "self-service",
            "label_es": "Lavandería de Monedas",
            "label_en": "Coin Laundromat",
        },
        {"slug": "commercial", "label_es": "Comercial y Airbnb", "label_en": "Commercial & Airbnb"},
        {"slug": "care-guides", "label_es": "Guías de Cuidado", "label_en": "Fabric Care Guides"},
        {"slug": "tips-and-life", "label_es": "Consejos y Ahorro", "label_en": "Tips & Life"},
    ],
    "posts_per_week": 1.5,
    "visual_identity_inspo": {
        "photoshoot_directory": "app-boilerplate/data/raw/creatives/interior-shots-2024",
        "wiki_reference": "wiki/entities/interior-shots-2024",
        "equipment": "Electrolux Professional commercial front-loaders with royal blue door rings; double-stacked dryers.",
        "machines_and_tables_activity": "MANDATORY: Tables and machines must ALWAYS have clothes; washers must ALWAYS show active white soap suds.",
    },
}


def get_el_laundry_profile() -> BrandProfile:
    """Instantiate canonical El Laundry BrandProfile."""
    return BrandProfile(**EL_LAUNDRY_DATA)
