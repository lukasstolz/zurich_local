with distinct_categories as (
    select
        distinct category_de, category_en
    from {{ ref("zurich_items") }}
)

select
    md5(cast(category_de as string)) as id,
    category_de,
    category_en
from
    distinct_categories
