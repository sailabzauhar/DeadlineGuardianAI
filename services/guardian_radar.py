from database import (
    get_active_goal,
    get_total_task_count,
    get_completed_task_count
)

from services.risk_service import (
    get_risk_level,
    get_completion_probability
)


def get_guardian_radar():

    goal = get_active_goal()

    if goal is None:

        return {
            "risk": "Unknown",
            "reason": "No active goal.",
            "recommendation": "Create a goal."
        }

    goal_id = goal[0]

    total_tasks = (
        get_total_task_count(
            goal_id
        )
    )

    completed_tasks = (
        get_completed_task_count(
            goal_id
        )
    )

    pending_tasks = (
        total_tasks -
        completed_tasks
    )

    risk = (
        get_risk_level()
    )

    probability = (
        get_completion_probability()
    )

    if risk == "Low":

        reason = (
            "Progress is on track."
        )

        recommendation = (
            "Continue current execution plan."
        )

    elif risk == "Medium":

        reason = (
            f"{pending_tasks} tasks remain unfinished."
        )

        recommendation = (
            "Increase focus and monitor progress."
        )

    else:

        reason = (
            f"{pending_tasks} pending tasks are creating deadline risk."
        )

        recommendation = (
            "Run Recovery Mode immediately."
        )

    return {

        "risk": risk,
        "probability": probability,
        "reason": reason,
        "recommendation": recommendation
    }