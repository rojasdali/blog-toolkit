"""Subcommand handlers for the blog-toolkit CLI."""

import argparse
import json

from blog_toolkit.adapters.el_laundry import ElLaundryAdapter
from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.generator import BlogGenerator
from blog_toolkit.engine.planner import ContentPlanner
from blog_toolkit.engine.types import GenerationRequest
from blog_toolkit.exporters.json_exporter import JsonExporter
from blog_toolkit.exporters.markdown_exporter import MarkdownExporter
from blog_toolkit.exporters.typescript_exporter import TypeScriptExporter


def handle_plan(args: argparse.Namespace) -> int:
    ruleset = BrandRuleset.from_preset(args.preset)
    plan = ContentPlanner(ruleset).plan_calendar(weeks=args.weeks)
    if args.json:
        print(plan.model_dump_json(indent=2))
        return 0
    print(f"\n📅 Content Plan for '{plan.brand_name}' ({plan.start_date} to {plan.end_date}):")
    print(f"Cadence: {plan.cadence_per_week} posts/week (Total: {len(plan.topics)} posts)\n")
    for i, t in enumerate(plan.topics, 1):
        print(
            f"{i}. [{t.target_date}] ({t.category}) {t.topic}\n   Slug: /{t.slug}\n   Keywords: {', '.join(t.target_keywords)}\n"
        )
    return 0


def handle_generate(args: argparse.Namespace) -> int:
    ruleset = BrandRuleset.from_preset(args.preset)
    req = GenerationRequest(topic=args.topic, category=args.category, target_date=args.date)
    post = BlogGenerator(ruleset).generate(req)
    fmt = "json" if args.json else args.format
    exporter_map = {
        "ts": TypeScriptExporter().export,
        "md": MarkdownExporter().export,
        "json": JsonExporter().export,
    }
    output = exporter_map[fmt](post)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output)
        if args.json:
            print(json.dumps({"saved": args.out, "slug": post.slug}, indent=2))
        else:
            print(f"Saved post to {args.out}")
    else:
        print(output)
    return 0


def handle_curate(args: argparse.Namespace) -> int:
    adapter = ElLaundryAdapter(site_root=args.site_root)
    post = adapter.curate_next_post(topic=args.topic, category=args.category, target_date=args.date)
    if args.json:
        print(post.model_dump_json(indent=2))
        return 0
    print(
        f"\n✅ Successfully curated and synced blog post:\n   Slug: /{post.slug}\n   Title (ES): {post.es.title}\n   Title (EN): {post.en.title}"
    )
    return 0


def handle_check_topic(args: argparse.Namespace) -> int:
    topic = (args.topic_pos or args.topic_opt or "").strip()
    if not topic:
        raise ValueError("Provide a candidate topic via positional argument or --topic.")
    adapter = ElLaundryAdapter(site_root=args.site_root)
    result = adapter.check_topic(topic, threshold=args.threshold)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif result["approved"]:
        print(
            f"✅ APPROVED: Zero cannibalization across {result['surfaces_scanned']} surfaces for '{topic}'."
        )
    else:
        c = result["conflict"]
        print(
            f"❌ CANNIBALIZATION BLOCKED: Conflicts with {c['surface']} '{c['slug']}' ({c['similarity']:.0%}: '{c['title']}')."
        )
    return 0 if result["approved"] else 1
