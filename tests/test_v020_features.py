"""Tests for v0.2.0 BrandProfile fields, Gemini 2.5 default, presets export, and check-topic CLI."""

import json

from blog_toolkit import BrandProfile, __version__
from blog_toolkit.cli import main
from blog_toolkit.engine.client import GeminiClient
from blog_toolkit.engine.prompts import build_system_prompt
from blog_toolkit.presets.el_laundry import get_el_laundry_profile


def test_version_and_gemini_default_model(monkeypatch):
    assert __version__ == "0.2.0"
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


def test_cli_check_topic_blocks_pillar_and_neighborhood(capsys):
    rc_pillar = main(
        ["check-topic", "Lavandería comercial para restaurantes y mantelería", "--json"]
    )
    out_pillar = json.loads(capsys.readouterr().out)
    assert rc_pillar == 1
    assert out_pillar["approved"] is False
    assert out_pillar["conflict"]["surface"] == "commercial"

    rc_nbh = main(["--json", "check-topic", "Lavandería cerca de Opa-locka"])
    out_nbh = json.loads(capsys.readouterr().out)
    assert rc_nbh == 1
    assert out_nbh["approved"] is False
    assert out_nbh["conflict"]["surface"] == "neighborhood"

    rc_clean = main(["check-topic", "Cómo impermeabilizar chaquetas técnicas de lluvia", "--json"])
    out_clean = json.loads(capsys.readouterr().out)
    assert rc_clean == 0
    assert out_clean["approved"] is True
