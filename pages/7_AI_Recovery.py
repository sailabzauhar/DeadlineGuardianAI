import streamlit as st

from services.recovery_impact_service import (
    calculate_recovery_impact
)

from guardian_status_bar import (
    show_guardian_status_bar
)

from database import (
    get_active_goal,
    get_goal_progress,

    get_current_active_week,

    get_pending_tasks_by_week,
    get_completed_tasks_by_week,

    get_active_month_by_goal,
    get_active_day_by_week
)

from services.recovery_service import (
    generate_recovery_plan
)

from services.risk_service import (
    get_risk_level,
    get_schedule_gap,
    get_completion_probability,
    get_expected_progress,
    get_actual_progress
)

from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)

st.header("⚡ AI Recovery Mode")

quote = get_daily_motivation()

show_hero_quote(
    quote
)

st.info(
    "Missed tasks? Deadline Guardian will rebuild your execution plan automatically."
)

goal = get_active_goal()

if goal is None:

    st.info(
        "No active goal."
    )

    st.stop()

goal_id = goal[0]
goal_title = goal[1]
deadline = goal[2]

goal_progress = get_goal_progress(
    goal_id
)

active_month = get_active_month_by_goal(
    goal_id
)

active_week = get_current_active_week()

if active_week is None:

    st.success(
        "🎉 No active week found."
    )

    st.stop()

current_day = get_active_day_by_week(
    active_week["id"]
)

pending = get_pending_tasks_by_week(
    active_week["id"]
)

completed = get_completed_tasks_by_week(
    active_week["id"]
)

# ---------------------------------
# Recovery Analysis
# ---------------------------------

expected_progress = (
    get_expected_progress()
)

actual_progress = (
    get_actual_progress()
)

completion_probability = (
    get_completion_probability()
)

risk_level = (
    get_risk_level()
)

schedule_gap = (
    get_schedule_gap()
)

st.subheader(
    "🩺 Recovery Analysis"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Risk Level",
    risk_level
)

col2.metric(
    "Schedule Gap",
    f"{schedule_gap}%"
)

col3.metric(
    "Expected Progress",
    f"{expected_progress}%"
)

col4.metric(
    "Completion Chance",
    f"{completion_probability}%"
)

st.divider()

if risk_level == "Low":

    st.success(
        """
🟢 Guardian Diagnosis

You are currently on track.

Recovery Mode is not required.
"""
    )

elif risk_level == "Medium":

    st.warning(
        f"""
🟡 Guardian Diagnosis

You are approximately {abs(schedule_gap)}% behind schedule.

Recovery Mode may improve completion probability.
"""
    )

else:

    st.error(
        f"""
🔴 Guardian Diagnosis

High deadline risk detected.

You are approximately {abs(schedule_gap)}% behind schedule.

Recovery Mode is strongly recommended.
"""
    )

st.divider()

# ---------------------------------
# Recovery Decision
# ---------------------------------

if len(pending) == 0:

    st.success(
        "🎉 No pending tasks. Recovery Mode is not required."
    )

    st.stop()

if risk_level == "Low":

    st.success(
        """
🟢 You are currently on track.

Some pending tasks exist, but your overall progress is healthy.

Recovery Mode is not recommended at this time.
"""
    )

    st.stop()

st.warning(
    f"""
Recovery Opportunity Detected

Pending Tasks: {len(pending)}

Risk Level: {risk_level}

Schedule Gap: {schedule_gap}%

Deadline Guardian recommends rebuilding the execution plan.
"""
)

# ---------------------------------
# Generate Recovery Plan
# ---------------------------------

if st.button(
    "⚡ Generate Recovery Plan",
    use_container_width=True
):

    try:

        with st.spinner(
            "Analyzing schedule and rebuilding plan..."
        ):

            plan = generate_recovery_plan(
                goal_title,
                deadline,

                goal_progress,

                active_month,
                active_week,
                current_day,

                completed,
                pending
            )

            impact = calculate_recovery_impact(
                plan
            )

            from services.recovery_executor import (
                apply_recovery_plan
            )

            execution_result = (
                apply_recovery_plan(
                    active_week["id"],
                    plan
                )
            )

        st.success(
            "Recovery plan generated and applied successfully."
        )

        st.info(
            f"""
Deleted Pending Tasks: {execution_result['deleted_tasks']}

Created Recovery Tasks: {execution_result['created_tasks']}
"""
        )

        st.subheader(
            "🚑 Recovery Impact"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Before Recovery",
            f"{impact['before_probability']}%"
        )

        col2.metric(
            "After Recovery",
            f"{impact['after_probability']}%"
        )

        col3.metric(
            "Improvement",
            f"+{impact['improvement']}%"
        )

        st.subheader(
            "🧠 Guardian Analysis"
        )

        st.metric(
            "Risk Level",
            plan["risk_level"]
        )

        st.info(
            plan["strategy"]
        )

        st.subheader(
            "📋 Recovery Tasks"
        )

        for task in plan["tasks"]:

            st.markdown(
                f"""
### Day {task['day']}

**{task['title']}**

{task['description']}

⏳ Estimated Hours: {task['estimated_hours']}

---
"""
            )

        st.subheader(
            "🛡️ Guardian Verdict"
        )

        if impact["improvement"] > 15:

            st.success(
                "Recovery Mode significantly improves your chance of finishing before the deadline."
            )

        elif impact["improvement"] > 5:

            st.warning(
                "Recovery Mode provides moderate improvement. Stay consistent."
            )

        else:

            st.info(
                "Recovery impact is limited. Consider adjusting scope or deadline."
            )

        if st.button(
            "🔄 Refresh Mission Page"
        ):
            st.rerun()

    except Exception as e:

        st.error(
            f"Recovery failed: {str(e)}"
        )