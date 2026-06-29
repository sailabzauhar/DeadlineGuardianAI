import streamlit as st

from database import (
    get_active_goal,
    get_goal_progress,
    get_active_month_by_goal,
    get_active_week_by_month,
    get_active_day_by_week
)

from services.motivation_service import (
    get_daily_motivation
)


def show_guardian_status_bar():

    goal = get_active_goal()

    if goal is None:
        return

    goal_id = goal[0]
    goal_title = goal[1]
    deadline = goal[2]

    progress = int(
        get_goal_progress(
            goal_id
        ) * 100
    )

    month = get_active_month_by_goal(
        goal_id
    )

    week = None
    day = None

    if month:

        week = get_active_week_by_month(
            month["id"]
        )

    if week:

        day = get_active_day_by_week(
            week["id"]
        )

    month_text = "-"
    week_text = "-"
    day_text = "-"

    if month:
        month_text = str(
            month["month"]
        )

    if week:
        week_text = str(
            week["week"]
        )

    if day:
        day_text = str(
            day["day"]
        )

    try:

        quote = get_daily_motivation()

    except Exception:

        quote = (
            "आज का छोटा प्रयास, कल की बड़ी सफलता बनता है।"
        )

    st.markdown(
        f"""
<div style="
background:linear-gradient(
90deg,
#0f172a,
#1e293b
);
padding:18px;
border-radius:14px;
margin-bottom:20px;
border-left:6px solid #22c55e;
">

<h3 style="
color:white;
text-align:center;
">
🎯 {goal_title}
</h3>

<p style="
color:#cbd5e1;
text-align:center;
font-size:16px;
">

📈 Progress: <b>{progress}%</b>

&nbsp;&nbsp;|&nbsp;&nbsp;

🎯 Deadline: <b>{deadline}</b>

&nbsp;&nbsp;|&nbsp;&nbsp;

📅 Month {month_text}

&nbsp;&nbsp;|&nbsp;&nbsp;

📆 Week {week_text}

&nbsp;&nbsp;|&nbsp;&nbsp;

☀️ Day {day_text}

</p>

<div style="
background:#334155;
height:10px;
border-radius:10px;
overflow:hidden;
margin-top:10px;
margin-bottom:10px;
">

<div style="
width:{progress}%;
height:10px;
background:#22c55e;
">
</div>

</div>

<p style="
color:white;
font-size:18px;
font-weight:600;
text-align:center;
margin-top:10px;
">
🔥 {quote}
</p>

</div>
""",
        unsafe_allow_html=True
    )