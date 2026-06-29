import sqlite3

from .connection import (
    get_connection
)


def save_week(
    monthly_mission_id,
    week_data
):

    conn = get_connection()
    cursor = conn.cursor()

    status = "Locked"

    if week_data["week"] == 1:
        status = "Active"

    cursor.execute(
        """
        INSERT INTO weekly_missions (
            monthly_mission_id,
            week,
            title,
            description,
            deliverable,
            success_criteria,
            estimated_days,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            monthly_mission_id,
            week_data["week"],
            week_data["title"],
            week_data["description"],
            week_data["deliverable"],
            week_data["success_criteria"],
            week_data["estimated_days"],
            status
        )
    )

    week_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return week_id


def get_weeks(
    monthly_mission_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM weekly_missions
        WHERE monthly_mission_id=?
        ORDER BY week
        """,
        (monthly_mission_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def get_active_week(
    monthly_mission_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM weekly_missions
        WHERE monthly_mission_id=?
        AND status='Active'
        ORDER BY week
        LIMIT 1
        """,
        (monthly_mission_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def get_active_week_by_month(
    month_id
):

    return get_active_week(
        month_id
    )


def get_current_active_week():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM weekly_missions
        WHERE status='Active'
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None