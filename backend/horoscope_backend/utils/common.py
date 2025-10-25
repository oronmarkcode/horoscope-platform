import re
from datetime import date, datetime
from typing import Optional

from zoneinfo import ZoneInfo


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
    return re.sub(
        r"^```(?:json)?\s*|\s*```$", "", s.strip(), flags=re.IGNORECASE | re.MULTILINE
    )
