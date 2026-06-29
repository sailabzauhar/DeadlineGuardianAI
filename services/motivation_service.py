from datetime import date

from services.gemini_service import (
    GeminiService
)

from database import (
    get_active_goal,
    get_goal_progress
)

gemini = GeminiService()

_cache = {
    "date": None,
    "quote": "आज का अनुशासन कल की सफलता का आधार है"
}


def get_daily_motivation():

    today = str(
        date.today()
    )

    if _cache["date"] == today:

        return _cache["quote"]

    goal = get_active_goal()

    if goal is None:

        return (
            "आज का अनुशासन कल की सफलता का आधार है"
        )

    goal_title = goal[1]

    progress = int(
        get_goal_progress(
            goal[0]
        ) * 100
    )

    prompt = f"""
You are Deadline Guardian AI.

USER GOAL:
{goal_title}

GOAL PROGRESS:
{progress}%

Generate one powerful Hindi motivational quote.

Rules:

1. Must be related to the user's goal.
2. Must feel personal.
3. Maximum 20 words.
4. Hindi only.
5. No emojis.
6. No quotation marks.
7. Return only the quote.
"""

    try:

        quote = gemini.generate(
            prompt
        ).strip()

        if len(quote) > 0:

            _cache["date"] = today
            _cache["quote"] = quote

    except Exception:

        pass

    return _cache["quote"]