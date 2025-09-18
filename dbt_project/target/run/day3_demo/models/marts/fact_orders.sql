
  
    

        create or replace transient table DAY3_DEMO.ANALYTICS.fact_orders
         as
        (

with o as (
  select * from DAY3_DEMO.ANALYTICS.stg_orders
),
p as (
  select * from DAY3_DEMO.ANALYTICS.dim_products
)
select
  o.order_id,
  o.order_date,
  o.customer_id,
  o.product_id,
  o.quantity,
  p.price,
  (o.quantity * p.price) as total_amount
from o
left join p on o.product_id = p.product_id
        );
      
  