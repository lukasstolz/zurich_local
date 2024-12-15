select
    {% set cols_keys = get_flat_json_col_keys('stg_shopping', schema_name='staging') -%}

    {% for el in cols_keys -%}
        {{ el[0] -}}->>'{{- el[1] }}' as {{ el[0] -}}_{{- el[1] -}},
    {% endfor %}
from
    {{ ref("stg_shopping") }}
