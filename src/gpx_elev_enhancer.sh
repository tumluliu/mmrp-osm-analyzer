#!/bin/bash
# Add elevations to GPX data from SRTM

gpx_dir=/Users/user/Research/data/GPX/Munich

for gpx_file in "$gpx_dir"/*.gpx
do
    echo "appending elevations to $gpx_file ..."
    gpxelevations -o -p -s $gpx_file
    echo "done! "
done
mkdir -p "$gpx_dir"/gpx_with_elevations
mv "$gpx_dir"/*_with_elevations.gpx "$gpx_dir"/gpx_with_elevations

