"""Editorial calendar planner for 1-2x weekly publishing cadence."""

from datetime import datetime, timedelta

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.planner_topics import TOPIC_IDEAS_POOL
from blog_toolkit.engine.types import ContentPlan, PlannedTopic


class ContentPlanner:
    """Plans scheduled blog topics matching the brand ruleset."""

    def __init__(self, ruleset: BrandRuleset):
        self.ruleset = ruleset

    def plan_calendar(
        self,
        weeks: int = 4,
        start_date: datetime | None = None,
        existing_slugs: set[str] | None = None,
    ) -> ContentPlan:
        """Generate a structured content calendar."""
        start = start_date or datetime.now()
        existing = existing_slugs or set()
        topics: list[PlannedTopic] = []

        total_posts = int(weeks * self.ruleset.posts_per_week)
        total_posts = max(1, total_posts)

        days_between = max(3, int(7 / max(1.0, self.ruleset.posts_per_week)))
        current_dt = start

        categories = [c.slug for c in self.ruleset.categories] or list(TOPIC_IDEAS_POOL.keys())
        cat_idx = 0

        for i in range(total_posts):
            cat = categories[cat_idx % len(categories)]
            pool = TOPIC_IDEAS_POOL.get(cat, TOPIC_IDEAS_POOL.get("wash-and-fold", []))
            pick = pool[i % len(pool)]

            slug = str(pick["slug"])
            if slug in existing:
                slug = f"{slug}-{current_dt.strftime('%Y%m')}"

            topics.append(
                PlannedTopic(
                    topic=str(pick["topic"]),
                    slug=slug,
                    category=cat,
                    target_keywords=list(pick["keywords"]),
                    target_date=current_dt.strftime("%Y-%m-%d"),
                    rationale=str(pick["rationale"]),
                )
            )
            cat_idx += 1
            current_dt += timedelta(days=days_between)

        return ContentPlan(
            brand_name=self.ruleset.brand_name,
            start_date=start.strftime("%Y-%m-%d"),
            end_date=current_dt.strftime("%Y-%m-%d"),
            cadence_per_week=self.ruleset.posts_per_week,
            topics=topics,
        )
