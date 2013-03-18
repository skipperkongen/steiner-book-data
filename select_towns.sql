SELECT 
    x, y, 3857 as srid, name, place, population
FROM
    (
    SELECT 
        cast(st_x(ST_Transform(geom,3857)) as int) as x, 
        cast(st_y(ST_Transform(geom,3857)) as int) as y, 
        tags->'name' as name, 
        tags->'place' as place,
        CASE WHEN tags->'population' <> '' THEN cast(tags->'population' as int) ELSE -1 END as population 
    FROM 
        nodes 
    WHERE 
        tags->'place' in ('city','town', 'village', 'hamlet')
    ) foo
ORDER BY place asc, population desc
;
