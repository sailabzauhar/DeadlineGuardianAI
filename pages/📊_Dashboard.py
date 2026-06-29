import streamlit as st
import plotly.express as px
import pandas as pd

from guardian_status_bar import (
    show_guardian_status_bar
)

from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)

from services.guardian_radar import (
    get_guardian_radar
)

from guardian_alert import (
    show_guardian_alert
)

from database import (
    get_active_goal_id,
    get_active_month_by_goal,
    get_active_week_by_month,
    get_active_day_by_week,
    get_goal_progress,
    get_productivity_score,
    get_total_task_count,
    get_completed_task_count,

    get_completed_goals_count,
    get_archived_goals_count,
    get_goal_success_rate
)

from services.risk_service import (
    get_expected_progress,
    get_actual_progress,
    get_risk_level,
    get_completion_probability,
    get_schedule_gap
)

st.header("📊 Dashboard")

quote = get_daily_motivation()

show_hero_quote(
    quote
)

show_guardian_alert()

goal_id = get_active_goal_id()

if goal_id is None:

    st.info(
        "Create your first goal."
    )

    st.stop()

# ---------------------------------
# Goal Progress
# ---------------------------------

goal_progress = int(
    get_goal_progress(
        goal_id
    ) * 100
)

# ---------------------------------
# Active Month
# ---------------------------------

active_month = get_active_month_by_goal(
    goal_id
)

month_name = "Completed"

if active_month:

    month_name = (
        f"Month {active_month['month']}"
    )

# ---------------------------------
# Active Week
# ---------------------------------

week_name = "Completed"

active_week = None

if active_month:

    active_week = get_active_week_by_month(
        active_month["id"]
    )

    if active_week:

        week_name = (
            f"Week {active_week['week']}"
        )

# ---------------------------------
# Active Day
# ---------------------------------

day_name = "Completed"

if active_week:

    active_day = get_active_day_by_week(
        active_week["id"]
    )

    if active_day:

        day_name = (
            f"Day {active_day['day']}"
        )

# ---------------------------------
# Risk Engine
# ---------------------------------

expected_progress = (
    get_expected_progress()
)

actual_progress = (
    get_actual_progress()
)

risk_level = (
    get_risk_level()
)

completion_probability = (
    get_completion_probability()
)

schedule_gap = (
    get_schedule_gap()
)

radar = get_guardian_radar()

# ---------------------------------
# Task Stats
# ---------------------------------

total_tasks = get_total_task_count(
    goal_id
)

completed_tasks = get_completed_task_count(
    goal_id
)

pending_tasks = (
    total_tasks -
    completed_tasks
)

score = get_productivity_score(
    goal_id
)

completed_goals = (
    get_completed_goals_count()
)

archived_goals = (
    get_archived_goals_count()
)

success_rate = (
    get_goal_success_rate()
)

# ---------------------------------
# Guardian Health
# ---------------------------------

st.subheader(
    "🧠 Guardian Health"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Completion Probability",
    f"{completion_probability}%"
)

col2.metric(
    "Risk Level",
    risk_level
)

col3.metric(
    "Goal Progress",
    f"{goal_progress}%"
)

st.divider()

# ---------------------------------
# Guardian Verdict
# ---------------------------------


st.subheader(
    "🛡 Guardian Radar"
)

if radar["risk"] == "Low":

    st.success(
        f"""
Risk: {radar['risk']}

Reason:
{radar['reason']}

Recommendation:
{radar['recommendation']}
"""
    )

elif radar["risk"] == "Medium":

    st.warning(
        f"""
Risk: {radar['risk']}

Reason:
{radar['reason']}

Recommendation:
{radar['recommendation']}
"""
    )

else:

    st.error(
        f"""
Risk: {radar['risk']}

Reason:
{radar['reason']}

Recommendation:
{radar['recommendation']}
"""
    )

# ---------------------------------
# Guardian Verdict
# ---------------------------------

if risk_level == "Low":

    st.success(
        "🟢 Guardian Verdict: You are on track to finish before the deadline."
    )

elif risk_level == "Medium":

    st.warning(
        "🟡 Guardian Verdict: You are slightly behind schedule. Recovery may be needed."
    )

else:

    st.error(
        "🔴 Guardian Verdict: High risk of missing the deadline. Activate Recovery Mode."
    )

# ---------------------------------
# Quick Status
# ---------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Mission Status",
    "On Track" if schedule_gap >= 0 else "Behind"
)

col2.metric(
    "Tasks Remaining",
    pending_tasks
)

col3.metric(
    "Recovery Needed",
    "No" if schedule_gap >= 0 else "Yes"
)

# ---------------------------------
# Progress Analysis
# ---------------------------------

st.divider()

st.subheader(
    "📈 Progress Analysis"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Expected Progress",
    f"{expected_progress}%"
)

col2.metric(
    "Actual Progress",
    f"{actual_progress}%"
)

col3.metric(
    "Schedule Gap",
    f"{schedule_gap}%"
)

# ---------------------------------
# Recovery Opportunity
# ---------------------------------

if schedule_gap < 0:

    st.subheader(
        "🚑 Recovery Opportunity"
    )

    st.warning(
        f"""
You are currently behind by {abs(schedule_gap)}%.

Deadline Guardian recommends activating Recovery Mode to improve your completion probability.
"""
    )

# ---------------------------------
# Current Position
# ---------------------------------

st.divider()

st.subheader(
    "🗺️ Current Position"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Active Month",
    month_name
)

col2.metric(
    "Active Week",
    week_name
)

col3.metric(
    "Active Day",
    day_name
)

# ---------------------------------
# Execution Stats
# ---------------------------------

st.divider()

st.subheader(
    "⚡ Execution Stats"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Productivity Score",
    f"{score}%"
)

col2.metric(
    "Completed Tasks",
    completed_tasks
)

col3.metric(
    "Pending Tasks",
    pending_tasks
)

# ---------------------------------
# 🏆 Lifetime Statistics
# ---------------------------------


st.divider()

st.subheader(
    "🏆 Lifetime Statistics"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Goals Completed",
    completed_goals
)

col2.metric(
    "Goals Archived",
    archived_goals
)

col3.metric(
    "Success Rate",
    f"{success_rate}%"
)

# ---------------------------------
# Goal Completion
# ---------------------------------

st.divider()

st.subheader(
    "🎯 Goal Completion"
)

st.progress(
    goal_progress / 100
)

st.caption(
    f"{goal_progress}% Completed"
)

# ---------------------------------
# Progress Chart
# ---------------------------------

st.divider()

st.subheader(
    "📈 Expected vs Actual Progress"
)

progress_df = pd.DataFrame(
    {
        "Type": [
            "Expected",
            "Actual"
        ],
        "Progress": [
            expected_progress,
            actual_progress
        ]
    }
)

fig_progress = px.bar(
    progress_df,
    x="Type",
    y="Progress",
    text="Progress",
    title="Progress Comparison"
)

st.plotly_chart(
    fig_progress,
    use_container_width=True
)

# ---------------------------------
# Task Completion Chart
# ---------------------------------

if total_tasks > 0:

    fig = px.pie(
        names=[
            "Completed",
            "Pending"
        ],
        values=[
            completed_tasks,
            pending_tasks
        ],
        hole=0.45,
        title="Task Completion Overview"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )