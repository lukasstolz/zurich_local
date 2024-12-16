with localities as (
    select distinct address_addressLocality, address_addressCountry
        from
    {{ ref("stg_activities") }}

    union

    select distinct address_addressLocality, address_addressCountry
        from
    {{ ref("stg_shopping") }}
),

distinct_localities as (
    select
        distinct address_addressLocality as city, address_addressCountry as country
    from localities
)

select
    md5(cast(city as string) || ':' || cast(country as string) ) as id,
    city,
    country
from
    distinct_localities
