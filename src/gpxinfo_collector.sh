#!/bin/bash
# Scan and collect the summaries of all the downloaded GPX files via gpxinfo util

#gpx_dir=/Users/user/Research/data/GPX/Munich
gpx_dir=$1

for gpx_file in "$gpx_dir"/gpx_with_elevations/*.gpx
do
    echo "collecting summary info of $gpx_file ..."
    gpxinfo "$gpx_file" > "$gpx_file.summary"
    echo " done!"
done
mkdir -p "$gpx_dir"/summary
mv "$gpx_dir"/gpx_with_elevations/*.summary "$gpx_dir"/summary
