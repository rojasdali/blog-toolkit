# 📜 Operations Log: blog-toolkit

All major architectural decisions, schema evolutions, and toolkit updates.

---

## 2026-10-03 (Standardization & Graphify Integration)

### /graphify-build — Knowledge Graph Scaffolding
- **Operation**: graphify-build
- **Guardrails**: Added `tests/test_modularity.py` and `githooks/pre-commit` (hooking into `core.hooksPath = githooks`).
- **Modularity**: Verified 100% compliance (<120 LOC, complexity <= 10).
- **Knowledge Base**: Initialized `wiki/entities/`, `wiki/concepts/`, and `wiki/systems/` with compiled graph.

---

## 2026-10-07 (Semantic Anti-Duplication & Dynamic Striking Keywords Engine)

### Dynamic Targeting & Cannibalization Defense
- **Repurposed Duplicate Post**: Converted duplicate Wash & Fold post into `servicio-lavanderia-comercial-hialeah-b2b` targeting GSC striking-distance query `commercial laundry service hialeah` (Pos 11.2, 18 impr) with 301 permanent redirects in `next.config.ts`.
- **Semantic Anti-Duplication**: Implemented `ContentDeduplicator` utilizing token normalization and Jaccard similarity across titles, slugs, and keywords to mathematically block duplicate/cannibalizing article generation.
- **Dynamic Striking-Distance Targeting**: Integrated `dynamic_keywords` and `gsc_loader` to ingest live Google Search Console queries (positions 8.0-25.0) and prioritize high-opportunity search terms.
- **Image Uniqueness**: Expanded `DEFAULT_EL_LAUNDRY_IMAGES` and updated `ImageMatcher` to track `used_images`, preventing cover photo repetition across blog posts.
- **Modularity & Tests**: 100% compliance with strict Python modularity (<120 LOC, complexity <= 10). 28/28 unit tests passing.
