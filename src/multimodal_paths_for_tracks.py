#!/usr/bin/env python

"""
author: Lu LIU
created at: 2015-07-28
Description:
    Calculate the multimodal paths between every source-target pair of the GPX
    tracks collected from OpenStreetMap within Munich area. The routing profile
    is from some pre-defined templates available under the 'profile-templates/'
    directory.
"""

from pymmrouting.routeplanner import MultimodalRoutePlanner
from pymmrouting.inferenceengine import RoutingPlanInferer
import datetime
import argparse
import json
import logging.config
import os
import csv
import copy

LOGGING_CONF_FILE = 'logging.json'
DEFAULT_LOGGING_LVL = logging.WARN
path = LOGGING_CONF_FILE
value = os.getenv('LOG_CFG', None)
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("SOURCE_TARGET_FILE",
                    help="The CSV file containing source-target pairs of tracks")
parser.add_argument("ROUTING_PROFILE",
                    help="User-defined options about travelling")
parser.add_argument("OUTPUT_DIR",
                    help="where the multimodal paths GeoJSON files will be stored")
parser.add_argument("-c", "--APP-CONFIG", default="config.json",
                    help="config for client application")
args = parser.parse_args()
SOURCE_TARGET_FILE = args.SOURCE_TARGET_FILE
ROUTING_PROFILE = args.ROUTING_PROFILE
OUTPUT_DIR = args.OUTPUT_DIR
CONFIG_FILE = args.APP_CONFIG

def _normalize(r):
    r['ogc_fid']   = int(r['ogc_fid'])
    r['page_no']   = int(r['page_no'])
    r['track_id']  = int(r['track_id'])
    r['start_lon'] = float(r['start_lon'])
    r['start_lat'] = float(r['start_lat'])
    r['end_lon']   = float(r['end_lon'])
    r['end_lat']   = float(r['end_lat'])
    return r

tracks_st_info = []
with open(SOURCE_TARGET_FILE) as tracks_file:
    track_reader = csv.DictReader(tracks_file)
    for row in track_reader:
        tracks_st_info.append(_normalize(row))

with open(ROUTING_PROFILE) as f:
    routing_profile = json.load(f)

track_profiles = []
for ti in tracks_st_info:
    tp = copy.deepcopy(routing_profile)
    tp['source']['value']['x'] = ti['start_lon']
    tp['source']['value']['y'] = ti['start_lat']
    tp['target']['value']['x'] = ti['end_lon']
    tp['target']['value']['y'] = ti['end_lat']
    tp['trackinfo'] = {}
    tp['trackinfo']['ogc_fid'] = ti['ogc_fid']
    tp['trackinfo']['page_no'] = ti['page_no']
    tp['trackinfo']['track_id'] = ti['track_id']
    track_profiles.append(tp)

with (open(os.path.join(OUTPUT_DIR, "multimodal_routing_results.csv"), 'w')) as result_file:
    colnames = ['ogc_fid', 'page_no', 'track_id', 'summary', 'distance',
                'duration', 'walking_distance', 'walking_duration',
                'geojson', 'switch_points', 'existence']
    result_writer = csv.DictWriter(result_file, fieldnames=colnames)
    result_writer.writeheader()
    for i, tp in enumerate(track_profiles):
        logging.info("==== Processing track " + str(i) + " ====")
        logging.info("Fetch raw track geometry")
        track_file_name = '_'.join([
            str(tp['trackinfo']['ogc_fid']),
            str(tp['trackinfo']['page_no']),
            str(tp['trackinfo']['track_id']),
        ])
        logging.info("Multimodal routing from " + \
                     str(tp['source']['value']['x']) + ',' + \
                     str(tp['source']['value']['y']) + ' to ' + \
                     str(tp['target']['value']['x']) + ',' + \
                     str(tp['target']['value']['y']))
        inferer = RoutingPlanInferer()
        inferer.load_routing_options(tp)
        routing_plans = inferer.generate_routing_plan()
        route_planner = MultimodalRoutePlanner()
        final_results = route_planner.batch_find_path(routing_plans)
        for i, r in enumerate(final_results["routes"]):
            path_file_name = track_file_name + '_' + str(i+1) + '.geojson'
            with (open(os.path.join(OUTPUT_DIR, path_file_name), 'w')) as path_file:
                path_file.write(json.dumps(r['geojson']))
            logging.debug("== " + str(i + 1) + ". " + r["summary"] + " ==")
            logging.debug("Total distance: %s meters", str(r["distance"]))
            logging.debug("Total time (estimated): %s ",
                          str(datetime.timedelta(minutes=float(r["duration"]))))
            logging.debug("Total walking distance: %s meters",
                          str(r["walking_distance"]))
            logging.debug("Total walking time (estimated): %s",
                          str(datetime.timedelta(
                              minutes=float(r["walking_duration"]))))
            r.update({
                'ogc_fid':  tp['trackinfo']['ogc_fid'],
                'page_no':  tp['trackinfo']['page_no'],
                'track_id': tp['trackinfo']['track_id']
            })
            r['geojson'] = path_file_name
            switch_points_count = len(r['switch_points'])
            r['switch_points'] = switch_points_count
            result_writer.writerow(r)
            #print "Multimodal path: "
            #print str(r["geojson"])
            #print "Switch Points along the path: "
            #for sp in r["switch_points"]:
                #print colored((sp['properties']['switch_type'] + ": "), "blue")
                #print str(sp)
        #with (open("../tmp/multimodal_routing_results.json", 'w')) as result_file:
            #result_file.write(json.dumps(final_results))
        route_planner.cleanup()
