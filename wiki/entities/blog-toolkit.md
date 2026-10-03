---
type: entity
title: Blog Toolkit
created: 2026-10-03
updated: 2026-10-03
aliases: [blog-toolkit]
tags: [toolkit, blog, seo, aeo]
---

# Blog Toolkit

## Summary
The `blog-toolkit` is an agnostic, modular Python library for automated editorial planning, AI-assisted bilingual content generation, authentic photo matching, and TypeScript / Next.js export.

## Key Facts
- Generates bilingual articles (Spanish and English) with matching schema and URL slugs.
- Matches authentic photography from an asset catalog without using generative AI imagery.
- Strictly adheres to clean architecture: all modules < 120 lines and cyclomatic complexity <= 10.

## Relationships
- [[gemini-client]] — AI generation adapter for topic outlines and body text
- [[authentic-photo-matching]] — Logic for pairing articles with real brand photography
- [[aeo-key-takeaways]] — Answer Engine Optimization rule enforcement
- [[editorial-calendar]] — Multi-week topic planning and scheduling
- [[typescript-export]] — AST generation for Next.js blog posts

## For AI
- **Type**: entity
- **Confidence**: high
- **Last verified**: 2026-10-03
