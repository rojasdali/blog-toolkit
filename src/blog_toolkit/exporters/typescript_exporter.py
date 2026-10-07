"""TypeScript exporter formatting posts for Next.js / React projects."""

import json
import re

from blog_toolkit.core.types import BlogPost


class TypeScriptExporter:
    """Exports a BlogPost to a clean TypeScript object."""

    @staticmethod
    def _clean_sections(sections: list[dict]) -> list[dict]:
        cleaned = []
        for s in sections:
            item = {
                "heading": s["heading"],
                "paragraphs": s["paragraphs"],
            }
            if s.get("bullets"):
                item["bullets"] = s["bullets"]
            if s.get("callout"):
                item["callout"] = s["callout"]
            cleaned.append(item)
        return cleaned

    @staticmethod
    def _replace_canonical_phone(text: str) -> str:
        phone_pattern = r"(?:\+1[-.\s]?)?\(?786\)?[-.\s]?803[-.\s]?8622"

        def replacer(match):
            content = match.group(1)
            new_content = re.sub(phone_pattern, "${BUSINESS_PHONE_DISPLAY}", content)
            return f"`{new_content}`"

        return re.sub(r"\"([^\"\n]*" + phone_pattern + r"[^\"\n]*)\"", replacer, text)

    def export(self, post: BlogPost) -> str:
        """Convert BlogPost to a TypeScript code snippet."""
        raw_dict = post.model_dump()
        es_slug = raw_dict["es"].get("slug") or raw_dict["slug"]
        en_slug = raw_dict["en"].get("slug") or raw_dict["slug"]

        # Format into clean camelCase TypeScript structure
        ts_obj = {
            "slug": raw_dict["slug"],
            "date": raw_dict["date"],
            "readTimeMinutes": raw_dict["read_time_minutes"],
            "featured": raw_dict["featured"],
            "author": raw_dict["author"],
            "image": raw_dict["image"],
            "category": raw_dict["category"],
            "es": {
                "slug": es_slug,
                "title": raw_dict["es"]["title"],
                "excerpt": raw_dict["es"]["excerpt"],
                "keywords": raw_dict["es"]["keywords"],
                "keyTakeaways": raw_dict["es"]["key_takeaways"],
                "sections": self._clean_sections(raw_dict["es"]["sections"]),
                "categoryLabel": raw_dict["es"]["category_label"],
            },
            "en": {
                "slug": en_slug,
                "title": raw_dict["en"]["title"],
                "excerpt": raw_dict["en"]["excerpt"],
                "keywords": raw_dict["en"]["keywords"],
                "keyTakeaways": raw_dict["en"]["key_takeaways"],
                "sections": self._clean_sections(raw_dict["en"]["sections"]),
                "categoryLabel": raw_dict["en"]["category_label"],
            },
        }

        # Convert to formatted JS/TS object code
        json_str = json.dumps(ts_obj, ensure_ascii=False, indent=2)
        return self._replace_canonical_phone(json_str)

    def append_to_posts_file(self, post: BlogPost, file_path: str) -> None:
        """Append the generated post into a Next.js posts.ts file."""
        code = self.export(post)
        with open(file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            # Find the closing array bracket
            closing_idx = content.rfind("];")
            if closing_idx == -1:
                closing_idx = content.rfind("]")
            if closing_idx == -1:
                raise ValueError(f"Could not find closing array bracket in {file_path}")

            prefix = content[:closing_idx].rstrip()
            if not prefix.endswith(","):
                prefix += ","
            new_content = f"{prefix}\n  {code}\n{content[closing_idx:]}"
            f.seek(0)
            f.write(new_content)
            f.truncate()
