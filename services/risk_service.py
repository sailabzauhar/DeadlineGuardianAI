from datetime import datetime

from database import (
    get_active_goal,
    get_goal_progress
)


def get_expected_progress():

    goal = get_active_goal()

    if goal is None:
        return 0

    
    deadline = goal[2]

    created_at = goal[3]

    start_date = datetime.strptime(
        created_at[:10],
        "%Y-%m-%d"
    ).date()

    deadline_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    ).date()

    today = datetime.today().date()

    total_days = (
        deadline_date - start_date
    ).days

    elapsed_days = (
        today - start_date
    ).days

    if total_days <= 0:
        return 100

    expected = (
        elapsed_days / total_days
    ) * 100

    expected = max(
        0,
        min(
            100,
            expected
        )
    )

    return int(expected)


def get_actual_progress():

    goal = get_active_goal()

    if goal is None:
        return 0

    progress = (
        get_goal_progress(
            goal[0]
        ) * 100
    )

    return int(progress)


def get_schedule_gap():

    expected = (
        get_expected_progress()
    )

    actual = (
        get_actual_progress()
    )

    return actual - expected


def get_risk_level():

    gap = (
        get_schedule_gap()
    )

    if gap >= 0:
        return "Low"

    elif gap >= -15:
        return "Medium"

    else:
        return "High"


def get_completion_probability():

    expected = (
        get_expected_progress()
    )

    actual = (
        get_actual_progress()
    )

    if expected == 0:
        return 90

    performance_ratio = (
        actual / expected
    )

    probability = (
        performance_ratio * 100
    )

    probability += (
        actual * 0.20
    )

    probability = max(
        5,
        min(
            95,
            probability
        )
    )

    return int(
        probability
    )