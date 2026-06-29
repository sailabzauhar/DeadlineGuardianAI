import sqlite3
from datetime import datetime

from .connection import (
    get_connection
)


def save_daily_task(
    daily_mission_id,
    task_data
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO daily_tasks(
            daily_mission_id,
            task,
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
            daily_mission_id,
            task_data["task"],
            task_data["title"],
            task_data["description"],
            task_data["deliverable"],
            task_data["success_criteria"],
            task_data["estimated_hours"],
            "Pending"
        )
    )

    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return task_id


def get_daily_tasks(
    daily_mission_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_tasks
        WHERE daily_mission_id=?
        ORDER BY task
        """,
        (daily_mission_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def complete_daily_task(
    task_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE daily_tasks
        SET
            status='Completed',
            completed_at=?
        WHERE id=?
        """,
        (
            datetime.now().isoformat(),
            task_id
        )
    )

    conn.commit()
    conn.close()


def get_active_tasks(
    daily_mission_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_tasks
        WHERE daily_mission_id=?
        AND status='Pending'
        ORDER BY task
        """,
        (daily_mission_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_completed_daily_tasks():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_tasks
        WHERE status='Completed'
        ORDER BY completed_at DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_pending_daily_tasks():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_tasks
        WHERE status='Pending'
        ORDER BY created_at
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_total_task_count(goal_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_tasks dt
        JOIN daily_missions dm
            ON dt.daily_mission_id = dm.id
        JOIN weekly_missions wm
            ON dm.weekly_mission_id = wm.id
        JOIN monthly_missions mm
            ON wm.monthly_mission_id = mm.id
        WHERE mm.goal_id = ?
        """,
        (goal_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count



def get_completed_task_count(goal_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_tasks dt
        JOIN daily_missions dm
            ON dt.daily_mission_id = dm.id
        JOIN weekly_missions wm
            ON dm.weekly_mission_id = wm.id
        JOIN monthly_missions mm
            ON wm.monthly_mission_id = mm.id
        WHERE
            mm.goal_id = ?
            AND dt.status='Completed'
        """,
        (goal_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_pending_tasks_by_week(
    week_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT dt.*
        FROM daily_tasks dt
        JOIN daily_missions dm
        ON dt.daily_mission_id = dm.id
        WHERE dm.weekly_mission_id=?
        AND dt.status='Pending'
        ORDER BY dm.day, dt.task
        """,
        (week_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def get_completed_tasks_by_week(
    week_id
):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT dt.*
        FROM daily_tasks dt
        JOIN daily_missions dm
        ON dt.daily_mission_id = dm.id
        WHERE dm.weekly_mission_id=?
        AND dt.status='Completed'
        ORDER BY dt.completed_at DESC
        """,
        (week_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def delete_pending_tasks_by_week(
    week_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM daily_tasks
        WHERE id IN (

            SELECT dt.id
            FROM daily_tasks dt
            JOIN daily_missions dm
            ON dt.daily_mission_id = dm.id

            WHERE dm.weekly_mission_id=?
            AND dt.status='Pending'

        )
        """,
        (week_id,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted


def save_recovery_task(
    daily_mission_id,
    task_number,
    title,
    description,
    estimated_hours
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO daily_tasks(

            daily_mission_id,
            task,
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
            daily_mission_id,
            task_number,
            title,
            description,
            "Recovery Deliverable",
            "Task Completed",
            estimated_hours,
            "Pending"
        )
    )

    conn.commit()
    conn.close()