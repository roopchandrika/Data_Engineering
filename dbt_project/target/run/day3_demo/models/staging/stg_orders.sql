
  create or replace   view DAY3_DEMO.ANALYTICS.stg_orders
  
   as (
    

select
  cast(ORDER_ID as int)              as order_id,
  cast(CUSTOMER_ID as int)           as customer_id,
  cast(PRODUCT_ID as int)            as product_id,
  cast(ORDER_DATE as date)           as order_date,
  cast(QUANTITY as int)              as quantity
from DAY3_DEMO.RAW.ORDERS_STAGE
where ORDER_ID is not null
  );

