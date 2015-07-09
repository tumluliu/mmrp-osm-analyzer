#!/bin/bash
ogr2ogr -append -f PostgreSQL PG:"dbname='tracksdb' user='liulu' password='workhard'" ../data/tracks_munich_page_0_with_elevations.gpx tracks
psql -d tracksdb -U liulu -c "ALTER TABLE tracks ADD COLUMN page_no integer;"
psql -d tracksdb -U liulu -c "ALTER TABLE tracks ADD COLUMN track_id integer;"
for f in $(ls /Users/user/Research/data/GPX/Munich/gpx_with_elevations/*.gpx)
#for f in $(ls ../data/*.gpx)
do
    echo "Importing gpx file $f to PostGIS table..." #, ${f%.*}"
    #ogr2ogr -append -update -f PostgreSQL PG:"dbname='tracksdb' user='liulu' password='workhard'" ../data/$f -nln gpx.osm_munich -sql "SELECT ele, time FROM track_points"
    #ogr2ogr -append -f PostgreSQL PG:"dbname='tracksdb' user='liulu' password='workhard'" $f -sql "SELECT $f as tracks.filename"
    PAGE_NO=`echo $f | cut -d '_' -f 6`
    LAST_ROW=`psql -d tracksdb -c "select count(*) from tracks;" | sed "3q;d" | xargs`
    ogr2ogr -append -f PostgreSQL PG:"dbname='tracksdb' user='liulu' password='workhard'" $f tracks
    psql -d tracksdb -U liulu -c "UPDATE tracks SET page_no='$PAGE_NO', track_id=(ogc_fid-$LAST_ROW-1) WHERE ogc_fid > $LAST_ROW;"
done
psql -d tracksdb -U liulu -c "DELETE FROM tracks where page_no is NULL;"
