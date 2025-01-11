import streamlit as st

from src.dashboard.data.load_data import load_zurich_item

st.session_state["selected_marker"] = []
item_df = load_zurich_item(item_id=st.session_state["current_item"]).iloc[0]
st.subheader(item_df["name_en"], divider="rainbow")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(item_df["image_url"])

with col2:
    st.html(item_df["description_en"])

with col3:
    tel = (
        f'{item_df["address_telephone"]}<br />'
        if item_df["address_telephone"] is not None
        else ""
    )
    email = (
        f'{item_df["address_email"]}<br />'
        if item_df["address_email"] is not None
        else ""
    )
    web = (
        f"""<a href='{item_df["address_url"]}' target="_blank">Website</a><br />"""
        if item_df["address_url"] is not None
        else ""
    )

    text = f"""
    {item_df["address_streetAddress"]} <br />
    {item_df["address_postalCode"]} {item_df["city"]}<br />
    <br />
    {tel}
    {email}
    {web}
    """
    st.html(text)
