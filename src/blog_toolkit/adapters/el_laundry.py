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

    def curate_next_post(
        self,
        topic: str | None = None,
        category: str | None = None,
        target_date: str | None = None,
        keywords: list[str] | None = None,
    ) -> BlogPost:
        """Curate and append the next scheduled or requested blog post."""
        if not topic:
            plan = self.plan_upcoming_schedule(weeks=4)
            if not plan.topics:
                raise ValueError("No planned topics available in the editorial schedule.")
            next_topic = plan.topics[0]
            topic = next_topic.topic
            category = category or next_topic.category
            target_date = target_date or next_topic.target_date
            keywords = keywords or next_topic.target_keywords
        elif not category:
            category = "wash-and-fold"

        return self.generate_and_sync(
            topic=topic,
            category=category,
            target_date=target_date,
            keywords=keywords,
        )

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
            self.sync_to_llms_txt(post)

        return post

    def sync_to_llms_txt(self, post: BlogPost) -> None:
        """Synchronize the new post into content-es.ts and content-en.ts."""
        llms_dir = self.site_root / "src" / "app" / "llms.txt"
        es_file = llms_dir / "content-es.ts"
        en_file = llms_dir / "content-en.ts"

        if es_file.exists():
            c_es = es_file.read_text(encoding="utf-8")
            if post.slug not in c_es:
                entry = f"- [{post.es.title}](https://el-laundry.com/blog/{post.slug}): {post.es.excerpt}\n"
                marker = "## Páginas de Servicios Comerciales (B2B)"
                if marker in c_es:
                    c_es = c_es.replace(marker, f"{entry}\n{marker}")
                    es_file.write_text(c_es, encoding="utf-8")

        if en_file.exists():
            c_en = en_file.read_text(encoding="utf-8")
            if post.slug not in c_en:
                entry = f"- [{post.en.title}](https://el-laundry.com/en/blog/{post.slug}): {post.en.excerpt}\n"
                marker = "## Commercial Service Pages (B2B)"
                if marker in c_en:
                    c_en = c_en.replace(marker, f"{entry}\n{marker}")
                    en_file.write_text(c_en, encoding="utf-8")

