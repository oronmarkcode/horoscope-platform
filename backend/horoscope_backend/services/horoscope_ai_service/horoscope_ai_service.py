import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from zodiac_sign import get_zodiac_sign
from zoneinfo import ZoneInfo

from ..ai.ai_provider_base import (
    AIProvider,
    ChatInput,
    Role,
)


class HoroscopeServiceError(Exception):
    pass


class JSONParseError(HoroscopeServiceError):
    def __init__(self, raw_text: str):
        super().__init__("Failed to parse model output as JSON.")
        self.raw_text = raw_text


class InvalidPayloadError(HoroscopeServiceError):
    def __init__(self, payload: Dict[str, Any]):
        super().__init__("Parsed JSON is missing required fields.")
        self.payload = payload


def today_in_tz(tz: str) -> date:
    try:
        return datetime.now(ZoneInfo(tz)).date()
    except Exception:
        return datetime.utcnow().date()


def clean_name(name: Optional[str]) -> str:
    if not name:
        return "friend"
    name = name.strip()
    return re.sub(r"[^A-Za-zÀ-ÿ' \-]", "", name)[:40] or "friend"


def strip_code_fences(s: str) -> str:
    """Remove markdown code fences like ```json ... ``` from model output."""
    return re.sub(
        r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.IGNORECASE | re.MULTILINE
    )


@dataclass
class HoroscopeResult:
    headline: str
    reading: str
    lucky_color: str
    lucky_number: int
    mood: str
    focus: List[str]
    do: List[str]
    dont: List[str]
    best_time_window: str

    compatibility_sign: Optional[str] = None
    raw_text: Optional[str] = None
    finish_reason: Optional[str] = None
    usage: Dict[str, int] = None


