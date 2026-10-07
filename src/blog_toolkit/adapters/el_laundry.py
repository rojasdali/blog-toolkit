"""El Laundry adapter for seamless integration with el-laundry-site."""

from pathlib import Path

from blog_toolkit.adapters.gsc_loader import fetch_live_striking_keywords
from blog_toolkit.adapters.llms_sync import sync_post_to_llms_txt
from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.core.types import BlogPost
from blog_toolkit.engine.deduplicator import ContentDeduplicator
from blog_toolkit.engine.dynamic_keywords import pick_striking_topic
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.inspector import get_used_images, parse_existing_posts
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import ExistingPostSummary, GenerationRequest
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


class ElLaundryAdapter:
    """Specialized adapter for El Laundry website."""

    def __init__(self, site_root: str | Path | None = None):
        self.ruleset = BrandRuleset.from_preset("el_laundry")
        default_root = Path(__file__).resolve().parent.parent.parent.parent / "el-laundry-site"
        self.site_root = Path(site_root) if site_root else default_root
        self.posts_file = self.site_root / "src" / "lib" / "blog" / "posts.ts"

    def get_existing_posts(self) -> list[ExistingPostSummary]:
        """Parse structured existing posts from posts.ts."""
        if not self.posts_file.exists():
            return []
        return parse_existing_posts(self.posts_file.read_text(encoding="utf-8"))

    def get_existing_slugs(self) -> set[str]:
        return {p.slug for p in self.get_existing_posts()}

    def plan_upcoming_schedule(self, weeks: int = 4):
        """Generate a schedule taking into account existing posts and anti-duplication."""
        planner = ContentPlanner(self.ruleset)
        return planner.plan_calendar(weeks=weeks, existing_posts=self.get_existing_posts())

    def _resolve_topic(
        self,
        topic: str | None,
        category: str | None,
        target_date: str | None,
        keywords: list[str] | None,
        existing: list[ExistingPostSummary],
    ) -> tuple[str, str, str | None, list[str]]:
        if topic:
            return topic, category or "wash-and-fold", target_date, keywords or []
        striking = fetch_live_striking_keywords()
        if striking:
            p = pick_striking_topic(striking, existing, target_date or "")
            if p:
                return p.topic, p.category, p.target_date, p.target_keywords
        plan = self.plan_upcoming_schedule(weeks=4)
        if not plan.topics:
            raise ValueError("No planned topics available in the editorial schedule.")
        t = plan.topics[0]
        return t.topic, t.category, target_date or t.target_date, t.target_keywords

    def curate_next_post(
        self,
        topic: str | None = None,
        category: str | None = None,
        target_date: str | None = None,
        keywords: list[str] | None = None,
    ) -> BlogPost:
        """Curate, validate against duplicates, and generate the next blog post."""
        existing = self.get_existing_posts()
        r_top, r_cat, r_date, r_kws = self._resolve_topic(topic, category, target_date, keywords, existing)
        dedup = ContentDeduplicator(existing)
        is_dup, reason, _ = dedup.is_duplicate(r_top, r_kws, r_top.lower().replace(" ", "-"))
        if is_dup and topic:
            raise ValueError(f"Requested topic rejected due to duplication: {reason}")
        return self.generate_and_sync(
            topic=r_top,
            category=r_cat,
            target_date=r_date,
            keywords=r_kws,
            used_images=list(get_used_images(existing)),
        )

    def generate_and_sync(
        self,
        topic: str,
        category: str,
        target_date: str | None = None,
        keywords: list[str] | None = None,
        used_images: list[str] | None = None,
    ) -> BlogPost:
        """Generate a post and append directly into posts.ts and llms.txt."""
        generator = BlogGenerator(self.ruleset)
        req = GenerationRequest(
            topic=topic,
            category=category,
            target_date=target_date,
            target_keywords=keywords or [],
            used_images=used_images or [],
        )
        post = generator.generate(req)
        if self.posts_file.exists():
            TypeScriptExporter().append_to_posts_file(post, str(self.posts_file))
            sync_post_to_llms_txt(self.site_root, post)
        return post
