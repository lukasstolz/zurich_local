import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from src.dashboard.data.load_data import load_categories, load_zurich_items

items_df = load_zurich_items()


def create_marker(lat: int, lon: int, popup: str, tooltip: str) -> None:
    marker = folium.Marker([lat, lon], popup=popup, tooltip=tooltip)
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

    st_folium(
        m,
        feature_group_to_add=fg,
        center=st.session_state.map_config["center"],
        zoom=st.session_state.map_config["zoom"],
        returned_objects=[],
        use_container_width=True,
    )


def add_markers() -> None:
    selected_items = items_df[items_df["category_de"] == st.session_state["category"]]

    selected_items[~pd.isna(selected_items["geocoordinates_latitude"])].apply(
        lambda x: create_marker(
            x["geocoordinates_latitude"],
            x["geocoordinates_longitude"],
            tooltip=x["name_de"],
            popup=x["description_de"],
        ),
        axis=1,
    )


with st.sidebar:
    categories_df = load_categories()

    for category in categories_df["category_de"]:
        if st.button(category):
            st.session_state["markers"].clear()
            st.session_state["category"] = category
            add_markers()

if "category" not in st.session_state:
    st.session_state["category"] = "Gastronomie"

if "markers" not in st.session_state:
    st.session_state["markers"] = []
    add_markers()

if "map_config" not in st.session_state:
    st.session_state.map_config = {
        "center": [47.3769, 8.5417],
        "zoom": 12,
    }

st.header(st.session_state["category"], divider="rainbow")
draw_map()
