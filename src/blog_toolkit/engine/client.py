"""Gemini client wrapper with structured JSON output and fallback support."""

import json
import os

from blog_toolkit.core.types import BlogPost


class GeminiClient:
    """Interface for invoking Gemini models to generate structured blog content."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY", "")).strip()
        self.model = (model or os.getenv("GEMINI_MODEL") or "gemini-3.5-flash").strip()

    def generate_post_json(self, system_prompt: str, user_prompt: str) -> dict:
        """Call Gemini to generate a post conforming to BlogPost schema."""
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Please set the GEMINI_API_KEY environment "
                "variable or pass it to GeminiClient(api_key=...)."
            )

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=BlogPost,
                    temperature=0.3,
                ),
            )
            raw = response.text or "{}"
            return json.loads(raw)
        except Exception as exc:
            return self._fallback_legacy_sdk(system_prompt, user_prompt, exc)

    def _fallback_legacy_sdk(
        self, system_prompt: str, user_prompt: str, original_exc: Exception
    ) -> dict:
        """Fallback to google.generativeai if google.genai encounters an error."""
        try:
            import google.generativeai as gai

            gai.configure(api_key=self.api_key)
            model = gai.GenerativeModel(
                model_name=self.model,
                system_instruction=system_prompt,
                generation_config={"response_mime_type": "application/json"},
            )
            resp = model.generate_content(user_prompt)
            return json.loads(resp.text or "{}")
        except Exception as fallback_exc:
            raise RuntimeError(
                f"Failed to generate post with Gemini. Error: {original_exc} (Fallback: {fallback_exc})"
            ) from original_exc
