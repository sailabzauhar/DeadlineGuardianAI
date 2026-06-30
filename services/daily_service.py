from services.gemini_service import (
    GeminiService
)

from prompts.daily_prompt import (
    DAILY_PROMPT
)

from utils.json_helper import (
    extract_json
)

gemini = GeminiService()


def generate_daily_missions(
    week
):

    estimated_days = (
        week["estimated_days"]
    )

    prompt = f"""
{DAILY_PROMPT}

WEEK:
{week['week']}

TITLE:
{week['title']}

DESCRIPTION:
{week['description']}

DELIVERABLE:
{week['deliverable']}

SUCCESS CRITERIA:
{week['success_criteria']}

ESTIMATED DAYS:
{estimated_days}

IMPORTANT:

Generate EXACTLY {estimated_days} daily missions.

Do not generate fewer days.
Do not generate more days.

Day numbering must start from 1.
Day numbering must remain sequential.
"""

    response = gemini.generate(
        prompt
    )

    cleaned = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        result = extract_json(
            cleaned
        )

    except Exception:

        raise Exception(
            "Gemini returned an invalid daily mission JSON."
        )

    if "days" not in result:

        raise Exception(
            "Daily JSON missing days field."
        )

    if len(result["days"]) == 0:

        raise Exception(
            "Daily planner returned zero days."
        )

    if len(result["days"]) != estimated_days:

        raise Exception(
            f"Daily planner generated {len(result['days'])} days instead of {estimated_days}."
        )

    return result