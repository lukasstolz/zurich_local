import streamlit as st
from streamlit_option_menu import option_menu

from src.dashboard.data.load_data import load_zurich_items

items_df = load_zurich_items()
icon_dict = {
    "Lodging": {"icon": "hotel", "color": "blue"},
    "Sports": {"icon": "volleyball", "color": "green"},
    "Nightlife": {"icon": "martini-glass", "color": "darkblue"},
    "Bars": {"icon": "wine-glass", "color": "cadetblue"},
    "Shopping": {"icon": "bag-shopping", "color": "lightgreen"},
    "Museums": {"icon": "building-columns", "color": "purple"},
    "Sights": {"icon": "mountain", "color": "darkgreen"},
    "Wellness": {"icon": "spa", "color": "lightblue"},
    "Dining": {"icon": "utensils", "color": "red"},
    "Culture": {"icon": "masks-theater", "color": "lightred"},
    "Activities": {"icon": "ticket", "color": "darkred"},
}

categories = [*icon_dict]
st.session_state["selected_marker"] = []


def change_category(id: str) -> None:
    st.session_state["category"] = st.session_state[id]


if "category" not in st.session_state:
    st.session_state["category"] = categories[0]


with st.sidebar:
    st.session_state["category"] = option_menu(
        None,
        categories,
        default_index=categories.index(st.session_state["category"]),
        key="category_menu",
        on_change=change_category,
    )


st.header(st.session_state["category"], divider="rainbow")


selected_items = items_df[items_df["category_en"] == st.session_state["category"]]

for index, item in selected_items.iterrows():
    st.subheader(item["name_en"])

    st.text(item["textteaser_en"])

    details_button = st.button("Detail", key=index)
    if details_button:
        st.session_state["current_item"] = item["id"]
        st.switch_page("sites/detail.py")

    st.divider()
