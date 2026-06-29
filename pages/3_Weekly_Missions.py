import streamlit as st

from guardian_status_bar import (
    show_guardian_status_bar
)
from database import (
    get_active_goal,
    get_active_month,

    get_weeks,
    get_week_progress,

    get_days,
    save_day
)

from services.daily_service import (
    generate_daily_missions
)

from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)


st.header("📆 Weekly Missions")

quote = get_daily_motivation()

show_hero_quote(
    quote
)
goal = get_active_goal()

if goal is None:

    st.info(
        "Create a goal first."
    )

    st.stop()

goal_id = goal[0]

active_month = get_active_month(
    goal_id
)

if active_month is None:

    st.info(
        "No active monthly mission."
    )

    st.stop()

st.subheader(
    f"Month {active_month['month']}"
)

st.write(
    active_month["title"]
)

st.caption(
    active_month["description"]
)

weeks = get_weeks(
    active_month["id"]
)

if len(weeks) == 0:

    st.info(
        "Generate Weekly Missions from Goal Roadmap."
    )

    st.stop()

for week in weeks:

    if week["status"] == "Completed":
        icon = "✅"

    elif week["status"] == "Active":
        icon = "🟢"

    else:
        icon = "🔒"

    st.markdown(
        f"## {icon} Week {week['week']}"
    )

    st.markdown(
        f"### {week['title']}"
    )

    st.write(
        week["description"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "**Deliverable**"
        )

        st.write(
            week["deliverable"]
        )

    with col2:

        st.markdown(
            "**Success Criteria**"
        )

        st.write(
            week["success_criteria"]
        )

    st.caption(
        f"Estimated Days : {week['estimated_days']}"
    )

    progress = int(
        get_week_progress(
            week["id"]
        ) * 100
    )

    st.progress(
        progress / 100
    )

    st.caption(
        f"Progress : {progress}%"
    )

    if week["status"] == "Active":

        existing_days = get_days(
            week["id"]
        )

        if len(existing_days) == 0:

            if st.button(
                "☀️ Generate Daily Missions",
                key=f"week_{week['id']}",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating Daily Missions..."
                ):

                    plan = generate_daily_missions(
                        week
                    )

                    for day in plan["days"]:

                        save_day(
                            week["id"],
                            day
                        )

                st.success(
                    "Daily Missions Generated Successfully!"
                )

                st.rerun()

        else:

            st.success(
                f"✅ {len(existing_days)} Daily Missions Created"
            )

    else:

        st.button(
            "🔒 Locked",
            disabled=True,
            key=f"locked_{week['id']}",
            use_container_width=True
        )

    st.divider()