"""Curated and fallback topic ideas pool for content planning."""

TOPIC_IDEAS_POOL: dict[str, list[dict[str, str | list[str]]]] = {
    "self-service": [
        {
            "topic": "Lavandería con Máquinas de Monedas en Palm Springs North",
            "slug": "lavanderia-monedas-palm-springs-north",
            "keywords": ["lavandería de monedas palm springs north", "coin laundromat near me", "laundromat palm springs north"],
            "rationale": "High-intent geo capture for Palm Springs North residents (7 mins away)",
        },
        {
            "topic": "Lavandería con Monedas en Hialeah: Autoservicio y Máquinas Grandes",
            "slug": "lavanderia-con-monedas-hialeah-autoservicio",
            "keywords": ["coin laundry near me", "lavanderia monedas hialeah", "coin laundromat sedanos"],
            "rationale": "Targeting #1 high-volume striking search query (coin laundry near me)",
        },
        {
            "topic": "Lavandería Segura Cerca de Opa-locka: Autoservicio en Plaza de Sedano's",
            "slug": "lavanderia-segura-cerca-opa-locka",
            "keywords": ["lavandería cerca de opa-locka", "laundromat near opa-locka fl", "lavandería segura hialeah"],
            "rationale": "Safety, parking, and convenience capture for Opa-locka border residents",
        },
    ],
    "wash-and-fold": [
        {
            "topic": "Drop Off Laundry Service Cerca de Miami Lakes: Lavado y Doblado en Sedano's",
            "slug": "drop-off-laundry-service-miami-lakes",
            "keywords": ["drop off laundry service miami lakes", "lavado y doblado cerca de miami lakes", "wash and fold sedanos"],
            "rationale": "Directly targets GSC striking keyword (drop off laundry service miami lakes)",
        },
        {
            "topic": "Fluff and Fold en Hialeah: Servicio Profesional de Ropa por Libra el Mismo Día",
            "slug": "fluff-and-fold-hialeah-ropa-por-libra",
            "keywords": ["fluff and fold near me", "fluff and fold hialeah", "ropa por libra hialeah"],
            "rationale": "Directly targets striking search query (fluff and fold near me)",
        },
        {
            "topic": "Wash and Fold Cerca de Miami Springs: Servicio Familiar de Lavado y Doblado",
            "slug": "wash-and-fold-cerca-miami-springs",
            "keywords": ["wash and fold miami springs", "lavado y doblado cerca de miami springs", "drop off laundry near me"],
            "rationale": "Family-owned drop-off convenience for Miami Springs residents",
        },
    ],
    "comforters": [
        {
            "topic": "Las 5 Mejores Lavadoras para Edredones en Hialeah (y Dónde Encontrarlas)",
            "slug": "mejores-lavadoras-edredones-hialeah",
            "keywords": ["lavar edredón hialeah", "best washer for comforters hialeah", "lavadoras grandes 60 lbs"],
            "rationale": "Specialty heavy-duty comforter cleaning capture",
        },
        {
            "topic": "Guía para Lavar Mantas Pesadas y Cortinas sin Quemar tu Lavadora",
            "slug": "lavar-mantas-pesadas-cortinas-lavanderia",
            "keywords": ["lavar mantas pesadas", "lavanderia edredones sedanos", "lavar cortinas grandes"],
            "rationale": "Seasonal and deep clean traffic driver",
        },
    ],
    "commercial": [
        {
            "topic": "Servicio de Lavandería para Restaurantes y Negocios en Medley, FL",
            "slug": "lavanderia-restaurantes-negocios-medley-fl",
            "keywords": ["lavandería comercial medley fl", "commercial laundry service medley", "restaurant linen cleaning"],
            "rationale": "Commercial restaurant and hospitality linen acquisition in Medley",
        },
        {
            "topic": "Servicio de Toallas y Uniformes para Barberías y Salones en Hialeah",
            "slug": "lavanderia-barberias-salones-belleza-hialeah",
            "keywords": ["lavanderia toallas barberia", "lavado uniformes negocios", "salon towel laundry hialeah"],
            "rationale": "Commercial contract acquisition for local grooming salons",
        },
    ],
    "care-guides": [
        {
            "topic": "Cómo Lavar Uniformes de Trabajo Industriales sin que Pierdan la Forma",
            "slug": "como-lavar-uniformes-trabajo-industriales",
            "keywords": ["cómo lavar uniformes de trabajo", "industrial uniform cleaning hialeah", "lavar uniforme"],
            "rationale": "Industrial workwear fabric care and B2B lead capture",
        },
        {
            "topic": "Cómo Eliminar Manchas Difíciles de Ropa Blanca sin Cloro Dañino",
            "slug": "eliminar-manchas-ropa-blanca-sin-cloro",
            "keywords": ["quitar manchas ropa blanca", "consejos lavanderia", "eliminar manchas vino salsa"],
            "rationale": "Top of funnel informational search capture",
        },
    ],
}
