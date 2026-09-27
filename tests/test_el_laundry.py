"""Tests for ElLaundryAdapter integration."""

from blog_toolkit.adapters.el_laundry import ElLaundryAdapter


def test_el_laundry_adapter_reads_existing_slugs():
    adapter = ElLaundryAdapter()
    slugs = adapter.get_existing_slugs()

    # If el-laundry-site/src/lib/blog/posts.ts exists, it should have the current live posts
    if adapter.posts_file.exists():
        assert len(slugs) > 0
        assert "lavado-doblado-hialeah-guia-completa" in slugs or len(slugs) >= 4


def test_el_laundry_adapter_plan_schedule():
    adapter = ElLaundryAdapter()
    plan = adapter.plan_upcoming_schedule(weeks=3)

    assert plan.brand_name == "El Laundry"
    assert len(plan.topics) >= 4
    for topic in plan.topics:
        assert topic.slug
        assert topic.category
