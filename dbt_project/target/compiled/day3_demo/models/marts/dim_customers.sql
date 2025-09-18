

select
  customer_id,
  first_name,
  last_name,
  email,
  country
from DAY3_DEMO.ANALYTICS.customers_snapshot
where dbt_valid_to is null