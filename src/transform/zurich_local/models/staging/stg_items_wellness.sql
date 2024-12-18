select
    {% set json_cols_keys = get_flat_json_col_keys('wellness', schema_name='raw') -%}

    {% for el in json_cols_keys -%}
        {{ el[0] -}}->>'{{- el[1] }}' as {{ el[0] -}}_{{- el[1] | replace(" ", "_") | replace("&", "_")-}},
    {% endfor %}

    {% set non_json_cols = get_non_json_cols('wellness', schema_name='raw') -%}
    {% for col in non_json_cols -%}
        {{- col -}},
    {% endfor %}

    'Wellness' as category_en,
    'Wellness' as category_de
from
    {{ source('zuerich_raw', 'wellness') }}
