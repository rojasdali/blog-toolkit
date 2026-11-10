"""Post-generation keyword deduplication against existing site content."""

from blog_toolkit.core.types import BlogPost
from blog_toolkit.engine.types import ExistingPostSummary


def _filter_locale_keywords(
    keywords: list[str], used_kws: set[str], fallback_slug: str
) -> list[str]:
    """Strip any keyword that collides with existing posts and backfill from slug."""
    cleaned: list[str] = []
    seen: set[str] = set()
    for kw in keywords:
        norm = kw.lower().strip()
        if norm and norm not in used_kws and norm not in seen:
            cleaned.append(kw.strip())
            seen.add(norm)
    base_phrase = fallback_slug.replace("-", " ").strip()
    for suffix in ("", " hialeah", " el laundry"):
        candidate = f"{base_phrase}{suffix}".strip()
        if len(cleaned) < 3 and candidate.lower() not in used_kws and candidate.lower() not in seen:
            cleaned.append(candidate)
            seen.add(candidate.lower())
    return cleaned


def sanitize_post_keywords(post: BlogPost, existing_posts: list[ExistingPostSummary]) -> BlogPost:
    """Ensure generated post keywords never cannibalize any existing post's keywords."""
    used_kws = {k.lower().strip() for p in existing_posts for k in p.keywords}
    post.es.keywords = _filter_locale_keywords(
        post.es.keywords, used_kws, post.es.slug or post.slug
    )
    post.en.keywords = _filter_locale_keywords(
        post.en.keywords, used_kws, post.en.slug or post.slug
    )
    return post
