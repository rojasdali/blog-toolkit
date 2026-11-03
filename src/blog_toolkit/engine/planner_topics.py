"""Curated and fallback topic ideas pool for content planning."""

TOPIC_IDEAS_POOL: dict[str, list[dict[str, str | list[str]]]] = {
    "self-service": [
        {
            "topic": "Lavandería con Máquinas de Monedas en Palm Springs North",
            "slug": "lavanderia-monedas-palm-springs-north",
            "keywords": [
                "lavandería de monedas palm springs north",
                "coin laundromat palm springs north",
                "laundromat palm springs north fl",
            ],
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
            "topic": "Lavado y Doblado para Personas Mayores y Seniors en Hialeah: Empaque Fácil por Cajón",
            "slug": "lavado-doblado-personas-mayores-seniors-hialeah",
            "keywords": [
                "lavanderia para personas mayores hialeah",
                "senior laundry service hialeah",
                "doblado organizado por cajon",
            ],
            "rationale": "High-retention drop-off capture for seniors and caregivers in Hialeah",
        },
        {
            "topic": "Cómo Preparar tu Bolsa de Drop-Off por Primera Vez: Separación, Peso Mínimo y Preferencias",
            "slug": "como-preparar-bolsa-drop-off-primera-vez",
            "keywords": [
                "como funciona servicio drop off lavanderia",
                "first time wash and fold guide",
                "preparar ropa lavado por libra",
            ],
            "rationale": "First-time drop-off customer conversion and onboarding guide",
        },
        {
            "topic": "Lavado por Libra para Estudiantes y Profesionales con Horarios Rotativos en Miami-Dade",
            "slug": "lavado-por-libra-estudiantes-turnos-rotativos-hialeah",
            "keywords": [
                "lavanderia para turnos rotativos hialeah",
                "wash and fold busy professionals hialeah",
                "entrega mismo dia antes 12pm",
            ],
            "rationale": "Same-day turnaround capture for shift workers and college students",
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
            "topic": "Lavado de Toallas de Microfibra para Car Wash y Talleres de Detailing en Hialeah",
            "slug": "lavado-toallas-microfibra-car-wash-detailing-hialeah",
            "keywords": [
                "lavar toallas microfibra detailing hialeah",
                "auto detailing towel laundry service",
                "lavanderia comercial car wash miami",
            ],
            "rationale": "Commercial microfiber towel care for Hialeah auto detailing shops",
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
