"""Command-line interface for the agnostic blog toolkit."""

import argparse
import sys

from blog_toolkit.adapters.el_laundry import ElLaundryAdapter
from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.exporters.json_exporter import JsonExporter
from blog_toolkit.exporters.markdown_exporter import MarkdownExporter
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


def _handle_plan(args: argparse.Namespace) -> int:
    ruleset = BrandRuleset.from_preset(args.preset)
    planner = ContentPlanner(ruleset)
    plan = planner.plan_calendar(weeks=args.weeks)
    print(f"\n📅 Content Plan for '{plan.brand_name}' ({plan.start_date} to {plan.end_date}):")
    print(f"Cadence: {plan.cadence_per_week} posts/week (Total: {len(plan.topics)} posts)\n")
    for i, t in enumerate(plan.topics, 1):
        print(f"{i}. [{t.target_date}] ({t.category}) {t.topic}")
        print(f"   Slug: /{t.slug}")
        print(f"   Keywords: {', '.join(t.target_keywords)}")
        print(f"   Rationale: {t.rationale}\n")
    return 0


def _handle_generate(args: argparse.Namespace) -> int:
    ruleset = BrandRuleset.from_preset(args.preset)
    generator = BlogGenerator(ruleset)
    req = GenerationRequest(topic=args.topic, category=args.category, target_date=args.date)
    post = generator.generate(req)

    exporter_map = {
        "ts": TypeScriptExporter().export,
        "md": MarkdownExporter().export,
        "json": JsonExporter().export,
    }
    output = exporter_map[args.format](post)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved post to {args.out}")
    else:
        print(output)
    return 0


def _handle_curate(args: argparse.Namespace) -> int:
    adapter = ElLaundryAdapter(site_root=args.site_root)
    post = adapter.curate_next_post(
        topic=args.topic,
        category=args.category,
        target_date=args.date,
    )
    print("\n✅ Successfully curated and synced blog post:")
    print(f"   Slug: /{post.slug}")
    print(f"   Category: {post.category}")
    print(f"   Title (ES): {post.es.title}")
    print(f"   Title (EN): {post.en.title}")
    print(f"   Cover Image: {post.image}")
    print(f"   Takeaways: {len(post.es.key_takeaways)} AEO points")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blog-toolkit",
        description="Agnostic Blog Generation, Planning, and Publishing Toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # plan
    plan_p = subparsers.add_parser("plan", help="Generate an editorial calendar plan.")
    plan_p.add_argument("--preset", default="el_laundry", help="Brand preset name")
    plan_p.add_argument("--weeks", type=int, default=4, help="Number of weeks to plan")

    # generate
    gen_p = subparsers.add_parser("generate", help="Generate a blog post.")
    gen_p.add_argument("--topic", required=True, help="Topic title to generate")
    gen_p.add_argument("--category", required=True, help="Category slug")
    gen_p.add_argument("--preset", default="el_laundry", help="Brand preset name")
    gen_p.add_argument("--date", default=None, help="Target publication date YYYY-MM-DD")
    gen_p.add_argument("--format", choices=["ts", "md", "json"], default="ts", help="Format")
    gen_p.add_argument("--out", default=None, help="Output destination file")

    # curate
    cur_p = subparsers.add_parser("curate", help="Curate and sync next post into Next.js app.")
    cur_p.add_argument("--site-root", default=None, help="Path to Next.js site root")
    cur_p.add_argument("--topic", default=None, help="Optional topic title")
    cur_p.add_argument("--category", default=None, help="Optional category slug")
    cur_p.add_argument("--date", default=None, help="Optional publication date")

    return parser


def main(args: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    parsed = parser.parse_args(args or sys.argv[1:])

    handlers = {
        "plan": _handle_plan,
        "generate": _handle_generate,
        "curate": _handle_curate,
    }
    return handlers[parsed.command](parsed)


if __name__ == "__main__":
    sys.exit(main())
