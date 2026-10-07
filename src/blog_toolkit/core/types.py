"""Domain types for the agnostic blog toolkit."""

from pydantic import BaseModel, Field


class BlogSection(BaseModel):
    """Structured section within a blog post."""

    heading: str = Field(description="H2 or H3 heading for the section")
    paragraphs: list[str] = Field(description="Body paragraphs for this section")
    bullets: list[str] = Field(default_factory=list, description="Optional bullet points")
    callout: str | None = Field(default=None, description="Optional highlight or tip callout")


class PostLocaleContent(BaseModel):
    """Localized content for a single language."""

    slug: str | None = Field(default=None, description="Localized URL slug")
    title: str = Field(description="SEO and conversion optimized title")
    excerpt: str = Field(description="1-2 sentence meta description/excerpt")
    keywords: list[str] = Field(default_factory=list, description="Target search keywords")
    key_takeaways: list[str] = Field(
        default_factory=list, description="3-5 bulleted key takeaways for AEO"
    )
    sections: list[BlogSection] = Field(description="Ordered structured content sections")
    category_label: str = Field(description="Human-readable category badge text")


class BlogPost(BaseModel):
    """Unified bilingual blog post structure."""

    slug: str = Field(description="URL-friendly kebab-case slug")
    date: str = Field(description="Publication date in ISO format YYYY-MM-DD")
    read_time_minutes: int = Field(default=4, description="Estimated reading time in minutes")
    featured: bool = Field(default=False, description="Whether this is a highlighted post")
    author: str = Field(default="Editorial Team", description="Author or team name")
    image: str = Field(description="Primary cover image path or URL")
    category: str = Field(description="Category slug matching taxonomy")
    es: PostLocaleContent = Field(description="Spanish language content")
    en: PostLocaleContent = Field(description="English language content")

    def word_count(self, lang: str = "es") -> int:
        """Calculate approximate word count for a language."""
        content = self.es if lang == "es" else self.en
        text = content.title + " " + content.excerpt + " " + " ".join(content.key_takeaways)
        for s in content.sections:
            text += " " + s.heading + " " + " ".join(s.paragraphs) + " " + " ".join(s.bullets)
            if s.callout:
                text += " " + s.callout
        return len(text.split())
