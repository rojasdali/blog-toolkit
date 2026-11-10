"""Multi-surface topic cannibalization gatekeeper & topic resolution for El Laundry."""

from pathlib import Path
from typing import Any

from blog_toolkit.adapters.gsc_loader import fetch_live_striking_keywords
from blog_toolkit.engine.deduplicator import jaccard_similarity, normalize_tokens
from blog_toolkit.engine.dynamic_keywords import pick_striking_topic
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import ExistingPostSummary


def resolve_default_site_root(anchor_file: str) -> Path:
    """Resolve sibling `el-laundry-site` directory from packaged or editable install."""
    here = Path(anchor_file).resolve()
    workspace_sibling = here.parents[4] / "el-laundry-site"
    return workspace_sibling if workspace_sibling.exists() else here.parents[3] / "el-laundry-site"


def check_topic_against_surfaces(
    candidate: str,
    surfaces: list[ExistingPostSummary],
    threshold: float = 0.35,
) -> dict[str, Any]:
    """Check candidate topic against blog posts, commercial pillars, and neighborhood pages."""
    cand_toks = normalize_tokens(candidate)
    for item in surfaces:
        slug_sim = jaccard_similarity(cand_toks, normalize_tokens(item.slug.replace("-", " ")))
        title_sims = [(t, jaccard_similarity(cand_toks, normalize_tokens(t))) for t in item.titles]
        best_title, best_t_sim = max(title_sims, key=lambda x: x[1], default=("", 0.0))
        kw_sim = jaccard_similarity(cand_toks, normalize_tokens(" ".join(item.keywords)))
        max_sim = max(slug_sim, best_t_sim, kw_sim)
        if max_sim >= threshold:
            return {
                "approved": False,
                "candidate": candidate,
                "threshold": threshold,
                "surfaces_scanned": len(surfaces),
                "conflict": {
                    "slug": item.slug,
                    "surface": item.category or "blog",
                    "title": best_title or item.slug,
                    "similarity": round(max_sim, 3),
                },
            }
    return {
        "approved": True,
        "candidate": candidate,
        "threshold": threshold,
        "surfaces_scanned": len(surfaces),
        "conflict": None,
    }


def resolve_next_topic(
    planner: ContentPlanner,
    topic: str | None,
    category: str | None,
    target_date: str | None,
    keywords: list[str] | None,
    existing: list[ExistingPostSummary],
) -> tuple[str, str, str | None, list[str]]:
    """Resolve explicit topic, live GSC striking-distance query, or next editorial plan slot."""
    if topic:
        return topic, category or "wash-and-fold", target_date, keywords or []
    striking = fetch_live_striking_keywords()
    if striking and (picked := pick_striking_topic(striking, existing, target_date or "")):
        return picked.topic, picked.category, picked.target_date, picked.target_keywords
    plan = planner.plan_calendar(weeks=4, existing_posts=existing)
    if not plan.topics:
        raise ValueError("No planned topics available in the editorial schedule.")
    first = plan.topics[0]
    return first.topic, first.category, target_date or first.target_date, first.target_keywords
