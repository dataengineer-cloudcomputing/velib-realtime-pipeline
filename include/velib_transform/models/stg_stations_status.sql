{{ config(materialized='table') }}

with raw_data as (
    select * from {{ source('raw_data', 'stations_status') }}
)

select
    cast(stationcode as STRING) as station_id,
    name as station_name,
    cast(numbikesavailable as INT64) as bikes_available,
    cast(numdocksavailable as INT64) as docks_available,
    -- On transforme les strings en nombres décimaux pour la géographie
    cast(lat as FLOAT64) as latitude,
    cast(lon as FLOAT64) as longitude,
    cast(extraction_date as TIMESTAMP) as extraction_time
from raw_data