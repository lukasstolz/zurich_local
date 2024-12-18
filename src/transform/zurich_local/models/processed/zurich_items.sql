-- depends_on: {{ ref('stg_items_activities') }}
-- depends_on: {{ ref('stg_items_bars') }}
-- depends_on: {{ ref('stg_items_culture') }}
-- depends_on: {{ ref('stg_items_dining') }}
-- depends_on: {{ ref('stg_items_hotels') }}
-- depends_on: {{ ref('stg_items_museums') }}
-- depends_on: {{ ref('stg_items_nightlife') }}
-- depends_on: {{ ref('stg_items_shopping') }}
-- depends_on: {{ ref('stg_items_sights') }}
-- depends_on: {{ ref('stg_items_sport') }}
-- depends_on: {{ ref('stg_items_wellness') }}

with items as (
    {% set staging_tables_query %}
        select distinct table_name from information_schema.columns where table_schema = 'staging' and table_name like 'stg_items_%'
    {% endset %}

    {% set staging_tables = dbt_utils.get_query_results_as_dict(staging_tables_query) %}

    {% set select_fields = [
        "description_de",
        "description_en",
        "description_fr",
        "description_it",
        "address_addressCountry",
        "address_addressLocality",
        "address_postalCode",
        "address_streetAddress",
        "address_telephone",
        "address_email",
        "address_url",
        "detailedinformation_de",
        "detailedinformation_en",
        "detailedinformation_fr",
        "detailedinformation_it",
        "disambiguatingdescription_de",
        "disambiguatingdescription_en",
        "disambiguatingdescription_fr",
        "disambiguatingdescription_it",
        "geocoordinates_latitude",
        "geocoordinates_longitude",
        "image_url",
        "image_caption",
        "name_de",
        "name_en",
        "name_fr",
        "name_it",
        "price_de",
        "price_en",
        "price_fr",
        "price_it",
        "specialopeninghoursspecification_de",
        "specialopeninghoursspecification_en",
        "specialopeninghoursspecification_fr",
        "specialopeninghoursspecification_it",
        "textteaser_de",
        "textteaser_en",
        "textteaser_fr",
        "textteaser_it",
        "titleteaser_de",
        "titleteaser_en",
        "titleteaser_fr",
        "titleteaser_it",
        "_customtype",
        "_type",
        "datemodified",
        "identifier",
        "license",
        "osm_id",
        "zurichcard",
        "category_de",
        "category_en"
    ] %}
    {% for stg_table in staging_tables.table_name %}

        {%- set available_cols = dbt_utils.get_filtered_columns_in_relation(from=ref(stg_table)) -%}

        select
        {% for select_field in select_fields %}
            {% if select_field in available_cols -%}
                {{- select_field }},
            {% else %}
                NULL as {{- select_field }},
            {% endif %}
        {% endfor %}

        from staging.{{- stg_table }}

        {% if not loop.last %}
            union all
        {% endif %}

    {% endfor %}
)

select * from items
