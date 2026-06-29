from .connection import (
    get_connection
)


def add_goal(
    title,
    deadline
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE goals
        SET status='Archived'
        WHERE status='Active'
        """
    )

    cursor.execute(
        """
        INSERT INTO goals (
            title,
            deadline,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            deadline,
            "Active"
        )
    )

    goal_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return goal_id


def get_goals():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            deadline,
            status,
            created_at
        FROM goals
        ORDER BY created_at DESC
        """
    )

    goals = cursor.fetchall()

    conn.close()

    return goals


def get_goal_history():

    return get_goals()


def get_latest_goal():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM goals
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    return row


def get_latest_goal_id():

    goal = get_latest_goal()

    if goal is None:
        return None

    return goal[0]


def complete_goal(
    goal_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE goals
        SET status='Completed'
        WHERE id=?
        """,
        (goal_id,)
    )

    conn.commit()
    conn.close()


def get_active_goal():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM goals
        WHERE status='Active'
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    return row


def get_active_goal_id():

    goal = get_active_goal()

    if goal is None:
        return None

    return goal[0]


def get_goal_status(
    goal_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM goals
        WHERE id=?
        """,
        (goal_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]


def get_completed_goals_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM goals
        WHERE status='Completed'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_archived_goals_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM goals
        WHERE status='Archived'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_goal_success_rate():

    completed = (
        get_completed_goals_count()
    )

    archived = (
        get_archived_goals_count()
    )

    total = completed + archived

    if total == 0:

        return 100

    return int(
        completed /
        total *
        100
    )