"""Tests for v0.2.0 BrandProfile fields, Gemini 2.5 default, presets export, and check-topic CLI."""

import json

from blog_toolkit import BrandProfile, __version__
from blog_toolkit.cli import main
from blog_toolkit.engine.client import GeminiClient
from blog_toolkit.engine.prompts import build_system_prompt
from blog_toolkit.presets.el_laundry import get_el_laundry_profile


def test_version_and_gemini_default_model(monkeypatch):
    assert __version__ == "0.2.1"
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    assert GeminiClient(api_key="k").model == "gemini-2.5-flash"
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash")
    assert GeminiClient(api_key="k").model == "gemini-2.5-flash"


def test_brand_profile_configurable_fields_and_prompt():
    profile = get_el_laundry_profile()
    assert isinstance(profile, BrandProfile)
    assert any("$1.00/lb" in fact for fact in profile.pricing_facts)
    assert "2:00 PM" in profile.cutoff_time
    assert "laundry mat" in profile.forbidden_terms

    prompt = build_system_prompt(profile)
    assert "$1.00/lb" in prompt
    assert "2:00 PM" in prompt
    assert "laundry mat" in prompt


def test_cli_check_topic_blocks_pillar_and_neighborhood(tmp_path, capsys):
    for rel, body in (
        (
            "src/lib/commercial/pillars.ts",
            'export const PILLARS = [\n  {\n    slug: "restaurantes-manteleria-hialeah",\n    es: {\n      title: "Lavandería Comercial para Restaurantes y Mantelería",\n      keywords: ["lavanderia para restaurantes hialeah"],\n    },\n  },\n];\n',
        ),
        (
            "src/lib/locations/neighborhoods.ts",
            'export const NEIGHBORHOODS = [\n  {\n    slug: "lavanderia-cerca-de-opa-locka",\n    es: {\n      title: "Lavandería Cerca de Opa-locka",\n      metaTitle: "Lavandería Cerca de Opa-locka: $1/lb | El Laundry",\n    },\n  },\n];\n',
        ),
    ):
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")

    root = str(tmp_path)
    rc_pillar = main(
        [
            "check-topic",
            "Lavandería comercial para restaurantes y mantelería",
            "--site-root",
            root,
            "--json",
        ]
    )
    out_pillar = json.loads(capsys.readouterr().out)
    assert rc_pillar == 1
    assert out_pillar["approved"] is False
    assert out_pillar["conflict"]["surface"] == "commercial"

    rc_nbh = main(
        ["--json", "check-topic", "Lavandería cerca de Opa-locka", "--site-root", root]
    )
    out_nbh = json.loads(capsys.readouterr().out)
    assert rc_nbh == 1
    assert out_nbh["approved"] is False
    assert out_nbh["conflict"]["surface"] == "neighborhood"

    rc_clean = main(
        [
            "check-topic",
            "Cómo impermeabilizar chaquetas técnicas de lluvia",
            "--site-root",
            root,
            "--json",
        ]
    )
    out_clean = json.loads(capsys.readouterr().out)
    assert rc_clean == 0
    assert out_clean["approved"] is True


def test_el_laundry_blocks_pr22_wrong_policies():
    from blog_toolkit.core.types import BlogPost, BlogSection, PostLocaleContent

    profile = get_el_laundry_profile()
    bad_post = BlogPost(
        slug="bad-policy-post",
        image="/images/blog/wash-and-fold-counter-team.webp",
        date="2026-11-10",
        read_time_minutes=4,
        author="Equipo El Laundry",
        category="wash-and-fold",
        es=PostLocaleContent(
            title="Guía de prueba para lavado por libra en Hialeah",
            excerpt="Deja antes de las 3:00 PM con mínimo 10 lbs de viernes a lunes.",
            keywords=["kw"],
            key_takeaways=["Takeaway suficientemente largo para pasar validacion"],
            sections=[BlogSection(heading="H", paragraphs=["Usa código para $10 OFF."])],
            category_label="Lavado y Doblado",
        ),
        en=PostLocaleContent(
            title="Sample wash and fold guide in Hialeah Sedanos",
            excerpt="Drop off before 3:00 PM with 10 lb min Friday through Monday.",
            keywords=["kw"],
            key_takeaways=["Sufficiently long key takeaway item for validation"],
            sections=[BlogSection(heading="H", paragraphs=["Claim $10 OFF today."])],
            category_label="Wash & Fold",
        ),
    )
    violations = profile.validate_post(bad_post)
    assert any("3:00 pm" in v.lower() for v in violations)
    assert any("10 lb" in v.lower() for v in violations)
    assert any("$10 off" in v.lower() for v in violations)
    assert any("viernes a lunes" in v.lower() for v in violations)
