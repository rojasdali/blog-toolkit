"""Tests for prompt builder module."""

from blog_toolkit.core.ruleset import BrandRuleset
from blog_toolkit.engine.prompts import build_system_prompt, build_user_prompt
from blog_toolkit.engine.types import GenerationRequest


def test_build_system_prompt():
    ruleset = BrandRuleset.from_preset("el_laundry")
    sys_prompt = build_system_prompt(ruleset)

    assert "El Laundry" in sys_prompt
    assert "Hialeah" in sys_prompt
    assert "laundry mat" in sys_prompt
    assert "BlogPost" in sys_prompt


def test_build_user_prompt():
    ruleset = BrandRuleset.from_preset("el_laundry")
    req = GenerationRequest(
        topic="Servicio de Lavandería Comercial para Airbnb",
        category="commercial",
        target_keywords=["airbnb laundry", "hialeah"],
    )
    user_prompt = build_user_prompt(req, ruleset, "/images/blog/towels.webp")

    assert "Servicio de Lavandería Comercial para Airbnb" in user_prompt
    assert "commercial" in user_prompt
    assert "/images/blog/towels.webp" in user_prompt
