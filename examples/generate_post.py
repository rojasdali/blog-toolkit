"""Example: Generating a post and exporting to Next.js TypeScript format."""

import os

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("Note: Set GEMINI_API_KEY environment variable to generate live with Gemini.")
        return

    ruleset = BrandRuleset.from_preset("el_laundry")
    generator = BlogGenerator(ruleset)

    req = GenerationRequest(
        topic="Lavado de Edredones Gigantes y Colchas en Hialeah",
        category="comforters",
        target_keywords=["lavar edredon hialeah", "lavadoras gigantes 65 lbs"],
    )

    print(f"Generating post for: {req.topic}...")
    post = generator.generate(req)

    print("\n--- Generated Post in TypeScript Format ---")
    print(TypeScriptExporter().export(post))


if __name__ == "__main__":
    main()
