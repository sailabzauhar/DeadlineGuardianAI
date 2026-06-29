from services.gemini_service import (
    GeminiService
)

from prompts.task_prompt import (
    TASK_PROMPT
)

from utils.json_helper import (
    extract_json
)

gemini = GeminiService()


def generate_tasks(
    day
):

    prompt = f"""
{TASK_PROMPT}

DAY:
{day['day']}

TITLE:
{day['title']}

DESCRIPTION:
{day['description']}

DELIVERABLE:
{day['deliverable']}

SUCCESS CRITERIA:
{day['success_criteria']}

ESTIMATED HOURS:
{day['estimated_hours']}
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
            "Gemini returned an invalid task JSON."
        )

    if "tasks" not in result:

        raise Exception(
            "Task JSON missing tasks field."
        )

    if len(result["tasks"]) == 0:

        raise Exception(
            "Task planner returned zero tasks."
        )

    return result