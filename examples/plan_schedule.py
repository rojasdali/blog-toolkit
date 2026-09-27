"""Example: Planning a 4-week content calendar with El Laundry preset."""

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.planner import ContentPlanner


def main():
    ruleset = BrandRuleset.from_preset("el_laundry")
    planner = ContentPlanner(ruleset)

    plan = planner.plan_calendar(weeks=4)
    print(f"\nContent Plan for {plan.brand_name}:")
    print(f"Cadence: {plan.cadence_per_week} posts/week\n")

    for i, t in enumerate(plan.topics, 1):
        print(f"{i}. Date: {t.target_date} [{t.category}]")
        print(f"   Topic: {t.topic}")
        print(f"   Slug: /{t.slug}")
        print(f"   Keywords: {', '.join(t.target_keywords)}\n")


if __name__ == "__main__":
    main()
