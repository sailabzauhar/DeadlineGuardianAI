import streamlit as st

from guardian_status_bar import (
    show_guardian_status_bar
)

from database import (
    get_goals,
    get_goal_months,
    get_weeks,
    save_week,
    get_month_progress,
    get_goal_progress,
)

from services.weekly_service import (
    generate_weekly_missions
)

from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)


st.header("🎯 Monthly Mission")

quote = get_daily_motivation()

show_hero_quote(
    quote
)
goals = get_goals()

if not goals:

    st.info("Create a goal first.")

else:

    latest_goal = goals[0]

    goal_id = latest_goal[0]
    goal_title = latest_goal[1]
    deadline = latest_goal[2]

    st.subheader(goal_title)
    st.caption(f"Deadline: {deadline}")

    goal_progress = get_goal_progress(
        goal_id
    )

    st.subheader(
        "🎯 Goal Progress"
    )

    st.progress(
        goal_progress
    )

    st.caption(
        f"{int(goal_progress*100)}% Completed"
    )

    st.divider()


    months = get_goal_months(goal_id)

    if not months:

        st.info("No Monthly Mission Plan available.")

    else:

        for month in months:

            # -----------------------------
            # Status
            # -----------------------------
            if month["status"] == "Active":
                icon = "🟢"
            elif month["status"] == "Completed":
                icon = "✅"
            else:
                icon = "🔒"

            st.markdown(
                f"## {icon} Month {month['month']}"
            )

            st.markdown(
                f"### {month['title']}"
            )

            st.write(
                month["description"]
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Deliverable**")
                st.write(month["deliverable"])

            with col2:
                st.markdown("**Success Criteria**")
                st.write(month["success_criteria"])

            st.caption(
                f"Estimated Duration : {month['estimated_weeks']} week(s)"
            )

            # -----------------------------
            # Progress (Placeholder)
            # -----------------------------
            progress = int(
                get_month_progress(
                    month["id"]
                ) * 100
            )
            st.progress(progress / 100)

            st.caption(f"Progress : {progress}%")

            # -----------------------------
            # Button
            # -----------------------------
            if month["status"] == "Active":

                existing_weeks = get_weeks(
                    month["id"]
                )

                if len(existing_weeks) == 0:
                
                    if st.button(
                        "📆 Generate Weekly Missions",
                        key=f"month_{month['id']}",
                        use_container_width=True
                    ):

                        with st.spinner(
                            "Generating Weekly Missions..."
                        ):

                            plan = generate_weekly_missions(
                                month
                            )

                            for week in plan["weeks"]:

                                save_week(
                                    month["id"],
                                    week
                                )

                        st.success(
                            "Weekly Missions Generated Successfully!"
                        )

                        st.rerun()

                else:

                    st.success(         
                        f"✅ {len(existing_weeks)} Weekly Missions Created"
                    )           

            else:

                st.button(
                    "🔒 Locked",
                    disabled=True,
                    key=f"locked_{month['id']}",
                    use_container_width=True
                )

            st.divider()