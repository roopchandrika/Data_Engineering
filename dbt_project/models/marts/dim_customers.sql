{{ config(materialized='view') }}

select
  customer_id,
  first_name,
  last_name,
  email,
  country
from {{ ref('customers_snapshot') }}
where dbt_valid_to is null