"""Prompt engineering for structured blog generation driven by configurable BrandProfile."""

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.types import GenerationRequest


def _format_optional_block(heading: str, items: list[str] | str) -> str:
    if isinstance(items, str):
        return f"\n{heading}:\n- {items.strip()}\n" if items.strip() else ""
    cleaned = [i.strip() for i in items if i.strip()]
    if not cleaned:
        return ""
    bullet_lines = "\n- ".join(cleaned)
    return f"\n{heading}:\n- {bullet_lines}\n"


def build_system_prompt(ruleset: BrandRuleset) -> str:
    """Build the editorial and brand system instructions from BrandProfile fields."""
    geo_info = ", ".join([f"{k}: {v}" for k, v in ruleset.location_context.items()])
    diffs = "\n- ".join(ruleset.key_differentiators)
    services = "\n- ".join(ruleset.services)
    forbidden = ", ".join(ruleset.effective_forbidden_terms()) or "None"
    pricing_block = _format_optional_block(
        "Verified Pricing Facts (Use Exact Rates Only)", ruleset.pricing_facts
    )
    cutoff_block = _format_optional_block("Turnaround & Cutoff Policy", ruleset.cutoff_time)

    return f"""You are an elite SEO/AEO content strategist and bilingual copywriter for '{ruleset.brand_name}'.
Brand Tagline: {ruleset.tagline}
Brand Voice: {ruleset.brand_voice}
Target Audience: {ruleset.target_audience}
Author Name: {ruleset.author_name}

Geographic Context:
{geo_info}

Core Services:
- {services}

Key Differentiators:
- {diffs}
{pricing_block}{cutoff_block}
Strict Rules:
1. NEVER use any of these forbidden terms or phrases: {forbidden}.
2. Output MUST be valid JSON adhering strictly to the BlogPost schema.
3. Provide BOTH Spanish ('es') and English ('en') content with native phrasing and identical section count.
4. Each post must feature 3-5 structured sections (heading, 1-2 paragraphs, optional bullet points, optional callout). Open Section 1 paragraph 1 with a 2-sentence Snippet-First direct factual answer (40-55 words).
5. Include 3-5 concise, actionable 'key_takeaways' per language (>= 20 chars each) for Answer Engine Optimization (AEO/LLM search).
6. Keep both 'es.title' and 'en.title' strictly between 42 and 58 characters (so mobile SERPs never truncate price/unit hooks), and ensure 'en.slug' is an English-translated hyphenated slug distinct from 'es.slug'.
7. Naturally reference authentic local context and verified pricing/cutoff policies when relevant."""


def build_user_prompt(req: GenerationRequest, ruleset: BrandRuleset, image_path: str) -> str:
    """Build the generation prompt for a specific topic."""
    cat_item = next((c for c in ruleset.categories if c.slug == req.category), None)
    cat_label_es = cat_item.label_es if cat_item else req.category
    cat_label_en = cat_item.label_en if cat_item else req.category
    keywords_str = (
        ", ".join(req.target_keywords) if req.target_keywords else "High-intent local search"
    )

    return f"""Generate a high-converting, educational blog post.
Topic: {req.topic}
Category Slug: {req.category}
Category Label ES: {cat_label_es}
Category Label EN: {cat_label_en}
Target Keywords: {keywords_str}
Assigned Cover Image: {image_path}
Publish Date: {req.target_date or "YYYY-MM-DD"}

Return ONLY the raw JSON matching the BlogPost schema with keys:
slug, date, read_time_minutes, featured, author, image, category, es, en."""
