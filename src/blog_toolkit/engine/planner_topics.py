"""Curated and fallback topic ideas pool aligned to unserved 90-day GSC demand gaps."""

from blog_toolkit.engine.planner_topics_b2b import B2B_AND_CARE_TOPICS

RETAIL_TOPICS: dict[str, list[dict[str, str | list[str]]]] = {
    "self-service": [
        {
            "topic": "Cuántas Cargas de Ropa Caben en una Lavadora de 65 lbs vs. 20 lbs: Guía de Ahorro",
            "slug": "cuantas-cargas-caben-lavadora-65-lbs-vs-20-lbs",
            "keywords": [
                "cuanta ropa cabe en lavadora 65 libras",
                "capacidad lavadora 20 kg en libras",
                "cuantas cestas caben lavadora industrial",
            ],
            "rationale": "High-volume kg/lb drum sizing AEO & Featured Snippet demand",
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
            "topic": "Cómo Lavar Alfombras Lavables (Ruggable) y Forros de Sofá en Tambores de 65 lbs",
            "slug": "como-lavar-alfombras-lavables-forros-sofa-65-lbs",
            "keywords": [
                "lavar alfombras lavables lavanderia",
                "lavar forros de sofa muebles grandes",
                "lavadora gigante para alfombras hialeah",
            ],
            "rationale": "Machine-washable area rugs and slipcovers high-intent 65 lb drum AEO capture",
        },
        {
            "topic": "Cómo Lavar Sacos de Dormir, Cobijas Pesadas (Weighted Blankets) y Mantas Polares",
            "slug": "como-lavar-weighted-blankets-cobijas-pesadas-65-lbs",
            "keywords": [
                "como lavar weighted blanket cobija pesada",
                "lavar cobijas gruesas san marcos lavanderia",
                "lavadora 65 lbs cobijas pesadas hialeah",
            ],
            "rationale": "Heavy weighted blankets and San Marcos / plush mink blankets AEO & Hialeah household demand",
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
