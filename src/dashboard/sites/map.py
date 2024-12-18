import re

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from src.dashboard.data.load_data import load_types, load_zurich_items

st.subheader("Baz")

items_df = load_zurich_items()


if "selected_type" not in st.session_state:
    st.session_state["type"] = "Restaurant"


# Sidebar
with st.sidebar:
    types_df = load_types()
    types = [
        re.sub(r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", type)
        for type in types_df["type"]
    ]

    for type in types:
        if st.button(type):
            st.session_state["type"] = type


m = folium.Map(location=[47.3769, 8.5417], zoom_start=12, tiles="Stadia.AlidadeSmooth")


def add_item_marker(lat: int, lon: int, popup: str, tooltip: str) -> None:
    folium.Marker([lat, lon], popup=popup, tooltip=tooltip).add_to(m)


selected_items = items_df[items_df["type"] == st.session_state["type"]]

selected_items[~pd.isna(selected_items["geocoordinates_latitude"])].apply(
    lambda x: add_item_marker(
        x["geocoordinates_latitude"],
        x["geocoordinates_longitude"],
        tooltip=x["name_de"],
        popup=x["description_de"],
    ),
    axis=1,
)

st_folium(m, width=1200, height=800, returned_objects=[])


st.dataframe(selected_items)
