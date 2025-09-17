{% snapshot customers_snapshot %}
{{
  config(
    target_schema='ANALYTICS',
    target_database='DAY3_DEMO',
    unique_key='customer_id',
    strategy='check',
    check_cols=['first_name','last_name','email','country']
  )
}}
select * from {{ ref('stg_customers') }}
{% endsnapshot %}