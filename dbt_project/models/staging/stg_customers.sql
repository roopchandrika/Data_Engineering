{{ config(materialized='view') }}

select
  cast(CUSTOMER_ID as int)           as customer_id,
  trim(FIRST_NAME)                   as first_name,
  trim(LAST_NAME)                    as last_name,
  lower(trim(EMAIL))                 as email,
  trim(COUNTRY)                      as country
from {{ source('raw','CUSTOMERS_STAGE') }}
where CUSTOMER_ID is not null