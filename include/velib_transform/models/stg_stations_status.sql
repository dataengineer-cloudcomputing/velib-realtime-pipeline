{{ config(materialized='table') }}

with raw_data as (
    select * from {{ source('raw_data', 'stations_status') }}
),

transformed_data as (
    select
        cast(stationcode as STRING) as station_id,
        name as station_name,
        cast(mechanical as INT64) as bikes_mechanical_count,
        cast(ebike as INT64) as bikes_ebike_count,
        cast(numbikesavailable as INT64) as total_bikes_available,
        cast(numdocksavailable as INT64) as docks_available,
        is_renting,
        is_installed,
        nom_arrondissement_communes as commune,
        -- Correction ici : on extrait la lat/lon depuis la colonne coordonnees_geo
        -- Dans l'API v1.0, c'est souvent une chaîne "[lat, lon]" ou déjà splittée
        -- On utilise SAFE_OFFSET pour éviter les erreurs si la donnée est mal formée
        cast(split(trim(coordonnees_geo, '[]'), ',')[SAFE_OFFSET(0)] as FLOAT64) as latitude,
        cast(split(trim(coordonnees_geo, '[]'), ',')[SAFE_OFFSET(1)] as FLOAT64) as longitude,
        cast(extraction_date as TIMESTAMP) as extraction_time
    from raw_data
)

select
    *,
    CASE
        WHEN is_installed = 'NON' OR is_renting = 'NON' THEN 'HORS SERVICE'
        WHEN total_bikes_available = 0 THEN 'STATION VIDE'
        WHEN bikes_mechanical_count > 0 AND bikes_ebike_count > 0 THEN 'VERT ET BLEU DISPOS'
        WHEN bikes_mechanical_count > 0 THEN 'VERT UNIQUEMENT'
        WHEN bikes_ebike_count > 0 THEN 'BLEU UNIQUEMENT'
        ELSE 'INDISPONIBLE'
    END AS bike_operational_status
from transformed_data