"""Synchronizes generated blog posts to llms.txt endpoints."""

from pathlib import Path

from blog_toolkit.core.types import BlogPost


def sync_post_to_llms_txt(site_root: Path, post: BlogPost) -> None:
    """Synchronize the new post into content-es.ts and content-en.ts."""
    llms_dir = site_root / "src" / "app" / "llms.txt"
    es_file = llms_dir / "content-es.ts"
    en_file = llms_dir / "content-en.ts"

    if es_file.exists():
        c_es = es_file.read_text(encoding="utf-8")
        if post.slug not in c_es:
            entry = f"- [{post.es.title}](https://el-laundry.com/blog/{post.slug}): {post.es.excerpt}\n"
            marker = "## Páginas de Servicios Comerciales (B2B)"
            if marker in c_es:
                c_es = c_es.replace(marker, f"{entry}\n{marker}")
                es_file.write_text(c_es, encoding="utf-8")

    if en_file.exists():
        c_en = en_file.read_text(encoding="utf-8")
        if post.slug not in c_en:
            entry = f"- [{post.en.title}](https://el-laundry.com/en/blog/{post.slug}): {post.en.excerpt}\n"
            marker = "## Commercial Service Pages (B2B)"
            if marker in c_en:
                c_en = c_en.replace(marker, f"{entry}\n{marker}")
                en_file.write_text(c_en, encoding="utf-8")
