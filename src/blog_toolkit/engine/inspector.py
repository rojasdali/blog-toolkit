"""Parser and inspector for existing blog posts, commercial pillars, and neighborhoods."""

import re
from pathlib import Path

from blog_toolkit.engine.types import ExistingPostSummary

SURFACE_REGISTRIES: tuple[tuple[str, str], ...] = (
    ("blog", "src/lib/blog/posts.ts"),
    ("commercial", "src/lib/commercial/pillars.ts"),
    ("neighborhood", "src/lib/locations/neighborhoods.ts"),
)


def _extract_keywords(block: str) -> list[str]:
    """Extract list of keywords from a post block."""
    kw_blocks = re.findall(r"\"?keywords\"?:\s*\[(.*?)\]", block, re.DOTALL)
    keywords: list[str] = []
    for kwb in kw_blocks:
        keywords.extend(re.findall(r'["\']([^"\']+)["\']', kwb))
    return keywords


def _extract_primary_titles(block: str) -> list[str]:
    """Extract localized primary titles and metaTitles while ignoring spec sub-titles."""
    titles: list[str] = []
    for lang in ("es", "en"):
        m = re.search(rf"\b{lang}:\s*\{{([\s\S]*?)(?=\n\s+(?:en|es):\s*\{{|\Z)", block)
        if not m:
            continue
        sub = m.group(1)
        for pat in (
            r'(?<![a-zA-Z])"?title"?:\s*["\']([^"\']+)["\']',
            r'\b"?metaTitle"?:\s*["\']([^"\']+)["\']',
        ):
            hit = re.search(pat, sub)
            if hit and hit.group(1) not in titles:
                titles.append(hit.group(1))
    return titles or re.findall(r'(?<![a-zA-Z])"?title"?:\s*["\']([^"\']+)["\']', block)


def _extract_single_post(block: str, default_category: str = "") -> ExistingPostSummary | None:
    """Parse a single TypeScript object block into an ExistingPostSummary."""
    slug_match = re.match(r'["\']([^"\']+)["\']', block)
    if not slug_match:
        return None
    slug = slug_match.group(1)
    img_match = re.search(r"\"?image\"?:\s*[\"']([^\"']+)[\"']", block)
    cat_match = re.search(r"\"?category\"?:\s*[\"']([^\"']+)[\"']", block)
    return ExistingPostSummary(
        slug=slug,
        image=img_match.group(1) if img_match else "",
        category=cat_match.group(1) if cat_match else default_category,
        titles=_extract_primary_titles(block),
        keywords=_extract_keywords(block),
    )


def parse_existing_posts(content: str, default_category: str = "") -> list[ExistingPostSummary]:
    """Parse TypeScript registry content into structured ExistingPostSummary items."""
    post_blocks = re.split(r"\n\s*\{\s*\n\s*\"?slug\"?:\s*", content)
    posts: list[ExistingPostSummary] = []
    for block in post_blocks[1:]:
        post = _extract_single_post(block, default_category=default_category)
        if post:
            posts.append(post)
    return posts


def parse_all_site_surfaces(site_root: Path) -> list[ExistingPostSummary]:
    """Scan blog posts, commercial pillars, and neighborhood pages for cannibalization checks."""
    summaries: list[ExistingPostSummary] = []
    for surface, rel_path in SURFACE_REGISTRIES:
        file_path = site_root / rel_path
        if file_path.exists():
            summaries.extend(
                parse_existing_posts(
                    file_path.read_text(encoding="utf-8"), default_category=surface
                )
            )
    return summaries


def get_used_images(posts: list[ExistingPostSummary]) -> set[str]:
    """Get unique image paths used by existing posts."""
    return {p.image for p in posts if p.image}
