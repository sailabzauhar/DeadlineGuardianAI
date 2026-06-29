from services.risk_service import (
    get_completion_probability
)


def calculate_recovery_impact(
    recovery_plan
):

    before_probability = (
        get_completion_probability()
    )

    risk = recovery_plan.get(
        "risk_level",
        "Medium"
    )

    tasks = recovery_plan.get(
        "tasks",
        []
    )

    task_count = len(
        tasks
    )

    # -------------------------
    # Base Improvement
    # -------------------------

    if risk == "Low":

        improvement = 5

    elif risk == "Medium":

        improvement = 10

    else:

        improvement = 15

    # -------------------------
    # Recovery Strength Bonus
    # -------------------------

    improvement += min(
        10,
        task_count * 2
    )

    after_probability = min(
        95,
        before_probability +
        improvement
    )

    return {

        "before_probability":
        before_probability,

        "after_probability":
        after_probability,

        "improvement":
        after_probability -
        before_probability,

        "task_count":
        task_count
    }