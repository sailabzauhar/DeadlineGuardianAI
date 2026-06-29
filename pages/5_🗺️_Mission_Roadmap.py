import streamlit as st

from guardian_status_bar import (
    show_guardian_status_bar
)

from database import (
    get_active_goal,
    get_months,
    get_weeks,
    get_days
)


from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)


st.header("🗺️ Mission Roadmap")

quote = get_daily_motivation()

show_hero_quote(
    quote
)


goal = get_active_goal()

if goal is None:

    st.info(
        "No active goal."
    )

    st.stop()

goal_id = goal[0]
goal_title = goal[1]

st.subheader(
    f"🎯 {goal_title}"
)

months = get_months(
    goal_id
)

if len(months) == 0:

    st.info(
        "No roadmap found."
    )

    st.stop()

for month in months:

    month_status = month["status"]

    if month_status == "Completed":

        month_icon = "✅"

    elif month_status == "Active":

        month_icon = "🚀"

    else:

        month_icon = "🔒"

    st.markdown(
        f"""
## {month_icon} Month {month['month']}

**{month['title']}**

{month['description']}
"""
    )

    weeks = get_weeks(
        month["id"]
    )

    for week in weeks:

        week_status = week["status"]

        if week_status == "Completed":

            week_icon = "✅"

        elif week_status == "Active":

            week_icon = "🚀"

        else:

            week_icon = "🔒"

        with st.expander(
            f"{week_icon} Week {week['week']} - {week['title']}"
        ):

            st.write(
                week["description"]
            )

            st.caption(
                f"Deliverable: {week['deliverable']}"
            )

            st.caption(
                f"Success Criteria: {week['success_criteria']}"
            )

            days = get_days(
                week["id"]
            )

            for day in days:

                day_status = day["status"]

                if day_status == "Completed":

                    day_icon = "✅"

                elif day_status == "Active":

                    day_icon = "🚀"

                else:

                    day_icon = "🔒"

                st.markdown(
                    f"""
{day_icon} Day {day['day']} — {day['title']}
"""
                )

    st.divider()