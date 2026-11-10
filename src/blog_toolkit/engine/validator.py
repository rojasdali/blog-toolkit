"""Configurable brand & AEO post validator decoupled from store-specific constants."""

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.core.types import BlogPost, PostLocaleContent


def _flatten_locale_text(locale_content: PostLocaleContent) -> str:
    parts = [
        locale_content.title,
        locale_content.excerpt,
        *locale_content.key_takeaways,
    ]
    for sec in locale_content.sections:
        parts.append(sec.heading)
        parts.extend(sec.paragraphs)
        parts.extend(sec.bullets)
        if sec.callout:
            parts.append(sec.callout)
    return " ".join(parts)


def _check_aeo_density(locale_content: PostLocaleContent, lang: str) -> list[str]:
    issues: list[str] = []
    title_len = len(locale_content.title.strip())
    if not (42 <= title_len <= 58):
        issues.append(f"[{lang}] Title length {title_len} outside 42-58 char mobile SERP target")
    if len(locale_content.key_takeaways) < 3:
        issues.append(
            f"[{lang}] Fewer than 3 AEO key_takeaways ({len(locale_content.key_takeaways)})"
        )
    for idx, item in enumerate(locale_content.key_takeaways):
        if len(item.strip()) < 20:
            issues.append(f"[{lang}] key_takeaways[{idx}] shorter than 20 chars")
    return issues


def validate_post_content(
    post: BlogPost,
    profile: BrandRuleset,
    strict_aeo: bool = False,
) -> list[str]:
    """Validate a BlogPost against configurable BrandProfile guardrails."""
    violations: list[str] = []
    combined_text = f"{_flatten_locale_text(post.es)} {_flatten_locale_text(post.en)}".lower()

    for forbidden in profile.effective_forbidden_terms():
        if forbidden.lower() in combined_text:
            violations.append(f"Forbidden phrase detected: '{forbidden}'")

    valid_slugs = [c.slug for c in profile.categories]
    if valid_slugs and post.category not in valid_slugs:
        violations.append(f"Unknown category '{post.category}'. Expected one of {valid_slugs}")

    if strict_aeo:
        violations.extend(_check_aeo_density(post.es, "es"))
        violations.extend(_check_aeo_density(post.en, "en"))

    return violations
