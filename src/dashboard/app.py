import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
from style import get_style_str

st.set_page_config(layout="wide")

nav = get_nav_from_toml("src/dashboard/pages.toml")

st.markdown(f"<style>{get_style_str()}</style>", unsafe_allow_html=True)
st.logo("src/dashboard/static/logo/logo.png", size="large")

with st.sidebar:
    st.text(
        "Welcome to zurich local. Learn about things to do, where to stay, eat & drink and what to see in and around Zurich!"
    )

pg = st.navigation(nav)

add_page_title(pg)

pg.run()
