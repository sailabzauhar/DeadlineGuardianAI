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

    total_weeks = max(
        1,
        math.ceil(
            days_remaining / 7
        )
    )

    number_of_months = max(
        1,
        math.ceil(
            total_weeks / 4
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

TOTAL WEEKS:
{total_weeks}

NUMBER OF MONTHS:
{number_of_months}

IMPORTANT:

1. The entire roadmap must fit within TOTAL WEEKS.
2. Do not assume every month contains 4 weeks.
3. If TOTAL WEEKS is 5:
   Month 1 = 4 weeks
   Month 2 = 1 week
4. If TOTAL WEEKS is 6:
   Month 1 = 4 weeks
   Month 2 = 2 weeks
5. If TOTAL WEEKS is 3:
   Create only 1 month.
6. Never create extra time beyond the deadline.
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