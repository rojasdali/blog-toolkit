"""Parser and inspector for existing blog posts in TypeScript repository."""

import re

from blog_toolkit.engine.types import ExistingPostSummary


def _extract_keywords(block: str) -> list[str]:
    """Extract list of keywords from a post block."""
    kw_blocks = re.findall(r"keywords:\s*\[(.*?)\]", block, re.DOTALL)
    keywords: list[str] = []
    for kwb in kw_blocks:
        keywords.extend(re.findall(r'["\']([^"\']+)["\']', kwb))
    return keywords


def _extract_single_post(block: str) -> ExistingPostSummary | None:
    """Parse a single TypeScript object block into an ExistingPostSummary."""
    slug_match = re.match(r'["\']([^"\']+)["\']', block)
    if not slug_match:
        return None
    slug = slug_match.group(1)

    img_match = re.search(r'image:\s*["\']([^"\']+)["\']', block)
    image = img_match.group(1) if img_match else ""

    cat_match = re.search(r'category:\s*["\']([^"\']+)["\']', block)
    category = cat_match.group(1) if cat_match else ""

    titles = re.findall(r'title:\s*["\']([^"\']+)["\']', block)
    keywords = _extract_keywords(block)

    return ExistingPostSummary(
        slug=slug,
        image=image,
        category=category,
        titles=titles,
        keywords=keywords,
    )


def parse_existing_posts(content: str) -> list[ExistingPostSummary]:
    """Parse posts.ts content into structured post summaries."""
    post_blocks = re.split(r"\n\s*\{\s*\n\s*slug:\s*", content)
    posts: list[ExistingPostSummary] = []
    for block in post_blocks[1:]:
        post = _extract_single_post(block)
        if post:
            posts.append(post)
    return posts


def get_used_images(posts: list[ExistingPostSummary]) -> set[str]:
    """Get unique image paths used by existing posts."""
    return {p.image for p in posts if p.image}
