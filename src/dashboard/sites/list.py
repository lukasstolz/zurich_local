import streamlit as st

st.subheader("Bar")

# Sidebar
with st.sidebar:
    zone_options = st.multiselect("Kategorien", ["Shopping", "Museen"])
