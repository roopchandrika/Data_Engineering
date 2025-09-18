
  create or replace   view DAY3_DEMO.ANALYTICS.stg_customers
  
   as (
    

select
  cast(CUSTOMER_ID as int)           as customer_id,
  trim(FIRST_NAME)                   as first_name,
  trim(LAST_NAME)                    as last_name,
  lower(trim(EMAIL))                 as email,
  trim(COUNTRY)                      as country
from DAY3_DEMO.RAW.CUSTOMERS_STAGE
where CUSTOMER_ID is not null
  );

