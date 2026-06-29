import streamlit as st

from guardian_status_bar import (
    show_guardian_status_bar
)

from services.automation_service import (
    bootstrap_day,
    bootstrap_week,
    bootstrap_month
)

from database import (
    get_active_goal_id,
    get_active_month_by_goal,
    get_active_week_by_month,
    get_active_day_by_week,

    get_daily_tasks,
    save_daily_task,
    complete_daily_task,

    get_daily_task_progress,

    all_tasks_completed,
    complete_day,
    activate_next_day,

    get_week_progress,
    all_days_completed,
    complete_week,
    activate_next_week,

    get_month_progress,
    all_weeks_completed,
    complete_month,
    activate_next_month
)

from services.task_service import (
    generate_tasks
)


from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)


st.header("☀️ Daily Missions")

quote = get_daily_motivation()

show_hero_quote(
    quote
)


goal_id = get_active_goal_id()

if goal_id is None:

    st.info(
        "Create a goal first."
    )

    st.stop()

month = get_active_month_by_goal(
    goal_id
)

if month is None:

    st.info(
        "No active month."
    )

    st.stop()

week = get_active_week_by_month(
    month["id"]
)

if week is None:

    st.info(
        "Generate Weekly Missions first."
    )

    st.stop()

day = get_active_day_by_week(
    week["id"]
)

if day is None:

    st.info(
        "Generate Daily Missions first."
    )

    st.stop()

# ---------------------------------
# Month Progress
# ---------------------------------

month_progress = get_month_progress(
    month["id"]
)

st.subheader(
    f"📅 Month {month['month']} Progress"
)

st.progress(
    month_progress
)

st.caption(
    f"{int(month_progress * 100)}% Completed"
)

# ---------------------------------
# Week Progress
# ---------------------------------

st.divider()

week_progress = get_week_progress(
    week["id"]
)

st.subheader(
    f"📆 Week {week['week']} Progress"
)

st.progress(
    week_progress
)

st.caption(
    f"{int(week_progress * 100)}% Completed"
)

# ---------------------------------
# Daily Mission
# ---------------------------------

st.divider()

st.success(
    "🎯 Current Daily Mission"
)

st.subheader(
    f"Day {day['day']}"
)

st.write(
    day["title"]
)

st.write(
    day["description"]
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "**Deliverable**"
    )

    st.write(
        day["deliverable"]
    )

with col2:

    st.markdown(
        "**Success Criteria**"
    )

    st.write(
        day["success_criteria"]
    )

st.caption(
    f"Estimated Hours: {day['estimated_hours']}"
)

# ---------------------------------
# Generate Tasks
# ---------------------------------

st.divider()

tasks = get_daily_tasks(
    day["id"]
)

if len(tasks) == 0:

    if st.button(
        "🚀 Generate Tasks",
        use_container_width=True
    ):

        with st.spinner(
            "Generating executable tasks..."
        ):

            plan = generate_tasks(
                day
            )

            for task in plan["tasks"]:

                save_daily_task(
                    day["id"],
                    task
                )

        st.success(
            "Tasks generated successfully."
        )

        st.rerun()

# ---------------------------------
# Task List
# ---------------------------------

else:

    st.subheader(
        "✅ Today's Tasks"
    )

    progress = get_daily_task_progress(
        day["id"]
    )

    st.progress(
        progress
    )

    st.caption(
        f"Progress: {int(progress * 100)}%"
    )

    for task in tasks:

        col1, col2 = st.columns(
            [10, 1]
        )

        with col1:

            st.markdown(
                f"""
### Task {task['task']}

**{task['title']}**

{task['description']}

**Deliverable**

{task['deliverable']}

**Success Criteria**

{task['success_criteria']}

⏳ {task['estimated_hours']} hour(s)

Status: **{task['status']}**
"""
            )

        with col2:

            if task["status"] == "Pending":

                if st.button(
                    "✅",
                    key=f"task_{task['id']}"
                ):

                    complete_daily_task(
                        task["id"]
                    )

                    # ---------------------
                    # Day Completion
                    # ---------------------

                    if all_tasks_completed(
                        day["id"]
                    ):

                        st.balloons()

                        st.success(
                            f"🎉 Day {day['day']} Completed"
                        )

                        complete_day(
                            day["id"]
                        )

                        activate_next_day(
                            week["id"],
                            day["day"]
                        )

                        next_day = get_active_day_by_week(
                            week["id"]
                        )

                        if next_day:

                            bootstrap_day(
                                next_day
                            )

                            st.success(
                                f"🚀 Day {next_day['day']} Activated"
                            )

                            st.rerun()

                        # ---------------------
                        # Week Completion
                        # ---------------------

                        if all_days_completed(
                            week["id"]
                        ):

                            st.success(
                                f"🏆 Week {week['week']} Completed"
                            )

                            complete_week(
                                week["id"]
                            )

                            activate_next_week(
                                month["id"],
                                week["week"]
                            )

                            next_week = get_active_week_by_month(
                                month["id"]
                            )

                            if next_week:

                                bootstrap_week(
                                    next_week
                                )

                                st.success(
                                    f"🚀 Week {next_week['week']} Activated"
                                )

                                st.rerun()

                            # ---------------------
                            # Month Completion
                            # ---------------------

                            if all_weeks_completed(
                                month["id"]
                            ):

                                st.success(
                                    f"🏅 Month {month['month']} Completed"
                                )

                                complete_month(
                                    month["id"]
                                )

                                activate_next_month(
                                    goal_id,
                                    month["month"]
                                )

                                next_month = get_active_month_by_goal(
                                    goal_id
                                )

                                if next_month:

                                    bootstrap_month(
                                        next_month
                                    )

                                    st.success(
                                        f"🚀 Month {next_month['month']} Activated"
                                    )

                                    st.rerun()

                    st.rerun()

            else:

                st.success(
                    "Done"
                )

        st.divider()