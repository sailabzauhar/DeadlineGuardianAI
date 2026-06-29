import streamlit as st

from services.risk_service import (
    get_risk_level,
    get_schedule_gap,
    get_completion_probability
)

from database import get_active_goal_id


def show_guardian_alert():

    goal_id = get_active_goal_id()

    if goal_id is None:

        st.info(
            "🎯 Create your first goal to activate Guardian Intelligence."
        )

        return

    risk = get_risk_level()

    gap = get_schedule_gap()

    probability = (
        get_completion_probability()
    )

    if risk == "Low":

        st.success(
            f"""
🟢 GUARDIAN STATUS: SAFE

Completion Probability: {probability}%

You are ahead of schedule.

Continue following today's mission.
"""
        )

    elif risk == "Medium":

        st.warning(
            f"""
🟡 GUARDIAN STATUS: CAUTION

Completion Probability: {probability}%

You are behind schedule by {abs(gap)}%.

Recovery Mode is recommended.
"""
        )

    else:

        st.error(
            f"""
🔴 GUARDIAN STATUS: CRITICAL

Completion Probability: {probability}%

You are behind schedule by {abs(gap)}%.

Immediate Recovery Mode activation is recommended.
"""
        )