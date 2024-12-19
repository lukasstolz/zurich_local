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


def create_marker(lat: int, lon: int, popup: str, tooltip: str) -> None:
    icon_opts = icon_dict[st.session_state["category"]]

    icon = folium.Icon(prefix="fa", **icon_opts)
    marker = folium.Marker(
        [lat, lon], popup=popup, tooltip=tooltip, icon=icon, lazy=True
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


def change_category(id: str) -> None:
    st.session_state["markers"].clear()
    st.session_state["category"] = st.session_state[id]
    add_markers()


if "category" not in st.session_state:
    st.session_state["category"] = "Gastronomie"

with st.sidebar:
    st.session_state["category"] = option_menu(
        None,
        [
            "Hotels",
            "Sport",
            "Nachtleben",
            "Bars",
            "Shopping",
            "Museen",
            "Sehenswürdigkeiten",
            "Wellness",
            "Gastronomie",
            "Kultur",
            "Aktivitäten",
        ],
        default_index=0,
        key="category_menu",
        on_change=change_category,
    )
# categories_df = load_categories()

# for category in categories_df["category_de"]:
#     if st.button(category, use_container_width=True):
#         st.session_state["markers"].clear()
#         st.session_state["category"] = category
#         add_markers()


if "markers" not in st.session_state:
    st.session_state["markers"] = []
    add_markers()

if "map_config" not in st.session_state:
    st.session_state.map_config = {
        "center": [47.3769, 8.5417],
        "zoom": 10,
    }

st.header(st.session_state["category"], divider="rainbow")


draw_map()
