"""Editorial calendar planner for 1-2x weekly publishing cadence."""

from datetime import datetime, timedelta

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.types import ContentPlan, PlannedTopic

TOPIC_IDEAS_POOL: dict[str, list[dict[str, str | list[str]]]] = {
    "wash-and-fold": [
        {
            "topic": "Guía de Lavado y Doblado en Hialeah: Cuánto Tiempo Realmente Ahorras",
            "slug": "guia-lavado-doblado-ahorro-tiempo",
            "keywords": ["lavado y doblado hialeah", "wash and fold fl", "lavanderia mismo dia"],
            "rationale": "High conversion search intent for busy working families",
        },
        {
            "topic": "Cómo Funciona el Servicio de Ropa por Libra: Tarifas y Qué Incluye",
            "slug": "servicio-lavanderia-por-libra-precios",
            "keywords": ["precio por libra lavanderia", "lavanderia precios sedanos"],
            "rationale": "Cost transparency and objection handling",
        },
    ],
    "comforters": [
        {
            "topic": "Por Qué No Debes Lavar tu Edredón King en Casa (Y Cómo Lavarlo sin Dañarlo)",
            "slug": "como-lavar-edredon-king-lavadoras-gigantes",
            "keywords": ["lavar edredon king", "lavadoras gigantes 65 lbs", "lavar plumon hialeah"],
            "rationale": "High margin specialty item query",
        },
        {
            "topic": "Guía para Lavar Mantas Pesadas y Cortinas sin Quemar el Motor de tu Lavadora",
            "slug": "lavar-mantas-pesadas-cortinas-lavanderia",
            "keywords": ["lavar mantas pesadas", "lavanderia edredones sedanos"],
            "rationale": "Seasonal and deep clean traffic driver",
        },
    ],
    "commercial": [
        {
            "topic": "Lavandería para Airbnb en Hialeah y Miami: Higiene y Turnaround Rápido",
            "slug": "lavanderia-comercial-airbnb-hialeah",
            "keywords": ["lavanderia airbnb hialeah", "servicio sabanas toallas airbnb"],
            "rationale": "B2B commercial lead acquisition",
        },
        {
            "topic": "Servicio de Toallas y Uniformes para Barberías y Salones en Hialeah",
            "slug": "lavanderia-barberias-salones-belleza-hialeah",
            "keywords": ["lavanderia toallas barberia", "lavado uniformes negocios"],
            "rationale": "Commercial contract acquisition",
        },
    ],
    "care-guides": [
        {
            "topic": "Cómo Eliminar Manchas Difíciles de Ropa Blanca sin Cloro Dañino",
            "slug": "eliminar-manchas-ropa-blanca-sin-cloro",
            "keywords": ["quitar manchas ropa blanca", "consejos lavanderia"],
            "rationale": "Top of funnel informational search capture",
        },
    ],
}


class ContentPlanner:
    """Plans scheduled blog topics matching the brand ruleset."""

    def __init__(self, ruleset: BrandRuleset):
        self.ruleset = ruleset

    def plan_calendar(
        self,
        weeks: int = 4,
        start_date: datetime | None = None,
        existing_slugs: set[str] | None = None,
    ) -> ContentPlan:
        """Generate a structured content calendar."""
        start = start_date or datetime.now()
        existing = existing_slugs or set()
        topics: list[PlannedTopic] = []

        total_posts = int(weeks * self.ruleset.posts_per_week)
        total_posts = max(1, total_posts)

        days_between = max(3, int(7 / max(1.0, self.ruleset.posts_per_week)))
        current_dt = start

        categories = [c.slug for c in self.ruleset.categories] or list(TOPIC_IDEAS_POOL.keys())
        cat_idx = 0

        for i in range(total_posts):
            cat = categories[cat_idx % len(categories)]
            pool = TOPIC_IDEAS_POOL.get(cat, TOPIC_IDEAS_POOL["wash-and-fold"])
            pick = pool[i % len(pool)]

            slug = str(pick["slug"])
            if slug in existing:
                slug = f"{slug}-{current_dt.strftime('%Y%m')}"

            topics.append(
                PlannedTopic(
                    topic=str(pick["topic"]),
                    slug=slug,
                    category=cat,
                    target_keywords=list(pick["keywords"]),
                    target_date=current_dt.strftime("%Y-%m-%d"),
                    rationale=str(pick["rationale"]),
                )
            )
            cat_idx += 1
            current_dt += timedelta(days=days_between)

        return ContentPlan(
            brand_name=self.ruleset.brand_name,
            start_date=start.strftime("%Y-%m-%d"),
            end_date=current_dt.strftime("%Y-%m-%d"),
            cadence_per_week=self.ruleset.posts_per_week,
            topics=topics,
        )
