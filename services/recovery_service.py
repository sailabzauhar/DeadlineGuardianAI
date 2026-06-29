import json

from services.gemini_service import (
    GeminiService
)

from prompts.recovery_prompt import (
    RECOVERY_PROMPT
)

from utils.json_helper import (
    extract_json
)

gemini = GeminiService()


def generate_recovery_plan(
    goal,
    deadline,
    goal_progress,
    current_month,
    current_week,
    current_day,
    completed_tasks,
    pending_tasks
):

    prompt = f"""
{RECOVERY_PROMPT}

GOAL:
{goal}

DEADLINE:
{deadline}

GOAL PROGRESS:
{goal_progress}

CURRENT MONTH:
{current_month}

CURRENT WEEK:
{current_week}

CURRENT DAY:
{current_day}

COMPLETED TASKS:
{json.dumps(completed_tasks, indent=2)}

PENDING TASKS:
{json.dumps(pending_tasks, indent=2)}
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
            "Recovery engine returned invalid JSON."
        )

    required_fields = [
        "risk_level",
        "strategy",
        "tasks"
    ]

    for field in required_fields:

        if field not in plan:

            raise Exception(
                f"Recovery JSON missing '{field}' field."
            )

    if len(plan["tasks"]) == 0:

        raise Exception(
            "Recovery engine returned zero recovery tasks."
        )

    return plan