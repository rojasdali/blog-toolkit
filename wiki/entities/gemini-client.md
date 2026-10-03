---
type: entity
title: Gemini Client
created: 2026-10-03
updated: 2026-10-03
aliases: [gemini-client]
tags: [ai, gemini, adapter]
---

# Gemini Client

## Summary
The Gemini client adapter wraps Google Generative AI APIs to produce structured JSON responses conforming to editorial schemas for post outlines and drafts.

## Key Facts
- Uses system instructions to enforce authentic business voice and prevent generic filler.
- Enforces bilingual translation symmetry between Spanish and English.
- Supports configurable temperature and token limits to maintain output predictability.

## Relationships
- [[blog-toolkit]] — Invoked by the generator engine
- [[aeo-key-takeaways]] — Constrained to output data-dense facts

## For AI
- **Type**: entity
- **Confidence**: high
- **Last verified**: 2026-10-03
