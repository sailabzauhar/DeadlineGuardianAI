from .connection import (
    get_connection
)

from .tasks import (
    get_total_task_count,
    get_completed_task_count
)


def get_daily_task_progress(
    daily_mission_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_tasks
        WHERE daily_mission_id=?
        """,
        (daily_mission_id,)
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_tasks
        WHERE daily_mission_id=?
        AND status='Completed'
        """,
        (daily_mission_id,)
    )

    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return completed / total


def get_month_progress(
    month_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM weekly_missions
        WHERE monthly_mission_id=?
        """,
        (month_id,)
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM weekly_missions
        WHERE monthly_mission_id=?
        AND status='Completed'
        """,
        (month_id,)
    )

    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return completed / total


def get_goal_progress(
    goal_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monthly_missions
        WHERE goal_id=?
        """,
        (goal_id,)
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM monthly_missions
        WHERE goal_id=?
        AND status='Completed'
        """,
        (goal_id,)
    )

    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return completed / total


def get_productivity_score(
    goal_id
):

    if goal_id is None:
        return 0

    total = get_total_task_count(
        goal_id
    )

    if total == 0:
        return 0

    completed = get_completed_task_count(
        goal_id
    )

    return int(
        completed / total * 100
    )