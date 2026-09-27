"""Markdown exporter producing posts with YAML frontmatter."""

from blog_toolkit.core.types import BlogPost


class MarkdownExporter:
    """Exports a BlogPost to Markdown files with frontmatter."""

    def export(self, post: BlogPost, lang: str = "es") -> str:
        """Render a localized Markdown document."""
        loc = post.es if lang == "es" else post.en
        keywords_str = ", ".join([f'"{k}"' for k in loc.keywords])
        takeaways_str = "\n".join([f"- {t}" for t in loc.key_takeaways])

        sections_md = []
        for sec in loc.sections:
            lines = [f"## {sec.heading}", ""]
            lines.extend(sec.paragraphs)
            if sec.bullets:
                lines.append("")
                lines.extend([f"- {b}" for b in sec.bullets])
            if sec.callout:
                lines.append("")
                lines.append(f"> **💡 Tip:** {sec.callout}")
            lines.append("")
            sections_md.append("\n".join(lines))

        body = "\n".join(sections_md)

        return f"""---
title: "{loc.title}"
slug: "{post.slug}"
date: "{post.date}"
category: "{post.category}"
category_label: "{loc.category_label}"
author: "{post.author}"
image: "{post.image}"
read_time_minutes: {post.read_time_minutes}
featured: {str(post.featured).lower()}
excerpt: "{loc.excerpt}"
keywords: [{keywords_str}]
---

# {loc.title}

## Puntos Clave / Key Takeaways
{takeaways_str}

{body}
"""
