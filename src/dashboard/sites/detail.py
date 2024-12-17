import streamlit as st

st.subheader("Foo")

# Sidebar
with st.sidebar:
    zone_options = st.multiselect("Kategorien", ["Shopping", "Museen"])
