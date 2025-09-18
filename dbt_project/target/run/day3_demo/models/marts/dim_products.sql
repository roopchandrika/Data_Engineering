
  
    

        create or replace transient table DAY3_DEMO.ANALYTICS.dim_products
         as
        (

select
  product_id,
  product_name,
  category,
  price
from DAY3_DEMO.ANALYTICS.stg_products
        );
      
  