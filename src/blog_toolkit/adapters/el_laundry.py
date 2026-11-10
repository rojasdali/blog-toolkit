"""El Laundry adapter for seamless integration with el-laundry-site."""

from pathlib import Path
from typing import Any

from blog_toolkit.adapters.llms_sync import sync_post_to_llms_txt
from blog_toolkit.adapters.topic_gatekeeper import (
    check_topic_against_surfaces,
    resolve_default_site_root,
    resolve_next_topic,
)
from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.core.types import BlogPost
from blog_toolkit.engine.deduplicator import ContentDeduplicator, sanitize_post_keywords
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.inspector import (
    get_used_images,
    parse_all_site_surfaces,
    parse_existing_posts,
)
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import ExistingPostSummary, GenerationRequest
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


class ElLaundryAdapter:
    """Specialized adapter for El Laundry website."""

    def __init__(self, site_root: str | Path | None = None):
        self.ruleset = BrandRuleset.from_preset("el_laundry")
        self.site_root = Path(site_root) if site_root else resolve_default_site_root(__file__)
        self.posts_file = self.site_root / "src" / "lib" / "blog" / "posts.ts"

    def get_existing_posts(self) -> list[ExistingPostSummary]:
        """Parse structured existing posts from posts.ts."""
        if not self.posts_file.exists():
            return []
        return parse_existing_posts(
            self.posts_file.read_text(encoding="utf-8"), default_category="blog"
        )

    def get_all_surfaces(self) -> list[ExistingPostSummary]:
        """Parse all live content registries (blog posts, commercial pillars, neighborhoods)."""
        return parse_all_site_surfaces(self.site_root)

    def get_existing_slugs(self) -> set[str]:
        return {p.slug for p in self.get_existing_posts()}

    def check_topic(self, candidate: str, threshold: float = 0.35) -> dict[str, Any]:
        """Check candidate topic against blog posts, commercial pillars, and neighborhood pages."""
        return check_topic_against_surfaces(candidate, self.get_all_surfaces(), threshold=threshold)

    def plan_upcoming_schedule(self, weeks: int = 4):
        """Generate a schedule taking into account all live surfaces and anti-duplication."""
        return ContentPlanner(self.ruleset).plan_calendar(
            weeks=weeks, existing_posts=self.get_all_surfaces()
        )

    def curate_next_post(
        self,
        topic: str | None = None,
        category: str | None = None,
        target_date: str | None = None,
        keywords: list[str] | None = None,
    ) -> BlogPost:
        """Curate, validate against multi-surface duplicates, and generate the next blog post."""
        existing = self.get_all_surfaces()
        r_top, r_cat, r_date, r_kws = resolve_next_topic(
            ContentPlanner(self.ruleset), topic, category, target_date, keywords, existing
        )
        is_dup, reason, _ = ContentDeduplicator(existing).is_duplicate(
            r_top, r_kws, r_top.lower().replace(" ", "-")
        )
        if is_dup:
            raise ValueError(f"Topic rejected due to cannibalization/duplication: {reason}")
        return self.generate_and_sync(r_top, r_cat, r_date, r_kws, list(get_used_images(existing)))

    def generate_and_sync(
        self,
        topic: str,
        category: str,
        target_date: str | None = None,
        keywords: list[str] | None = None,
        used_images: list[str] | None = None,
    ) -> BlogPost:
        """Generate a post and append directly into posts.ts and llms.txt."""
        req = GenerationRequest(
            topic=topic,
            category=category,
            target_date=target_date,
            target_keywords=keywords or [],
            used_images=used_images or [],
        )
        post = sanitize_post_keywords(
            BlogGenerator(self.ruleset).generate(req), self.get_all_surfaces()
        )
        if self.posts_file.exists():
            TypeScriptExporter().append_to_posts_file(post, str(self.posts_file))
            sync_post_to_llms_txt(self.site_root, post)
        return post
