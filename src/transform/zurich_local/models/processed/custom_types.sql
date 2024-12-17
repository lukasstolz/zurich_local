with distinct_custom_types as (
    select
        distinct _customtype as custom_type
    from {{ ref("zurich_items") }}
    where _customtype is not null
)

select
    md5(cast(custom_type as string)) as id,
    custom_type,
from
    distinct_custom_types
