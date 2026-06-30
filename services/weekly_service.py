from services.gemini_service import (
    GeminiService
)

from prompts.weekly_prompt import (
    WEEKLY_PROMPT
)

from utils.json_helper import (
    extract_json
)

gemini = GeminiService()


def generate_weekly_missions(
    month
):

    estimated_weeks = (
        month["estimated_weeks"]
    )

    prompt = f"""
{WEEKLY_PROMPT}

MONTH:
{month['month']}

TITLE:
{month['title']}

DESCRIPTION:
{month['description']}

DELIVERABLE:
{month['deliverable']}

SUCCESS CRITERIA:
{month['success_criteria']}

ESTIMATED WEEKS:
{estimated_weeks}

IMPORTANT:

Generate EXACTLY {estimated_weeks} weekly missions.

Do not generate fewer weeks.
Do not generate more weeks.

Week numbering must start at 1.
Week numbering must remain sequential.
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
            "Gemini returned an invalid weekly mission JSON."
        )

    if "weeks" not in result:

        raise Exception(
            "Weekly JSON missing weeks field."
        )

    if len(result["weeks"]) == 0:

        raise Exception(
            "Weekly planner returned zero weeks."
        )

    if len(result["weeks"]) != estimated_weeks:

        raise Exception(
            f"Weekly planner generated {len(result['weeks'])} weeks instead of {estimated_weeks}."
        )

    return result