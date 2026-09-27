"""Command-line interface for the agnostic blog toolkit."""

import argparse
import sys

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.exporters.json_exporter import JsonExporter
from blog_toolkit.exporters.markdown_exporter import MarkdownExporter
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


def main(args: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="blog-toolkit",
        description="Agnostic Blog Generation, Planning, and Publishing Toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: plan
    plan_parser = subparsers.add_parser("plan", help="Generate an editorial calendar plan.")
    plan_parser.add_argument("--preset", default="el_laundry", help="Brand preset name")
    plan_parser.add_argument("--weeks", type=int, default=4, help="Number of weeks to plan")

    # Subcommand: generate
    gen_parser = subparsers.add_parser("generate", help="Generate a blog post.")
    gen_parser.add_argument("--topic", required=True, help="Topic title to generate")
    gen_parser.add_argument("--category", required=True, help="Category slug")
    gen_parser.add_argument("--preset", default="el_laundry", help="Brand preset name")
    gen_parser.add_argument("--date", default=None, help="Target publication date YYYY-MM-DD")
    gen_parser.add_argument("--format", choices=["ts", "md", "json"], default="ts", help="Format")
    gen_parser.add_argument("--out", default=None, help="Output destination file")

    parsed = parser.parse_args(args or sys.argv[1:])

    if parsed.command == "plan":
        ruleset = BrandRuleset.from_preset(parsed.preset)
        planner = ContentPlanner(ruleset)
        plan = planner.plan_calendar(weeks=parsed.weeks)
        print(f"\n📅 Content Plan for '{plan.brand_name}' ({plan.start_date} to {plan.end_date}):")
        print(f"Cadence: {plan.cadence_per_week} posts/week (Total: {len(plan.topics)} posts)\n")
        for i, t in enumerate(plan.topics, 1):
            print(f"{i}. [{t.target_date}] ({t.category}) {t.topic}")
            print(f"   Slug: /{t.slug}")
            print(f"   Keywords: {', '.join(t.target_keywords)}")
            print(f"   Rationale: {t.rationale}\n")
        return 0

    if parsed.command == "generate":
        ruleset = BrandRuleset.from_preset(parsed.preset)
        generator = BlogGenerator(ruleset)
        req = GenerationRequest(
            topic=parsed.topic, category=parsed.category, target_date=parsed.date
        )
        post = generator.generate(req)

        if parsed.format == "ts":
            output = TypeScriptExporter().export(post)
        elif parsed.format == "md":
            output = MarkdownExporter().export(post)
        else:
            output = JsonExporter().export(post)

        if parsed.out:
            with open(parsed.out, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Saved post to {parsed.out}")
        else:
            print(output)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
