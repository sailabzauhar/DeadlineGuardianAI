import sqlite3

from .connection import (
    get_connection
)


def save_day(
    weekly_mission_id,
    day_data
):

    conn = get_connection()
    cursor = conn.cursor()

    status = "Locked"

    if day_data["day"] == 1:
        status = "Active"

    cursor.execute(
        """
        INSERT INTO daily_missions (
            weekly_mission_id,
            day,
            title,
            description,
            deliverable,
            success_criteria,
            estimated_hours,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            weekly_mission_id,
            day_data["day"],
            day_data["title"],
            day_data["description"],
            day_data["deliverable"],
            day_data["success_criteria"],
            day_data["estimated_hours"],
            status
        )
    )

    day_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return day_id


def get_days(
    weekly_mission_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_missions
        WHERE weekly_mission_id=?
        ORDER BY day
        """,
        (weekly_mission_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        dict(row)
        for row in rows
    ]


def get_active_day(
    weekly_mission_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_missions
        WHERE weekly_mission_id=?
        AND status='Active'
        ORDER BY day
        LIMIT 1
        """,
        (weekly_mission_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def get_active_day_by_week(
    week_id
):

    return get_active_day(
        week_id
    )