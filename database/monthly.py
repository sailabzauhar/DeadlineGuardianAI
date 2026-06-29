import sqlite3

from .connection import (
    get_connection
)


def save_month(
    goal_id,
    month_data
):

    conn = get_connection()
    cursor = conn.cursor()

    status = "Locked"

    if month_data["month"] == 1:
        status = "Active"

    cursor.execute(
        """
        INSERT INTO monthly_missions (
            goal_id,
            month,
            title,
            description,
            deliverable,
            success_criteria,
            estimated_weeks,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            goal_id,
            month_data["month"],
            month_data["title"],
            month_data["description"],
            month_data["deliverable"],
            month_data["success_criteria"],
            month_data["estimated_weeks"],
            status
        )
    )

    month_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return month_id


def get_months(
    goal_id
):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM monthly_missions
        WHERE goal_id=?
        ORDER BY month
        """,
        (goal_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def get_goal_months(
    goal_id
):

    return get_months(
        goal_id
    )


def get_active_month(
    goal_id
):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM monthly_missions
        WHERE goal_id=?
        AND status='Active'
        ORDER BY month
        LIMIT 1
        """,
        (goal_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def get_active_month_by_goal(
    goal_id
):

    return get_active_month(
        goal_id
    )