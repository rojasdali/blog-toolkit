"""Tests for inspector module parsing posts.ts."""

from blog_toolkit.engine.inspector import get_used_images, parse_existing_posts

SAMPLE_POSTS_TS = """
export const BLOG_POSTS = [
  {
    slug: "post-one-test",
    image: "/images/blog/img1.webp",
    category: "self-service",
    es: {
      title: "Título Uno",
      keywords: ["kw1", "kw2"]
    },
    en: {
      title: "Title One",
      keywords: ["kw3"]
    }
  },
  {
    slug: "post-two-test",
    image: "/images/blog/img2.webp",
    category: "commercial",
    es: {
      title: "Título Dos",
      keywords: ["kw4"]
    },
    en: {
      title: "Title Two",
      keywords: ["kw5"]
    }
  }
];
"""


def test_parse_existing_posts():
    posts = parse_existing_posts(SAMPLE_POSTS_TS)
    assert len(posts) == 2
    assert posts[0].slug == "post-one-test"
    assert posts[0].category == "self-service"
    assert "Título Uno" in posts[0].titles
    assert "kw1" in posts[0].keywords

    used = get_used_images(posts)
    assert "/images/blog/img1.webp" in used
    assert "/images/blog/img2.webp" in used


def test_parse_quoted_existing_posts():
    sample_quoted = """
    export const BLOG_POSTS = [
      {
      "slug": "fluff-and-fold-hialeah-ropa-por-libra",
      "date": "2026-10-09",
      "image": "/images/blog/wash-and-fold-neat-stack.webp",
      "category": "wash-and-fold",
      "es": {
        "title": "Fluff and Fold en Hialeah",
        "keywords": ["fluff and fold near me", "ropa por libra"]
      },
      "en": {
        "title": "Fluff and Fold in Hialeah",
        "keywords": ["wash and fold"]
      }
    }
    ];
    """
    posts = parse_existing_posts(sample_quoted)
    assert len(posts) == 1
    assert posts[0].slug == "fluff-and-fold-hialeah-ropa-por-libra"
    assert posts[0].category == "wash-and-fold"
    assert posts[0].image == "/images/blog/wash-and-fold-neat-stack.webp"
    assert "Fluff and Fold en Hialeah" in posts[0].titles
    assert "fluff and fold near me" in posts[0].keywords

