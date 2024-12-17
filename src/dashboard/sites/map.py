import streamlit as st

st.subheader("Baz")

# Sidebar
with st.sidebar:
    zone_options = st.multiselect("Kategorien", ["Shopping", "Museen"])
