"""El Laundry adapter for seamless integration with el-laundry-site."""

import re
from pathlib import Path

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.core.types import BlogPost
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


class ElLaundryAdapter:
    """Specialized adapter for El Laundry website."""

    def __init__(self, site_root: str | Path | None = None):
        self.ruleset = BrandRuleset.from_preset("el_laundry")
        self.site_root = (
            Path(site_root)
            if site_root
            else Path(__file__).resolve().parent.parent.parent.parent / "el-laundry-site"
        )
        self.posts_file = self.site_root / "src" / "lib" / "blog" / "posts.ts"

    def get_existing_slugs(self) -> set[str]:
        """Extract existing slugs from posts.ts using regex."""
        if not self.posts_file.exists():
            return set()
        content = self.posts_file.read_text(encoding="utf-8")
        matches = re.findall(r'slug:\s*["\']([^"\']+)["\']', content)
        return set(matches)

    def plan_upcoming_schedule(self, weeks: int = 4):
        """Generate a schedule taking into account existing slugs."""
        planner = ContentPlanner(self.ruleset)
        existing = self.get_existing_slugs()
        return planner.plan_calendar(weeks=weeks, existing_slugs=existing)

    def generate_and_sync(
        self,
        topic: str,
        category: str,
        target_date: str | None = None,
        keywords: list[str] | None = None,
    ) -> BlogPost:
        """Generate a post and append directly into posts.ts."""
        generator = BlogGenerator(self.ruleset)
        req = GenerationRequest(
            topic=topic,
            category=category,
            target_date=target_date,
            target_keywords=keywords or [],
        )
        post = generator.generate(req)

        if self.posts_file.exists():
            exporter = TypeScriptExporter()
            exporter.append_to_posts_file(post, str(self.posts_file))

        return post
