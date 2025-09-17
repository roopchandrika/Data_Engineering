{{ config(materialized='view') }}

with f as (
  select * from {{ ref('fact_orders') }}
),
c as (
  select * from {{ ref('dim_customers') }}  -- current version only
),
p as (
  select * from {{ ref('dim_products') }}
)
select
  c.country,
  p.category,
  date_trunc('day', f.order_date) as order_day,
  sum(f.total_amount)             as total_sales,
  count(distinct f.order_id)      as order_count
from f
left join c on f.customer_id = c.customer_id
left join p on f.product_id = p.product_id
group by c.country, p.category, date_trunc('day', f.order_date)