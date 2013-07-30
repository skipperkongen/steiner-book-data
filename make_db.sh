#!/bin/sh

python make_geodata.py

ogr2ogr -f PostgreSQL PG:"host=localhost user=kostas dbname=steiner" all_terminals.shp -a_srs "epsg:3857"
ogr2ogr -f PostgreSQL PG:"host=localhost user=kostas dbname=steiner" all_steiner.shp -a_srs "epsg:3857"
ogr2ogr -f PostgreSQL PG:"host=localhost user=kostas dbname=steiner" all_edges.shp -a_srs "epsg:3857"
