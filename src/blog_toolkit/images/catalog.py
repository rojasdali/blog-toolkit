"""Image catalog storage and scanning."""

import json
from pathlib import Path

from blog_toolkit.images.types import ImageItem

DEFAULT_EL_LAUNDRY_IMAGES: list[dict[str, str | list[str]]] = [
    {
        "path": "/images/blog/washers-commercial-electrolux.webp",
        "alt_es": "Fila de lavadoras industriales Electrolux en El Laundry Hialeah",
        "alt_en": "Commercial Electrolux washers lineup at El Laundry in Hialeah",
        "tags": ["washers", "electrolux", "self-service", "machines", "comforters"],
        "category": "self-service",
    },
    {
        "path": "/images/blog/wash-and-fold-neat-stack.webp",
        "alt_es": "Pilas de ropa perfectamente lavada, doblada y empaquetada",
        "alt_en": "Neatly folded and packaged laundry ready for pickup",
        "tags": ["wash-and-fold", "clothes", "folding", "service"],
        "category": "wash-and-fold",
    },
    {
        "path": "/images/blog/giant-comforter-washer-65lb.webp",
        "alt_es": "Lavadora gigante de 65 libras lavando edredón King Size",
        "alt_en": "Giant 65-pound commercial washer cleaning King size comforter",
        "tags": ["comforters", "giant", "blankets", "quilts", "heavy"],
        "category": "comforters",
    },
    {
        "path": "/images/blog/commercial-laundry-towels-airbnb.webp",
        "alt_es": "Toallas blancas y sábanas para Airbnb y negocios locales",
        "alt_en": "Fresh white towels and linens for Airbnb and commercial clients",
        "tags": ["commercial", "airbnb", "towels", "business"],
        "category": "commercial",
    },
    {
        "path": "/images/blog/family-team-store-counter.webp",
        "alt_es": "Equipo familiar atendiendo amablemente en El Laundry",
        "alt_en": "Friendly family team assisting customers at El Laundry",
        "tags": ["team", "family", "customer service", "hialeah"],
        "category": "tips-and-life",
    },
]


class ImageCatalog:
    """Catalog of authenticated brand photography."""

    def __init__(self, images: list[ImageItem] | None = None):
        self.images = images or [ImageItem(**img) for img in DEFAULT_EL_LAUNDRY_IMAGES]

    @classmethod
    def from_file(cls, path: str | Path) -> "ImageCatalog":
        """Load image catalog from JSON."""
        file_path = Path(path)
        if not file_path.exists():
            return cls()
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return cls(images=[ImageItem(**d) for d in data])

    def add_image(self, item: ImageItem) -> None:
        """Add image to catalog."""
        self.images.append(item)
