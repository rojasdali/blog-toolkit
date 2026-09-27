---
name: blog-toolkit
description: >-
  Agnostic, modular blog generation, content planning, and SEO/AEO publishing toolkit powered by Gemini AI. Use when planning 1-2x weekly content calendars, researching keyword-targeted topics, generating structured bilingual posts, matching real brand photography, and exporting to Next.js TypeScript, Markdown, or JSON.
metadata:
  category: ContentEngine
  author: rojasdali
  version: "0.1.0"
---

# Blog Toolkit SDK Skill

Use this skill when you need to plan, research, generate, audit, or publish blog content programmatically using the `blog-toolkit` library.

---

## 🚀 Quickstart & Initialization

### Environment Configuration
The toolkit parses credentials from `.env` or system environment:
```bash
GEMINI_API_KEY="your_gemini_api_key_here"
BLOG_TOOLKIT_PRESET="el_laundry" # or "default"
```

### Initializing the Toolkit
```python
from blog_toolkit import BrandRuleset, BlogGenerator, ContentPlanner, ImageCatalog
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter

# Load brand ruleset (from JSON file or built-in preset)
ruleset = BrandRuleset.from_preset("el_laundry")

# Initialize generator with Gemini AI
generator = BlogGenerator(ruleset)

# Generate a post
req = GenerationRequest(
    topic="Cómo Lavar Edredones Gigantes y Colchas en Hialeah",
    category="comforters",
    target_keywords=["lavar edredon king hialeah", "lavadoras gigantes 65 lbs"],
)
post = generator.generate(req)

# Export to Next.js TypeScript format
ts_code = TypeScriptExporter().export(post)
```

---

## 📅 Editorial Calendar Planning (1–2x Weekly)

```python
planner = ContentPlanner(ruleset)
plan = planner.plan_calendar(weeks=4)

for topic in plan.topics:
    print(f"[{topic.target_date}] ({topic.category}) {topic.topic}")
    print(f"Slug: /{topic.slug}")
    print(f"Keywords: {topic.target_keywords}")
```

---

## 💻 CLI Commands

```bash
# Generate 4-week publishing calendar
blog-toolkit plan --preset el_laundry --weeks 4

# Generate post and output to Next.js TypeScript
blog-toolkit generate \
  --topic "Guía de Lavado y Doblado en Hialeah" \
  --category "wash-and-fold" \
  --preset el_laundry \
  --format ts \
  --out ../el-laundry-site/src/lib/blog/new_post.ts
```

---

## 🏢 El Laundry Adapter

```python
from blog_toolkit.adapters.el_laundry import ElLaundryAdapter

adapter = ElLaundryAdapter()
existing_slugs = adapter.get_existing_slugs()
upcoming_plan = adapter.plan_upcoming_schedule(weeks=4)
```
