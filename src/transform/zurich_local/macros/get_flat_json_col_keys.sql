{% macro get_flat_json_col_keys(table_name, schema_name='') %}

{% if schema_name == '' %}
    {% set schema_name = target.schema %}
{% endif %}

{% set col_names_query %}
    select
        column_name
    from
        information_schema.columns
    where table_schema = '{{- schema_name -}}'
        and table_name = '{{- table_name -}}'
        and data_type = 'JSON'
{% endset %}

{% set col_names = dbt_utils.get_query_results_as_dict(col_names_query) %}

{% set cols_keys = [] %}

{% for col_name in col_names.column_name %}

    {% set json_keys_query %}
        with keys as (select json_keys({{- col_name -}}) as json_keys from {{ schema_name -}}.{{- table_name }} limit 1)
        select unnest(json_keys) as key_name from keys
    {% endset %}

    {% set key_names = dbt_utils.get_query_results_as_dict(json_keys_query) %}

    {% for key_name in key_names.key_name %}
        {% do cols_keys.append([col_name | replace(" ", "_"), key_name | replace(" ", "_")]) %}
    {% endfor %}

{% endfor %}

{{ return(cols_keys) }}

{% endmacro %}
