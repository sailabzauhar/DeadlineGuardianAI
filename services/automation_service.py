from services.weekly_service import (
    generate_weekly_missions
)

from services.daily_service import (
    generate_daily_missions
)

from services.task_service import (
    generate_tasks
)

from database import (
    save_week,
    save_day,
    save_daily_task,

    get_weeks,
    get_days,
    get_daily_tasks
)


def bootstrap_goal(
    goal_id,
    first_month
):

    weekly_plan = generate_weekly_missions(
        first_month
    )

    if "weeks" not in weekly_plan:

        raise Exception(
            "Weekly planner returned invalid data."
        )

    for week in weekly_plan["weeks"]:

        save_week(
            first_month["id"],
            week
        )

    weeks = get_weeks(
        first_month["id"]
    )

    if len(weeks) == 0:
        return

    week_one = weeks[0]

    daily_plan = generate_daily_missions(
        week_one
    )

    if "days" not in daily_plan:

        raise Exception(
            "Daily planner returned invalid data."
        )

    for day in daily_plan["days"]:

        save_day(
            week_one["id"],
            day
        )

    days = get_days(
        week_one["id"]
    )

    if len(days) == 0:
        return

    day_one = days[0]

    task_plan = generate_tasks(
        day_one
    )

    if "tasks" not in task_plan:

        raise Exception(
            "Task planner returned invalid data."
        )

    for task in task_plan["tasks"]:

        save_daily_task(
            day_one["id"],
            task
        )


def bootstrap_day(
    day
):

    existing_tasks = get_daily_tasks(
        day["id"]
    )

    if len(existing_tasks) > 0:
        return

    task_plan = generate_tasks(
        day
    )

    if "tasks" not in task_plan:

        raise Exception(
            "Task planner returned invalid data."
        )

    for task in task_plan["tasks"]:

        save_daily_task(
            day["id"],
            task
        )


def bootstrap_week(
    week
):

    existing_days = get_days(
        week["id"]
    )

    if len(existing_days) > 0:
        return

    daily_plan = generate_daily_missions(
        week
    )

    if "days" not in daily_plan:

        raise Exception(
            "Daily planner returned invalid data."
        )

    for day in daily_plan["days"]:

        save_day(
            week["id"],
            day
        )

    days = get_days(
        week["id"]
    )

    if len(days) == 0:
        return

    bootstrap_day(
        days[0]
    )


def bootstrap_month(
    month
):

    existing_weeks = get_weeks(
        month["id"]
    )

    if len(existing_weeks) > 0:
        return

    weekly_plan = generate_weekly_missions(
        month
    )

    if "weeks" not in weekly_plan:

        raise Exception(
            "Weekly planner returned invalid data."
        )

    for week in weekly_plan["weeks"]:

        save_week(
            month["id"],
            week
        )

    weeks = get_weeks(
        month["id"]
    )

    if len(weeks) == 0:
        return

    bootstrap_week(
        weeks[0]
    )