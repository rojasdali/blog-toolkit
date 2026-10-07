"""Semantic anti-duplication and cannibalization defense engine."""

import re

from blog_toolkit.engine.types import ExistingPostSummary

STOPWORDS: set[str] = {
    "de", "en", "la", "el", "los", "las", "un", "una", "unos", "unas",
    "con", "por", "para", "y", "o", "a", "del", "al",
    "the", "in", "of", "and", "for", "to", "on", "with", "at", "by", "from",
}


def normalize_tokens(text: str) -> set[str]:
    """Tokenize and normalize words, removing stopwords and plurals."""
    words = re.findall(r"[a-záéíóúüñ0-9]+", text.lower())
    tokens: set[str] = set()
    for w in words:
        if w in STOPWORDS or len(w) <= 1:
            continue
        if w.endswith("as") or w.endswith("es") or w.endswith("os"):
            w = w[:-2]
        elif w.endswith("s"):
            w = w[:-1]
        tokens.add(w)
    return tokens


def jaccard_similarity(s1: set[str], s2: set[str]) -> float:
    """Compute Jaccard similarity between two token sets."""
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


class ContentDeduplicator:
    """Detects semantic cannibalization and duplicates against existing posts."""

    def __init__(self, existing_posts: list[ExistingPostSummary]):
        self.existing = existing_posts

    def _check_post_match(
        self,
        post: ExistingPostSummary,
        c_slug: str,
        cand_slug_toks: set[str],
        cand_title_toks: set[str],
        cand_kw_toks: set[str],
    ) -> tuple[bool, str]:
        """Check if candidate conflicts with a specific existing post."""
        if post.slug == c_slug:
            return True, f"Exact slug match with existing post '{post.slug}'"

        slug_sim = jaccard_similarity(cand_slug_toks, normalize_tokens(post.slug.replace("-", " ")))
        if slug_sim >= 0.50:
            return True, f"Slug collision ({slug_sim:.0%}) with '{post.slug}'"

        for title in post.titles:
            title_sim = jaccard_similarity(cand_title_toks, normalize_tokens(title))
            if title_sim >= 0.40:
                return True, f"Title similarity ({title_sim:.0%}) with '{post.slug}': '{title}'"

        if post.keywords and cand_kw_toks:
            kw_sim = jaccard_similarity(cand_kw_toks, normalize_tokens(" ".join(post.keywords)))
            if kw_sim >= 0.45:
                return True, f"Keyword overlap ({kw_sim:.0%}) with '{post.slug}'"

        return False, ""

    def is_duplicate(
        self,
        topic: str,
        keywords: list[str],
        slug: str,
    ) -> tuple[bool, str, str | None]:
        """Verify if a candidate topic conflicts with any existing post."""
        cand_slug_toks = normalize_tokens(slug.replace("-", " "))
        cand_title_toks = normalize_tokens(topic)
        cand_kw_toks = normalize_tokens(" ".join(keywords))

        for post in self.existing:
            is_dup, reason = self._check_post_match(
                post, slug, cand_slug_toks, cand_title_toks, cand_kw_toks
            )
            if is_dup:
                return True, reason, post.slug

        return False, "", None
