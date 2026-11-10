"""Curated and fallback topic ideas pool aligned to unserved 90-day GSC demand gaps."""

from blog_toolkit.engine.planner_topics_b2b import B2B_AND_CARE_TOPICS

RETAIL_TOPICS: dict[str, list[dict[str, str | list[str]]]] = {
    "self-service": [
        {
            "topic": "Lavandería en North Hialeah (W 52nd St): Autoservicio 65 lbs y Drop-Off $1/lb",
            "slug": "lavanderia-north-hialeah-w-52nd-st",
            "keywords": [
                "laundromat north hialeah",
                "laundry drop off north hialeah",
                "lavanderia norte de hialeah",
            ],
            "rationale": "209+ 90d GSC impressions across North Hialeah queries with zero dedicated page",
        },
        {
            "topic": "Cómo Usar Lavadoras Comerciales de 65 lbs en Sedano's Plaza: Guía de Carga y Ciclos",
            "slug": "guia-uso-lavadoras-gigantes-65-lbs-sedanos",
            "keywords": [
                "como usar lavadoras grandes sedanos",
                "instrucciones lavadoras 65 lbs",
                "lavanderia 65 libras capacidad",
            ],
            "rationale": "High-intent operational guide for oversized 65 lb (20 kg) self-service drums",
        },
        {
            "topic": "Consejos para Lavar después del Trabajo en Hialeah: Último Lavado 8 PM y Parqueo Iluminado",
            "slug": "consejos-lavar-tarde-seguridad-parqueo-hialeah",
            "keywords": [
                "lavanderia abierta hasta las 9 pm hialeah",
                "ultimo lavado 8 pm hialeah",
                "lavanderia iluminada parqueo gratis",
            ],
            "rationale": "Post-work 4PM-8PM rush capture aligned with 8:00 PM Last Wash policy",
        },
    ],
    "comforters": [
        {
            "topic": "Cómo Lavar Cortinas Pesadas y Blackout en Lavadoras de 65 lbs sin Dañar Ojetes",
            "slug": "como-lavar-cortinas-pesadas-blackout-lavanderia",
            "keywords": [
                "lavar cortinas blackout lavanderia",
                "lavadoras grandes cortinas pesadas",
                "cuidado cortinas gruesas hialeah",
            ],
            "rationale": "Heavy drapery and blackout curtain deep-clean AEO capture",
        },
        {
            "topic": "Guía para Lavar Almohadas de Pluma y Protectores de Colchón en Tambores Comerciales",
            "slug": "como-lavar-almohadas-pluma-protectores-colchon",
            "keywords": [
                "lavar almohadas pluma lavanderia",
                "lavar protector de colchon acolchado",
                "desinfectar almohadas lavadora 65 lbs",
            ],
            "rationale": "Bulky bedding and mattress pad sanitization AEO capture",
        },
    ],
    "wash-and-fold": [
        {
            "topic": "Servicio de Lavado por Volumen (Bulk Laundry) para Familias Grandes en North Hialeah",
            "slug": "lavado-por-volumen-familias-north-hialeah",
            "keywords": [
                "bulk laundry service north hialeah",
                "drop off laundry service north hialeah",
                "lavado por libra familias grandes",
            ],
            "rationale": "Captures 117+ GSC impressions on North Hialeah bulk & drop-off queries",
        },
    ],
}

TOPIC_IDEAS_POOL: dict[str, list[dict[str, str | list[str]]]] = {
    **RETAIL_TOPICS,
    **B2B_AND_CARE_TOPICS,
}
