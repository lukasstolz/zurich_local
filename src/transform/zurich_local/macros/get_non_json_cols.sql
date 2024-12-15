{% macro get_non_json_cols(table_name, schema_name='') %}

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
        and data_type <>'JSON'
{% endset %}

{% set col_names = dbt_utils.get_query_results_as_dict(col_names_query) %}

{% set cols = [] %}

{% for col_name in col_names.column_name %}
    {% do cols.append(col_name) %}
{% endfor %}

{{ return(cols) }}

{% endmacro %}
