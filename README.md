# 📝 Blog Toolkit

[![CI](https://github.com/rojasdali/blog-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/rojasdali/blog-toolkit)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

An agnostic, modular content engine and editorial toolkit designed to plan, research, generate, and publish bilingual SEO/AEO-optimized blog posts powered by Google Gemini AI.

Built for local businesses, e-commerce brands, and content sites needing a consistent **1–2x per week publishing cadence** with real brand imagery, strict editorial rulesets, and zero duplicate fluff.

---

## 🌟 Key Features

- **Agnostic Brand Rulesets**: Configure brand voice, tone, forbidden phrases, local geographic entities, target audiences, and categories in clean JSON/YAML.
- **1–2x Weekly Calendar Planner**: Automatically schedules publication dates, category distributions, and high-intent keyword targets without colliding with existing post slugs.
- **Answer Engine Optimization (AEO)**: Generates structured key takeaways, actionable tips, and modular section blocks specifically optimized for Google AI Overviews and LLMs.
- **Bilingual Parallel Generation**: Generates native Spanish and English content side-by-side with identical section structures and local dialect precision.
- **Authentic Image Catalog & Matcher**: Automatically maps topics to your authentic real-world photography catalog (e.g. store interior, machines, team, folding station) or generates precise photo prompts.
- **Multi-Format Exporters**:
  - **Next.js / React TypeScript**: Drop-in compatible with frontend array stores (e.g. `src/lib/blog/posts.ts`).
  - **Markdown**: Includes YAML frontmatter for Astro, Hugo, Next.js MDX, or Obsidian.
  - **JSON**: Direct structured payload for CMS or database ingestion.
- **CLI & Python SDK**: Use as a standalone command-line tool or import directly into your app.

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/rojasdali/blog-toolkit.git
cd blog-toolkit
pip install -e .
```

### 2. Environment Setup

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Generate a 4-Week Publishing Calendar

```bash
blog-toolkit plan --preset el_laundry --weeks 4
```

Output:
```text
📅 Content Plan for 'El Laundry' (2026-10-01 to 2026-10-25):
Cadence: 1.5 posts/week (Total: 6 posts)

1. [2026-10-01] (wash-and-fold) Guía de Lavado y Doblado en Hialeah: Cuánto Tiempo Realmente Ahorras
   Slug: /guia-lavado-doblado-ahorro-tiempo
   Keywords: lavado y doblado hialeah, wash and fold fl, lavanderia mismo dia
   Rationale: High conversion search intent for busy working families

2. [2026-10-05] (comforters) Por Qué No Debes Lavar tu Edredón King en Casa (Y Cómo Lavarlo sin Dañarlo)
   Slug: /como-lavar-edredon-king-lavadoras-gigantes
   Keywords: lavar edredon king, lavadoras gigantes 65 lbs, lavar plumon hialeah
   Rationale: High margin specialty item query
...
```

### 4. Generate a Structured Post

```bash
blog-toolkit generate \
  --topic "Cómo Lavar Edredones Gigantes en Hialeah" \
  --category "comforters" \
  --preset "el_laundry" \
  --format "ts"
```

---

## 🏛️ Architecture & Project Structure

```
blog-toolkit/
├── presets/                    # Brand rulesets and editorial configurations
│   ├── el_laundry.json         # El Laundry local business preset
│   └── default.json            # Generic brand template
├── src/blog_toolkit/
│   ├── core/                   # Domain types, BrandRuleset, config
│   ├── engine/                 # Gemini client, prompt engineering, planner, generator
│   ├── images/                 # Image catalog and topic matcher
│   ├── exporters/              # TypeScript, Markdown, and JSON exporters
│   ├── adapters/               # Application-specific adapters (e.g. El Laundry)
│   └── cli.py                  # Command-line interface
├── tests/                      # Pytest suite with 100% core coverage
└── examples/                   # Standalone scripts for automation
```

---

## 🧪 Testing & Code Quality

Run tests:
```bash
make test
```

Run linter:
```bash
make lint
```

Full check:
```bash
make check
```

---

## 📄 License

MIT © [Dali Rojas](https://github.com/rojasdali)
