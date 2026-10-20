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
            "topic": "Cómo Usar las Máquinas Gigantes de 65 lbs en Sedano's Plaza: Guía Paso a Paso",
            "slug": "guia-uso-lavadoras-gigantes-65-lbs-sedanos",
            "keywords": ["como usar lavadoras grandes sedanos", "instrucciones lavadoras 65 lbs", "lavanderia autoservicio guia"],
            "rationale": "High-intent operational guide for oversized self-service loads",
        },
        {
            "topic": "Consejos para Lavar en Horas Nocturnas: Seguridad, Iluminación y Parqueo en Hialeah",
            "slug": "consejos-lavar-horas-nocturnas-seguridad-hialeah",
            "keywords": ["lavar de noche hialeah", "lavanderia segura noche", "lavanderia iluminada hialeah"],
            "rationale": "Night-time and late-shift self-service laundry capture",
        },
    ],
    "wash-and-fold": [
        {
            "topic": "Lavado y Doblado de Ropa Infantil y de Bebé con Detergentes Hipoalergénicos",
            "slug": "lavado-doblado-ropa-infantil-bebe-hialeah",
            "keywords": ["lavado ropa bebe hipoalergenico", "wash and fold ropa infantil hialeah", "detergente suave ropa ninos"],
            "rationale": "High-trust family and baby clothes laundry capture",
        },
        {
            "topic": "Servicio de Lavandería Express para Choferes y Trabajadores del Transporte en Hialeah",
            "slug": "lavanderia-express-choferes-transporte-hialeah",
            "keywords": ["lavanderia express camioneros choferes", "lavado rapido ropa trabajo transporte", "wash and fold choferes hialeah"],
            "rationale": "Fast turnaround laundry capture for logistics and transport workers",
        },
        {
            "topic": "Servicio de Lavado y Doblado para Apartamentos y Condominios en West Hialeah",
            "slug": "wash-and-fold-apartamentos-condominios-west-hialeah",
            "keywords": ["lavanderia condominios hialeah", "wash and fold apartamentos west hialeah", "servicio drop off condominios"],
            "rationale": "Multi-family condo and apartment resident drop-off capture",
        },
    ],
    "comforters": [
        {
            "topic": "Cómo Lavar Cortinas Pesadas y Blackout sin Romper la Tela ni Desgastar los Ojetes",
            "slug": "como-lavar-cortinas-pesadas-blackout-lavanderia",
            "keywords": ["lavar cortinas blackout lavanderia", "lavadoras grandes cortinas pesadas", "cuidado cortinas hialeah"],
            "rationale": "Heavy drapery and blackout curtain deep clean capture",
        },
        {
            "topic": "Guía para Lavar Almohadas de Pluma y Memory Foam en Lavadoras Comerciales",
            "slug": "como-lavar-almohadas-pluma-memory-foam",
            "keywords": ["lavar almohadas pluma lavanderia", "desinfectar almohadas lavadora grande", "como lavar memory foam"],
            "rationale": "Pillow sanitization and bulky bedding care capture",
        },
    ],
    "commercial": [
        {
            "topic": "Servicio de Lavandería para Clínicas Dentales y Consultorios Médicos en Hialeah",
            "slug": "lavanderia-clinicas-dentales-consultorios-hialeah",
            "keywords": ["lavanderia batas medicas hialeah", "lavado uniformes clinicas medicas", "servicio toallas medicas hialeah"],
            "rationale": "Medical and dental office scrubs and lab coat B2B capture",
        },
        {
            "topic": "Lavado y Planchado de Manteles y Servilletas para Salones de Fiestas en Hialeah",
            "slug": "lavanderia-manteles-salones-fiestas-hialeah",
            "keywords": ["lavanderia manteles fiestas hialeah", "lavado manteleria eventos", "manteles limpios salones hialeah"],
            "rationale": "Event venue and banquet hall linen cleaning acquisition",
        },
        {
            "topic": "Servicio de Lavandería para Restaurantes y Negocios en Medley, FL",
            "slug": "lavanderia-restaurantes-negocios-medley-fl",
            "keywords": ["lavandería comercial medley fl", "commercial laundry service medley", "restaurant linen cleaning"],
            "rationale": "Commercial restaurant and hospitality linen acquisition in Medley",
        },
    ],
    "care-guides": [
        {
            "topic": "Cómo Lavar Ropa Térmica y Chaquetas de Plumas para Viajes sin Desinflarlas",
            "slug": "como-lavar-ropa-termica-chaquetas-plumas",
            "keywords": ["lavar chaquetas plumas lavanderia", "ropa termica viaje lavar", "cuidado plumones invierno"],
            "rationale": "Travel winterwear and down coat specialized care capture",
        },
    ],
}
