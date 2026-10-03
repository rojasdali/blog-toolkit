---
type: system
title: TypeScript Export
created: 2026-10-03
updated: 2026-10-03
aliases: [typescript-export]
tags: [codegen, typescript, exporter]
---

# TypeScript Export

## Summary
The serialization system compiles in-memory article objects into typed TypeScript code for direct inclusion in Next.js web application codebases (`src/lib/blog/posts.ts`).

## Key Facts
- Outputs strictly valid TypeScript matching target application interfaces.
- Serializes bilingual content side-by-side with slug cross-linking.
- Validates code structure prior to file writes to prevent syntax regressions.

## Relationships
- [[blog-toolkit]] — Invoked via CLI or SDK export command
- [[authentic-photo-matching]] — Embeds matched asset imports
- [[editorial-calendar]] — Consumes calendar metadata for published dates

## For AI
- **Type**: system
- **Confidence**: high
- **Last verified**: 2026-10-03
