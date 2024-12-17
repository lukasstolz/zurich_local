with distinct_types as (
    select
        distinct _type as type
    from {{ ref("zurich_items") }}
    where _type is not null
)

select
    md5(cast(type as string)) as id,
    type,
from
    distinct_types
