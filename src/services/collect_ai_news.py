import textwrap
from datetime import datetime
from typing import Any

import requests
from icecream import ic

from src.config import settings


class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

    pass


class PerplexityClient:
    """Client for interacting with the Perplexity API."""

    BASE_URL = "https://api.perplexity.ai/chat/completions"

    def __init__(self):
        if not settings.perplexity_api_key:
            raise ConfigurationError("Perplexity API key is required")

        self.api_key = settings.perplexity_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ============================
    # ✅ PUBLIC METHOD
    # ============================

    def get_update(
        self, topic: str, max_tokens: int = 150, temperature: float = 0.3
    ) -> dict[str, Any]:
        """
        Fetch daily tech updates and return structured response:
        {
            "response": "...",
            "citations": [...]
        }
        """
        prompt_messages = self._build_weekly_prompt(topic)

        payload = {
            "model": "sonar",
            "messages": prompt_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "return_citations": True,
        }

        response = requests.post(
            self.BASE_URL, headers=self.headers, json=payload, timeout=30
        )
        response.raise_for_status()

        result = response.json()

        # ✅ 1. Parse response into components
        parsed_response = self._parse_response(result)

        # ✅ 2. Send billing separately (you will implement later)
        self._handle_billing(result)

        # ✅ 3. Return ONLY what frontend needs
        return parsed_response

    # ============================
    # 🔒 PRIVATE: PROMPT BUILDER
    # ============================

    def _build_daily_prompt(self, topic: str) -> list[dict[str, str]]:
        """
        Private function to build prompt.
        Currently hardcoded as requested.
        """
        current_date = datetime.now().strftime("%B %d, %Y")

        system_prompt = textwrap.dedent(
            f"""
            You are a strict tech change-log generator.
            Today's date is {current_date}.

            Task:
            - Output ONLY 3–6 bullet points
            - Each point must describe a REAL, CONCRETE update in the tech world related to {topic}.
            - Focus ONLY on:
            • New version releases
            • Security patches
            • Major feature drops
            • Acquisitions, funding, shutdowns
            • Breaking infrastructure changes

            HARD RULES:
            - NO opinions
            - NO praise
            - NO explanations
            - NO history
            - NO marketing language
            - NO "praised", "popular", "widely used", "continues to", etc.
            - ONE update per bullet
            - ONE line per bullet

            Required Output Format (STRICT):
            • <Product/Framework> <version or event> — <what changed> - <important detail or impact>

            Example:
            • FastAPI 0.111 released — adds HTTP/3 support
            • Python 3.14 beta 2 released — improves JIT compilation
    "
            """
        ).strip()

        user_prompt = f"""
        What are today's most important developments and news in {topic}?
        Focus on framework updates, new releases, acquisitions, product launches,
        and market-impacting announcements. Include sources.
        """.strip()

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _build_weekly_prompt(self, topic: str) -> list[dict[str, str]]:
        """
        Builds a strict weekly changelog prompt.
        """
        today = datetime.now()
        week_range = f"{(today).strftime('%B %d, %Y')} (last 7 days)"

        system_prompt = textwrap.dedent(
            f"""
            You are a strict WEEKLY tech change-log generator.
            Time window: LAST 8 DAYS.
            Reference date: {week_range}.

            Task:
            - Output ONLY 5–8 bullet points
            - Each point must be a REAL, CONFIRMED event from the last week
            - Focus ONLY on HIGH-IMPACT updates related to {topic}

            Allowed categories:
            • Major version releases
            • Security patches / CVEs
            • Large feature rollouts
            • Acquisitions, funding, shutdowns
            • Breaking infrastructure or policy changes

            HARD RULES:
            - NO opinions
            - NO analysis
            - NO speculation
            - NO history
            - NO marketing language
            - NO repeated events
            - ONE update per bullet
            - ONE line per bullet

            Required Output Format (STRICT):
            • <Product/Framework> <version or event> — <what changed> - <impact or constraint>

            Example:
            • Python 3.13.1 released — fixes multiple security vulnerabilities - affects stdlib SSL
            • OpenAI policy update — changes data retention rules - impacts enterprise APIs
            """
        ).strip()

        user_prompt = f"""
        List the most important and verifiable developments from the last 7 days in {topic}.
        Include sources.
        """.strip()

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _parse_response(self, result: dict[str, Any]) -> dict[str, Any]:
        """
        Breaks API response into:
        - actual user response
        - citations
        """

        # ✅ Main user-facing content
        user_response = result["choices"][0]["message"]["content"]

        # ✅ Citations (handled separately by your URL handler)
        citations = result.get("citations", [])

        structured_response = {"response": user_response, "citations": citations}

        return structured_response

    # ============================
    # 🔒 PRIVATE: BILLING HANDLER
    # ============================

    def _handle_billing(self, result: dict[str, Any]) -> None:
        """
        Extracts billing info and sends it to your billing system.
        You said to leave this empty for now.
        """

        usage = result.get("usage", {})
        cost = usage.get("cost", {})

        billing_payload = {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "total_cost": cost.get("total_cost"),
        }
        ic(billing_payload)
        return billing_payload
