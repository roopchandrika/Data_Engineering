
      
  
    

        create or replace transient table DAY3_DEMO.ANALYTICS.customers_snapshot
         as
        (
    

    select *,
        md5(coalesce(cast(customer_id as varchar ), '')
         || '|' || coalesce(cast(to_timestamp_ntz(convert_timezone('UTC', current_timestamp())) as varchar ), '')
        ) as dbt_scd_id,
        to_timestamp_ntz(convert_timezone('UTC', current_timestamp())) as dbt_updated_at,
        to_timestamp_ntz(convert_timezone('UTC', current_timestamp())) as dbt_valid_from,
        
  
  coalesce(nullif(to_timestamp_ntz(convert_timezone('UTC', current_timestamp())), to_timestamp_ntz(convert_timezone('UTC', current_timestamp()))), null)
  as dbt_valid_to

    from (
        

select * from DAY3_DEMO.ANALYTICS.stg_customers
    ) sbq



        );
      
  
  