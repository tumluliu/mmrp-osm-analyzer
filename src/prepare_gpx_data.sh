#!/bin/bash

BBOX=$1
GPX_DATA_DIR=$2
# TODO step 1: download GPX from OSM
python osm_gpx_fetcher.py $GPX_DATA_DIR
# step 2: complement the downloaded GPX with elevations from SRTM dataset
./gpx_elev_enhancer.sh $GPX_DATA_DIR
# step 3: generate summary info for each GPX
./gpxinfo_collector.sh $GPX_DATA_DIR
# step 4: reduce summaries into well-structured CSV format
python gpx_summary_reducer.py -c ./reducer_conf.json $GPX_DATA_DIR/summary
# step 5: combine CSV files into one
./combine_gpx_csv_info.sh $GPX_DATA_DIR/summary/csv $GPX_DATA_DIR/summary/csv/munich_gpx_info.csv
