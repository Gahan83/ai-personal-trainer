"""
AI Service Module (Azure OpenAI)

Thin wrapper around the Azure OpenAI chat completions API. Provides:
- chat: raw multi-message completion (conversational guidance)
- generate_completion: free-form text from a single prompt
- generate_json: structured output (used by the workout planner)

The service degrades gracefully when credentials are missing so the rest of
the app (DB, constraint engine, deterministic plan) keeps working offline.
"""

from typing import Optional, Dict, Any, List
import json

from app.core.config import settings

try:
    from openai import AzureOpenAI
except ImportError:  # pragma: no cover
    AzureOpenAI = None  # type: ignore


# Shared system prompt. Encodes the PRD's hard constraints so the model never
# violates them even if a downstream prompt forgets to restate them.
TRAINER_SYSTEM_PROMPT = """You are Gahan's personal AI strength & conditioning coach.

Profile: active individual in Bangalore. Trains 4x/week in the gym, plays
football 1x/week, takes 2 rest days. Goals: physique, strength, longevity —
NON-COMPETITIVE.

HARD CONSTRAINTS — never violate, ever:
1. NO abs/core direct work — not in warm-ups, finishers, or any suggestion.
2. Football day is a training day — never program a gym session the same day.
3. At least one full rest day between back-to-back hard sessions.
4. Never put leg day the day before football.
5. Keep everything non-competitive — physique, strength, longevity focus.

Style: concise, practical, encouraging. Use real exercise-science reasoning
(progressive overload, recovery, RPE). Give sets, reps, rest, and form cues
when relevant."""


class AIService:
    """Service for interacting with Azure OpenAI."""

    def __init__(self):
        self.api_key = getattr(settings, "OPENAI_API_KEY", "") or ""
        self.endpoint = getattr(settings, "AZURE_OPENAI_ENDPOINT", "") or ""
        self.api_version = getattr(settings, "AZURE_API_VERSION", "") or "2024-06-01"
        self.model = getattr(settings, "CHAT_MODEL", "gpt-4o-mini")

        # Capability flags, flipped on first 400 from the deployment.
        self._use_completion_tokens = False
        self._supports_temperature = True

        if AzureOpenAI and self.api_key and self.endpoint:
            self.client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.endpoint,
                api_version=self.api_version,
            )
        else:
            self.client = None

    @property
    def available(self) -> bool:
        return self.client is not None

    def _require_client(self):
        if not AzureOpenAI:
            raise ValueError("openai package not installed. Run: pip install openai")
        if not self.client:
            raise ValueError(
                "Azure OpenAI not configured. Set OPENAI_API_KEY and "
                "AZURE_OPENAI_ENDPOINT in your .env file."
            )

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 700,
        temperature: float = 0.7,
    ) -> str:
        """Run a chat completion. Prepends the trainer system prompt if the
        caller did not supply one.

        Handles newer Azure model deployments (GPT-5 family) that require
        ``max_completion_tokens`` instead of ``max_tokens`` and only accept the
        default temperature — retrying without the offending param on a 400.
        """
        self._require_client()
        if not messages or messages[0].get("role") != "system":
            messages = [{"role": "system", "content": TRAINER_SYSTEM_PROMPT}] + messages

        # Token-limit param name differs across model generations.
        token_kwarg = "max_completion_tokens" if self._use_completion_tokens else "max_tokens"
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            token_kwarg: max_tokens,
        }
        if self._supports_temperature:
            kwargs["temperature"] = temperature

        try:
            response = self.client.chat.completions.create(**kwargs)
        except Exception as e:
            msg = str(e)
            retried = False
            if "max_tokens" in msg and "max_completion_tokens" in msg:
                self._use_completion_tokens = True
                kwargs.pop("max_tokens", None)
                kwargs["max_completion_tokens"] = max_tokens
                retried = True
            if "temperature" in msg:
                self._supports_temperature = False
                kwargs.pop("temperature", None)
                retried = True
            if not retried:
                raise
            response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 700,
        temperature: float = 0.7,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt or TRAINER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        return self.chat(messages, max_tokens=max_tokens, temperature=temperature)

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1500,
    ) -> Dict[str, Any]:
        """Generate a JSON object response."""
        json_system = (system_prompt or TRAINER_SYSTEM_PROMPT) + (
            "\n\nRespond with valid JSON only. No markdown, no prose."
        )
        text = self.generate_completion(
            prompt=prompt,
            system_prompt=json_system,
            max_tokens=max_tokens,
            temperature=0.3,
        )
        return self._parse_json(text)

    @staticmethod
    def _parse_json(text: str) -> Dict[str, Any]:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI JSON response: {e}")


# Singleton. Calls raise a clear error if credentials are not configured.
ai_service = AIService()
