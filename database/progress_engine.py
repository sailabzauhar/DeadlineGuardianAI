from .connection import (
    get_connection
)

from .goals import (
    complete_goal
)


def complete_day(
    day_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE daily_missions
        SET status='Completed'
        WHERE id=?
        """,
        (day_id,)
    )

    conn.commit()
    conn.close()


def activate_next_day(
    weekly_mission_id,
    current_day
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM daily_missions
        WHERE weekly_mission_id=?
        AND day=?
        """,
        (
            weekly_mission_id,
            current_day + 1
        )
    )

    next_day = cursor.fetchone()

    if next_day:

        cursor.execute(
            """
            UPDATE daily_missions
            SET status='Active'
            WHERE weekly_mission_id=?
            AND day=?
            """,
            (
                weekly_mission_id,
                current_day + 1
            )
        )

    conn.commit()
    conn.close()


def all_tasks_completed(
    daily_mission_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_tasks
        WHERE daily_mission_id=?
        AND status='Pending'
        """,
        (daily_mission_id,)
    )

    pending = cursor.fetchone()[0]

    conn.close()

    return pending == 0


def get_week_progress(
    week_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_missions
        WHERE weekly_mission_id=?
        """,
        (week_id,)
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_missions
        WHERE weekly_mission_id=?
        AND status='Completed'
        """,
        (week_id,)
    )

    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return completed / total


def all_days_completed(
    week_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_missions
        WHERE weekly_mission_id=?
        AND status!='Completed'
        """,
        (week_id,)
    )

    remaining = cursor.fetchone()[0]

    conn.close()

    return remaining == 0


def complete_week(
    week_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE weekly_missions
        SET status='Completed'
        WHERE id=?
        """,
        (week_id,)
    )

    conn.commit()
    conn.close()


def activate_next_week(
    month_id,
    current_week
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM weekly_missions
        WHERE monthly_mission_id=?
        AND week=?
        """,
        (
            month_id,
            current_week + 1
        )
    )

    next_week = cursor.fetchone()

    if next_week:

        cursor.execute(
            """
            UPDATE weekly_missions
            SET status='Active'
            WHERE monthly_mission_id=?
            AND week=?
            """,
            (
                month_id,
                current_week + 1
            )
        )

    conn.commit()
    conn.close()


def all_weeks_completed(
    month_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM weekly_missions
        WHERE monthly_mission_id=?
        AND status!='Completed'
        """,
        (month_id,)
    )

    remaining = cursor.fetchone()[0]

    conn.close()

    return remaining == 0


def complete_month(
    month_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE monthly_missions
        SET status='Completed'
        WHERE id=?
        """,
        (month_id,)
    )

    conn.commit()
    conn.close()


def activate_next_month(
    goal_id,
    current_month
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM monthly_missions
        WHERE goal_id=?
        AND month=?
        """,
        (
            goal_id,
            current_month + 1
        )
    )

    next_month = cursor.fetchone()

    if next_month:

        cursor.execute(
            """
            UPDATE monthly_missions
            SET status='Active'
            WHERE goal_id=?
            AND month=?
            """,
            (
                goal_id,
                current_month + 1
            )
        )

        conn.commit()
        conn.close()

    else:

        conn.close()

        complete_goal(
            goal_id
        )