"""Command-line interface for the agnostic blog toolkit."""

import argparse
import sys

from blog_toolkit.cli_handlers import (
    handle_check_topic,
    handle_curate,
    handle_generate,
    handle_plan,
)


def _shared_flags() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument(
        "--json", action="store_true", default=argparse.SUPPRESS, help="Output structured JSON"
    )
    return shared


def build_parser() -> argparse.ArgumentParser:
    shared = _shared_flags()
    parser = argparse.ArgumentParser(
        prog="blog-toolkit",
        description="Agnostic Blog Generation, Planning, and Multi-Surface Gatekeeper Toolkit.",
    )
    parser.add_argument("--json", action="store_true", help="Output structured JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_p = subparsers.add_parser(
        "plan", parents=[shared], help="Generate an editorial calendar plan."
    )
    plan_p.add_argument("--preset", default="el_laundry", help="Brand preset name")
    plan_p.add_argument("--weeks", type=int, default=4, help="Number of weeks to plan")

    gen_p = subparsers.add_parser("generate", parents=[shared], help="Generate a blog post.")
    gen_p.add_argument("--topic", required=True, help="Topic title to generate")
    gen_p.add_argument("--category", required=True, help="Category slug")
    gen_p.add_argument("--preset", default="el_laundry", help="Brand preset name")
    gen_p.add_argument("--date", default=None, help="Target publication date YYYY-MM-DD")
    gen_p.add_argument("--format", choices=["ts", "md", "json"], default="ts", help="Output format")
    gen_p.add_argument("--out", default=None, help="Output destination file")

    cur_p = subparsers.add_parser(
        "curate", parents=[shared], help="Curate and sync next post into Next.js app."
    )
    cur_p.add_argument("--site-root", default=None, help="Path to Next.js site root")
    cur_p.add_argument("--topic", default=None, help="Optional topic title")
    cur_p.add_argument("--category", default=None, help="Optional category slug")
    cur_p.add_argument("--date", default=None, help="Optional publication date")

    chk_p = subparsers.add_parser(
        "check-topic",
        parents=[shared],
        help="Check candidate topic against blog posts, commercial pillars, and neighborhoods.",
    )
    chk_p.add_argument(
        "topic_pos", nargs="?", default="", help="Candidate topic title, slug, or keyword"
    )
    chk_p.add_argument(
        "--topic", dest="topic_opt", default="", help="Candidate topic title (flag form)"
    )
    chk_p.add_argument("--site-root", default=None, help="Path to Next.js site root")
    chk_p.add_argument("--threshold", type=float, default=0.35, help="Jaccard similarity threshold")

    return parser


HANDLERS = {
    "plan": handle_plan,
    "generate": handle_generate,
    "curate": handle_curate,
    "check-topic": handle_check_topic,
}


def main(args: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    parsed = parser.parse_args(sys.argv[1:] if args is None else args)
    parsed.json = getattr(parsed, "json", False)
    return HANDLERS[parsed.command](parsed)


if __name__ == "__main__":
    sys.exit(main())
