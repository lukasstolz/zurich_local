select
    md5(cast(name_de as string) || ':' || cast(category_de as string) || ':' || cast(address_addressLocality as string)) as id,
    md5(cast(_type as string)) as type_id,
    md5(cast(_customtype as string)) as custom_type_id,
    md5(cast(address_addressLocality as string) || ':' || cast(address_addressCountry as string) ) as city_id,
    md5(cast(category_de as string)) as category_id,
    {{ dbt_utils.star(from=ref('zurich_items'),
    except=[
        "_type",
        "_customtype",
        "address_addressLocality",
        "address_addressCountry",
        "identifier",
        "osm_id",
        "license",
        "datemodified"
    ]) }}
from
    {{ ref('zurich_items') }}
