{{ config(materialized='table') }}

with o as (
  select * from {{ ref('stg_orders') }}
),
p as (
  select * from {{ ref('dim_products') }}
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