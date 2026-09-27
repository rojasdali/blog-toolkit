"""Tests for exporters (TypeScript, Markdown, JSON)."""

from blog_toolkit.core.types import BlogPost, BlogSection, PostLocaleContent
from blog_toolkit.exporters.json_exporter import JsonExporter
from blog_toolkit.exporters.markdown_exporter import MarkdownExporter
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


def sample_post() -> BlogPost:
    return BlogPost(
        slug="test-slug",
        date="2026-10-10",
        read_time_minutes=3,
        featured=False,
        author="Equipo El Laundry",
        image="/images/test.webp",
        category="care-guides",
        es=PostLocaleContent(
            title="Título de Prueba",
            excerpt="Extracto de prueba",
            keywords=["prueba"],
            key_takeaways=["Punto 1", "Punto 2"],
            sections=[
                BlogSection(
                    heading="Sección 1",
                    paragraphs=["Párrafo de prueba."],
                    bullets=["Bala 1"],
                    callout="Consejo útil",
                )
            ],
            category_label="Guías",
        ),
        en=PostLocaleContent(
            title="Test Title",
            excerpt="Test Excerpt",
            keywords=["test"],
            key_takeaways=["Point 1", "Point 2"],
            sections=[
                BlogSection(
                    heading="Section 1",
                    paragraphs=["Test paragraph."],
                    bullets=["Bullet 1"],
                    callout="Useful tip",
                )
            ],
            category_label="Guides",
        ),
    )


def test_typescript_export():
    post = sample_post()
    ts_code = TypeScriptExporter().export(post)
    assert '"slug": "test-slug"' in ts_code
    assert '"readTimeMinutes": 3' in ts_code
    assert '"keyTakeaways"' in ts_code
    assert '"categoryLabel": "Guías"' in ts_code


def test_markdown_export():
    post = sample_post()
    md_es = MarkdownExporter().export(post, lang="es")
    assert 'title: "Título de Prueba"' in md_es
    assert "## Sección 1" in md_es
    assert "- Bala 1" in md_es
    assert "> **💡 Tip:** Consejo útil" in md_es


def test_json_export():
    post = sample_post()
    json_str = JsonExporter().export(post)
    assert '"slug": "test-slug"' in json_str
    assert '"category": "care-guides"' in json_str
