
  create or replace   view DAY3_DEMO.ANALYTICS.stg_products
  
   as (
    

select
  cast(PRODUCT_ID as int)            as product_id,
  trim(PRODUCT_NAME)                 as product_name,
  trim(CATEGORY)                     as category,
  cast(PRICE as number(10,2))        as price
from DAY3_DEMO.RAW.PRODUCTS_STAGE
where PRODUCT_ID is not null
  );

