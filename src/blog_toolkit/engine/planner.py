"""Editorial calendar planner for 1-2x weekly publishing cadence."""

from datetime import datetime, timedelta

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.deduplicator import ContentDeduplicator
from blog_toolkit.engine.planner_topics import TOPIC_IDEAS_POOL
from blog_toolkit.engine.types import ContentPlan, ExistingPostSummary, PlannedTopic


class ContentPlanner:
    """Plans scheduled blog topics matching the brand ruleset."""

    def __init__(self, ruleset: BrandRuleset):
        self.ruleset = ruleset

    def _find_untapped_topic(
        self,
        pool: list[dict],
        cat: str,
        current_dt: datetime,
        dedup: ContentDeduplicator,
    ) -> PlannedTopic:
        """Find the first topic in the pool that does not duplicate existing posts."""
        date_str = current_dt.strftime("%Y-%m-%d")
        for item in pool:
            slug = str(item["slug"])
            topic = str(item["topic"])
            kws = list(item["keywords"])
            is_dup, _, _ = dedup.is_duplicate(topic, kws, slug)
            if not is_dup:
                return PlannedTopic(
                    topic=topic,
                    slug=slug,
                    category=cat,
                    target_keywords=kws,
                    target_date=date_str,
                    rationale=str(item.get("rationale", "")),
                )
        pick = pool[0]
        month_suffix = current_dt.strftime("%Y%m")
        return PlannedTopic(
            topic=str(pick["topic"]),
            slug=f"{pick['slug']}-{month_suffix}",
            category=cat,
            target_keywords=list(pick["keywords"]),
            target_date=date_str,
            rationale=str(pick.get("rationale", "")),
        )

    def plan_calendar(
        self,
        weeks: int = 4,
        start_date: datetime | None = None,
        existing_slugs: set[str] | None = None,
        existing_posts: list[ExistingPostSummary] | None = None,
    ) -> ContentPlan:
        """Generate a structured content calendar with anti-duplication defense."""
        start = start_date or datetime.now()
        posts_summary = existing_posts or [
            ExistingPostSummary(slug=s, titles=[s.replace("-", " ")])
            for s in (existing_slugs or set())
        ]
        dedup = ContentDeduplicator(posts_summary)
        topics: list[PlannedTopic] = []

        total_posts = max(1, int(weeks * self.ruleset.posts_per_week))
        days_between = max(3, int(7 / max(1.0, self.ruleset.posts_per_week)))
        current_dt = start

        categories = [c.slug for c in self.ruleset.categories] or list(TOPIC_IDEAS_POOL.keys())

        for i in range(total_posts):
            cat = categories[i % len(categories)]
            pool = TOPIC_IDEAS_POOL.get(cat, TOPIC_IDEAS_POOL.get("wash-and-fold", []))
            planned = self._find_untapped_topic(pool, cat, current_dt, dedup)
            topics.append(planned)
            posts_summary.append(
                ExistingPostSummary(
                    slug=planned.slug,
                    titles=[planned.topic],
                    keywords=planned.target_keywords,
                )
            )
            current_dt += timedelta(days=days_between)

        return ContentPlan(
            brand_name=self.ruleset.brand_name,
            start_date=start.strftime("%Y-%m-%d"),
            end_date=current_dt.strftime("%Y-%m-%d"),
            cadence_per_week=self.ruleset.posts_per_week,
            topics=topics,
        )
