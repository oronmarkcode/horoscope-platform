import asyncio
import json
from datetime import date

from backend.horoscope_backend.core.config import settings
from backend.horoscope_backend.services.ai.openai_client import (
    OpenAIProvider,
    OpenAIProviderConfig,
)
from backend.horoscope_backend.services.horoscope_ai_service.horoscope_ai_service import (
    HoroscopeAIService,
)


async def main() -> None:
    provider_config = OpenAIProviderConfig(
        model=settings.openai_model,
    )

    provider = OpenAIProvider(config=provider_config)
    service = HoroscopeAIService(provider=provider, default_tz="Europe/Amsterdam")

    result = await service.generate_horoscope(
        name="Alice",
        dob=date(1990, 5, 17),
        tz="Europe/Amsterdam",
        variation=0,
        strict=True,
    )

    print(
        json.dumps(
            {
                "headline": result.headline,
                "reading": result.reading,
                "lucky_color": result.lucky_color,
                "lucky_number": result.lucky_number,
                "mood": result.mood,
                "focus": result.focus,
                "do": result.do,
                "dont": result.dont,
                "best_time_window": result.best_time_window,
                "compatibility_sign": result.compatibility_sign,
                "usage": result.usage,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
