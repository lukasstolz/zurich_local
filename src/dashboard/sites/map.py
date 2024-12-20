import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu

from src.dashboard.data.load_data import load_zurich_items

items_df = load_zurich_items()
icon_dict = {
    "Hotels": {"icon": "hotel", "color": "blue"},
    "Sport": {"icon": "volleyball", "color": "green"},
    "Nachtleben": {"icon": "martini-glass", "color": "darkblue"},
    "Bars": {"icon": "wine-glass", "color": "cadetblue"},
    "Shopping": {"icon": "bag-shopping", "color": "lightgreen"},
    "Museen": {"icon": "building-columns", "color": "purple"},
    "Sehenswürdigkeiten": {"icon": "mountain", "color": "darkgreen"},
    "Wellness": {"icon": "spa", "color": "lightblue"},
    "Gastronomie": {"icon": "utensils", "color": "red"},
    "Kultur": {"icon": "masks-theater", "color": "lightred"},
    "Aktivitäten": {"icon": "ticket", "color": "darkred"},
}

categories = [*icon_dict]

items_df["icon_opts"] = items_df["category_de"].map(icon_dict)


def create_marker(lat: int, lon: int, tooltip: str, icon_opts: dict) -> None:
    icon = folium.Icon(prefix="fa", **icon_opts)
    marker = folium.Marker(
        [lat, lon],
        tooltip=tooltip,
        icon=icon,
        lazy=True,
    )
    st.session_state["markers"].append(marker)


@st.cache_data
def base_map() -> None:
    m = folium.Map(
        location=st.session_state.map_config["center"],
        zoom_start=st.session_state.map_config["zoom"],
        tiles="Stadia.AlidadeSmooth",
    )
    fg = folium.FeatureGroup(name="Markers")

    return m, fg


def draw_map() -> None:
    m, fg = base_map()

    for marker in st.session_state["markers"]:
        fg.add_child(marker)

    selected = st_folium(
        m,
        feature_group_to_add=fg,
        center=st.session_state.map_config["center"],
        zoom=st.session_state.map_config["zoom"],
        returned_objects=["last_object_clicked"],
        use_container_width=True,
    )

    st.session_state["selected_marker"] = selected


def add_markers() -> None:
    selected_items = items_df[items_df["category_de"] == st.session_state["category"]]

    selected_items[~pd.isna(selected_items["geocoordinates_latitude"])].apply(
        lambda x: create_marker(
            x["geocoordinates_latitude"],
            x["geocoordinates_longitude"],
            tooltip=x["name_de"],
            icon_opts=x["icon_opts"],
        ),
        axis=1,
    )


def change_category(id: str) -> None:
    close_sidebar()
    st.session_state["markers"].clear()
    st.session_state["category"] = st.session_state[id]
    add_markers()


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


if "markers" not in st.session_state:
    st.session_state["markers"] = []
    add_markers()

if "map_config" not in st.session_state:
    st.session_state.map_config = {
        "center": [47.3769, 8.5417],
        "zoom": 10,
    }


def close_sidebar():
    st.session_state["selected_marker"] = []


def main() -> None:
    st.header(st.session_state["category"], divider="rainbow")

    if "selected_marker" not in st.session_state:
        close_sidebar()

    if len(st.session_state["selected_marker"]) > 0:
        col1, col2 = st.columns([3, 1])

        with col1:
            draw_map()

        with col2:
            selected_marker = st.session_state["selected_marker"]["last_object_clicked"]
            item = items_df[
                (items_df["category_de"] == st.session_state["category"])
                & (items_df["geocoordinates_latitude"] == str(selected_marker["lat"]))
                & (items_df["geocoordinates_longitude"] == str(selected_marker["lng"]))
            ].iloc[0]

            st.subheader(item["name_de"])

            st.text(item["disambiguatingdescription_de"])
            details_button = st.button("Details", key=item["id"])
            if details_button:
                st.session_state["current_item"] = item["id"]
                st.switch_page("sites/detail.py")

            st.button("Close", on_click=close_sidebar)

    else:
        draw_map()


main()
