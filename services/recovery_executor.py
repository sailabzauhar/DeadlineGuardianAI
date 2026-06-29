from database import (
    delete_pending_tasks_by_week,
    save_recovery_task,
    get_active_day_by_week
)


def apply_recovery_plan(
    week_id,
    recovery_plan
):

    deleted = (
        delete_pending_tasks_by_week(
            week_id
        )
    )

    current_day = (
        get_active_day_by_week(
            week_id
        )
    )

    if current_day is None:

        raise Exception(
            "No active day found."
        )

    day_id = current_day["id"]

    task_number = 1

    for task in recovery_plan["tasks"]:

        save_recovery_task(
            day_id,
            task_number,
            task["title"],
            task["description"],
            task["estimated_hours"]
        )

        task_number += 1

    return {
        "deleted_tasks": deleted,
        "created_tasks": len(
            recovery_plan["tasks"]
        )
    }