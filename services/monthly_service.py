import math
from datetime import datetime

from utils.json_helper import (
    extract_json
)

from services.automation_service import (
    bootstrap_goal
)

from services.gemini_service import (
    GeminiService
)

from prompts.monthly_prompt import (
    SYSTEM_PROMPT
)

from database import (
    add_goal,
    save_month,
    get_goal_months
)

gemini = GeminiService()


def generate_plan(
    goal,
    deadline,
    mode
):

    today = datetime.today().date()

    deadline_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    ).date()

    days_remaining = (
        deadline_date - today
    ).days

    if days_remaining <= 0:

        raise Exception(
            "Deadline must be in the future."
        )

    number_of_months = max(
        1,
        math.ceil(
            days_remaining / 30
        )
    )

    prompt = f"""
{SYSTEM_PROMPT}

USER TYPE:
{mode}

GOAL:
{goal}

DEADLINE:
{deadline}

AVAILABLE DAYS:
{days_remaining}

NUMBER OF MONTHS:
{number_of_months}
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

        plan = extract_json(
            cleaned
        )

    except Exception:

        raise Exception(
            "Gemini returned an invalid JSON response. Please try again."
        )

    if "months" not in plan:

        raise Exception(
            "Planner JSON missing months field."
        )

    if len(
        plan["months"]
    ) == 0:

        raise Exception(
            "Planner returned zero months."
        )

    goal_id = add_goal(
        goal,
        deadline
    )

    for month in plan["months"]:

        save_month(
            goal_id,
            month
        )

    months = get_goal_months(
        goal_id
    )

    if months:

        bootstrap_goal(
            goal_id,
            months[0]
        )

    plan["goal_id"] = goal_id

    return plan