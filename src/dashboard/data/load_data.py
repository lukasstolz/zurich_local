import os

import duckdb
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
md_access_token = os.environ.get("MD_ACCESS_TOKEN")

con: duckdb.DuckDBPyConnection = duckdb.connect(
    f"md:?motherduck_token={md_access_token}"
)
con.sql("use zuerich_db")


@st.cache_data
def load_cities() -> pd.DataFrame:
    cities = con.sql("select * from marts.dim_cities").df()
    return cities


@st.cache_data
def load_types() -> pd.DataFrame:
    types = con.sql("select * from marts.dim_types").df()
    return types


@st.cache_data
def load_custom_types() -> pd.DataFrame:
    custom_types = con.sql("select * from marts.dim_custom_types").df()
    return custom_types


@st.cache_data
def load_zurich_items() -> pd.DataFrame:
    items = con.sql("""
                    select
                        *
                    from marts.fact_zurich_items items

                    left join marts.dim_types types
                    on types.id = items.type_id

                    left join marts.dim_custom_types custom_types
                    on custom_types.id = items.custom_type_id

                    left join marts.dim_cities cities
                    on cities.id = items.city_id

                    """).df()

    return items


print(load_zurich_items())
