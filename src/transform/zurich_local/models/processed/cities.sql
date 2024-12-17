with distinct_localities as (
    select
        distinct address_addressLocality as city, address_addressCountry as country
    from {{ ref("zurich_items") }}
)

select
    md5(cast(city as string) || ':' || cast(country as string) ) as id,
    city,
    country
from
    distinct_localities
