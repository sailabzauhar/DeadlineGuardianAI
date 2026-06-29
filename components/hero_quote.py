import streamlit as st


def show_hero_quote(
    quote
):

    st.markdown(
        f"""
<div style="
background:linear-gradient(
135deg,
#111827,
#312e81
);
padding:12px 20px;
border-radius:18px;
margin-bottom:12px;
min-height:90px;
display:flex;
flex-direction:column;
justify-content:center;
">

<div style="
font-size:22px;
color:#a78bfa;
line-height:1;
margin-bottom:4px;
">
❝
</div>

<div style="
color:white;
font-size:20px;
font-weight:600;
line-height:1.3;
margin-bottom:6px;
">
{quote}
</div>

<div style="
color:#c4b5fd;
font-size:13px;
">
Stay focused. Future You is waiting.
</div>

</div>
""",
        unsafe_allow_html=True
    )