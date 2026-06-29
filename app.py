import streamlit as st

st.set_page_config(
    page_title="Deadline Guardian AI",
    page_icon="🛡️",
    layout="wide"
)

from database import (
    initialize_database,
    get_active_goal_id
)

from guardian_status_bar import (
    show_guardian_status_bar
)

initialize_database()

goal_id = get_active_goal_id()

if goal_id is None:

    st.switch_page(
        "pages/1_🏠_Create_Goal.py"
    )

with open(
    "assets/style.css",
    encoding="utf-8"
) as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


from components.hero_quote import (
    show_hero_quote
)

from services.motivation_service import (
    get_daily_motivation
)


st.title(
    "🛡️ Deadline Guardian AI"
)

quote = get_daily_motivation()

show_hero_quote(
    quote
)

st.markdown(
    """
## Your AI that refuses to let you miss deadlines

### Features

- 🎯 AI Goal Planning
- 📅 Daily Mission Tracking
- ⚡ AI Recovery Mode
- 📊 Productivity Dashboard

Use the sidebar to navigate through the application.
"""
)

st.success(
    "Deadline Guardian AI is ready."
)