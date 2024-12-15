select *
from {{ source('zuerich_raw', 'shopping') }}
