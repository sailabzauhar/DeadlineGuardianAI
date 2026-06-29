import streamlit as st
from datetime import date

from guardian_status_bar import (
    show_guardian_status_bar
)

from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)

from database import (
    get_goals
)

from services.monthly_service import (
    generate_plan
)

from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)


st.header("🏠 Create Goal")

quote = get_daily_motivation()

show_hero_quote(
    quote
)

st.markdown(
    """
Create a goal and let Deadline Guardian automatically build your execution roadmap.
"""
)

goal = st.text_input(
    "Goal",
    placeholder="Complete MD Physiology Thesis"
)

deadline = st.date_input(
    "Deadline",
    min_value=date.today()
)

mode = st.selectbox(
    "Mode",
    [
        "Medical Student",
        "Student",
        "Professional"
    ]
)

if st.button(
    "🚀 Generate AI Plan",
    use_container_width=True
):

    if goal.strip() == "":

        st.error(
            "Please enter a goal."
        )

    else:

        try:

            with st.spinner(
                "🧠 Deadline Guardian is creating your roadmap..."
            ):

                generate_plan(
                    goal,
                    str(deadline),
                    mode
                )

            st.success(
                "AI Plan Created Successfully!"
            )

            st.balloons()

            st.switch_page(
                "pages/4_Daily_Missions.py"
            )

        except Exception as e:

            st.error(
                str(e)
            )

# ---------------------------------
# Goal History
# ---------------------------------

st.divider()

st.subheader(
    "📋 Goal History"
)

goals = get_goals()

if goals:

    for goal_item in goals:

        st.markdown(
            f"""
### 🎯 {goal_item[1]}

📅 Deadline: {goal_item[2]}
"""
        )

        st.divider()

else:

    st.info(
        "No goals created yet."
    )