class HoroscopeAIService:
    def __init__(self, provider: AIProvider, default_tz: str = "Europe/Amsterdam"):
        self.provider = provider
        self.default_tz = default_tz

    async def generate_horoscope(
        self,
        *,
        name: Optional[str],
        dob: date,
        tz: Optional[str] = None,
        on_date: Optional[date] = None,
        variation: int = 0,
        strict: bool = False,
    ) -> HoroscopeResult:
        if not isinstance(dob, date):
            raise HoroscopeServiceError("`dob` must be a datetime.date instance.")

        safe_name = clean_name(name)
        tz = tz or self.default_tz
        today = on_date or today_in_tz(tz)
        sign = get_zodiac_sign(dob.month, dob.day)

        system_prompt = """
You are a friendly astrologer.

TASK
Return EXACTLY ONE JSON object that matches the schema below. Do not include markdown, code fences, prose, or explanations. Output must be valid JSON.

STYLE
• Uplifting, practical, non-deterministic.
• No medical, legal, or financial advice.

SCHEMA (order keys exactly as listed)
{
  "headline": string (≤140 chars),
  "reading": string (120–180 words, plain text),
  "lucky_color": string (single word or simple color name),
  "lucky_number": integer (1–99),
  "mood": one of ["calm","confident","curious","playful","focused"],
  "focus": array of 2–3 short strings,
  "do": array of exactly 3 short strings (imperative),
  "dont": array of exactly 2 short strings (imperative, positive phrasing without “not” if possible),
  "best_time_window": string "HH:MM–HH:MM" 24h format,
  "compatibility_sign": optional string (one of the 12 zodiac signs) — OMIT this key if unknown
}

RULES
• Do not add extra keys.
• Arrays must contain strings only (no emojis-only items).
• Use the user’s name in "headline" or first sentence of "reading".
• Mention the zodiac sign in the reading.
• Keep claims general; avoid absolutes.
"""

        user_prompt = f"""
Name: {safe_name}
Zodiac sign: {sign}
Date: {today.isoformat()}
Timezone: {tz}
Variation: {variation}

Output: Return the JSON object ONLY, with keys in the specified order.
"""

        out = await self.provider.generate(
            ChatInput(
                messages=[
                    {"role": Role.SYSTEM, "content": system_prompt},
                    {"role": Role.USER, "content": user_prompt},
                ]
            )
        )
        parsed = self._parse_json(out.get("text", ""))

        if not self._looks_ok(parsed):
            retry_user_prompt = (
                user_prompt
                + "\nYour previous output was invalid. Return ONE valid JSON object ONLY. No markdown or commentary."
            )
            out2 = await self.provider.generate(
                ChatInput(
                    messages=[
                        {"role": Role.SYSTEM, "content": system_prompt},
                        {"role": Role.USER, "content": retry_user_prompt},
                    ]
                )
            )
            parsed = self._parse_json(out2.get("text", ""))

            if not self._looks_ok(parsed):
                if strict:
                    if not parsed:
                        raise JSONParseError(out2.get("text", ""))
                    raise InvalidPayloadError(parsed)
                parsed = self._fallback_payload(safe_name, sign)
                return self._to_result(parsed, out2.get("text"), out2.get("usage", {}))

            return self._to_result(parsed, out2.get("text"), out2.get("usage", {}))

        return self._to_result(parsed, out.get("text"), out.get("usage", {}))

    def _parse_json(self, text: str) -> Dict[str, Any]:
        if not text:
            return {}
        body = strip_code_fences(text)
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", body, flags=re.DOTALL)
            if not m:
                return {}
            try:
                return json.loads(m.group(0))
            except Exception:
                return {}

    def _looks_ok(self, p: Dict[str, Any]) -> bool:
        if not isinstance(p, dict):
            return False
        required = [
            "headline",
            "reading",
            "lucky_color",
            "lucky_number",
            "mood",
            "focus",
            "do",
            "dont",
            "best_time_window",
        ]
        return all(k in p for k in required)

    def _clamp_int(self, n: Any, lo: int, hi: int) -> int:
        try:
            x = int(n)
        except Exception:
            x = lo
        return max(lo, min(hi, x))

    def _fallback_payload(self, name: str, sign: str) -> Dict[str, Any]:
        """Provide a safe default horoscope if parsing fails."""
        return {
            "headline": f"Hi {name} — a steady day for a {sign}.",
            "reading": f"Keep it simple and kind today, {name}. One small win will set the tone.",
            "lucky_color": "indigo",
            "lucky_number": 7,
            "mood": "calm",
            "focus": ["self-care", "planning"],
            "do": [
                "Take one focused action",
                "Send a quick thank-you",
                "Go for a short walk",
            ],
            "dont": ["Overcommit", "Skip breaks"],
            "best_time_window": "10:00–12:00",
        }

    def _to_result(
        self, p: Dict[str, Any], raw_text: Optional[str], meta: Dict[str, Any]
    ) -> HoroscopeResult:
        return HoroscopeResult(
            headline=str(p.get("headline", "A balanced day awaits."))[:140],
            reading=str(
                p.get("reading", "Stay patient and kind today; small wins add up.")
            )[:900],
            lucky_color=str(p.get("lucky_color", "indigo"))[:30],
            lucky_number=self._clamp_int(p.get("lucky_number", 7), 1, 99),
            mood=str(p.get("mood", "calm"))[:20],
            focus=[str(x) for x in (p.get("focus") or [])][:3]
            or ["self-care", "planning"],
            do=[str(x) for x in (p.get("do") or [])][:3]
            or [
                "Take one focused action",
                "Check in with a friend",
                "Tidy a small space",
            ],
            dont=[str(x) for x in (p.get("dont") or [])][:2]
            or ["Overcommit", "Skip breaks"],
            best_time_window=str(p.get("best_time_window", "10:00–12:00")),
            compatibility_sign=p.get("compatibility_sign"),
            raw_text=raw_text,
            finish_reason=None,
            usage=meta or {},
        )
