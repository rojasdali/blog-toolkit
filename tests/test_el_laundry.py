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


def test_el_laundry_adapter_curate_calls_generate(monkeypatch):
    adapter = ElLaundryAdapter()

    called = {}

    def mock_generate_and_sync(topic, category, target_date=None, keywords=None):
        called["topic"] = topic
        called["category"] = category
        from blog_toolkit.core.types import BlogPost, BlogSection, PostLocaleContent
        return BlogPost(
            slug="test-curate",
            image="/images/blog/test.webp",
            date="2026-09-26",
            read_time_minutes=4,
            author="Equipo El Laundry",
            category=category,
            es=PostLocaleContent(
                title="Título",
                excerpt="Resumen",
                keywords=["kw1"],
                key_takeaways=["t1"],
                sections=[BlogSection(heading="H1", paragraphs=["P1"])],
                category_label="Cat",
            ),
            en=PostLocaleContent(
                title="Title",
                excerpt="Excerpt",
                keywords=["kw1"],
                key_takeaways=["t1"],
                sections=[BlogSection(heading="H1", paragraphs=["P1"])],
                category_label="Cat",
            ),
        )

    monkeypatch.setattr(adapter, "generate_and_sync", mock_generate_and_sync)
    post = adapter.curate_next_post()
    assert post.slug == "test-curate"
    assert "topic" in called
