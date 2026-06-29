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
{week['estimated_days']}
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

    return result