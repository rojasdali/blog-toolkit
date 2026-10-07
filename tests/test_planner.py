"""Tests for ContentPlanner calendar generator."""

from datetime import datetime

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.planner import ContentPlanner


def test_plan_calendar_cadence():
    ruleset = BrandRuleset.from_preset("el_laundry")
    planner = ContentPlanner(ruleset)

    # 4 weeks at 1.5 posts per week -> 6 posts
    plan = planner.plan_calendar(weeks=4, start_date=datetime(2026, 10, 1))
    assert plan.brand_name == "El Laundry"
    assert len(plan.topics) == 6
    assert plan.topics[0].target_date == "2026-10-01"

    for t in plan.topics:
        assert t.slug
        assert t.topic
        assert len(t.target_keywords) > 0


def test_plan_calendar_avoids_existing_slugs():
    ruleset = BrandRuleset.from_preset("el_laundry")
    planner = ContentPlanner(ruleset)

    existing = {"lavanderia-monedas-palm-springs-north"}
    plan = planner.plan_calendar(weeks=2, start_date=datetime(2026, 10, 1), existing_slugs=existing)

    generated_slugs = [t.slug for t in plan.topics]
    assert "lavanderia-monedas-palm-springs-north" not in generated_slugs
    # Asserts that an alternative untapped topic from the pool was selected instead
    assert any("lavanderia" in s for s in generated_slugs)
