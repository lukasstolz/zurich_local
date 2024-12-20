import streamlit as st

from src.dashboard.data.load_data import load_zurich_item

item_df = load_zurich_item(item_id=st.session_state["current_item"]).iloc[0]
st.subheader(item_df["name_de"], divider="rainbow")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(item_df["image_url"])

with col2:
    st.html(item_df["description_de"])

with col3:
    text = f"""
    {item_df["address_streetAddress"]}<br />
    {item_df["address_postalCode"]} {item_df["city"]}<br />
    <br />
    {item_df["address_telephone"]}<br />
    {item_df["address_email"]}<br />
    <a href='{item_df["address_url"]} target="_blank"'>Website</a><br />
    """
    st.html(text)
