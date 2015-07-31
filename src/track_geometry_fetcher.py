import json
import requests
import logging.config
import os
import argparse
import sys

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
parser.add_argument(
    "OUTPUT_DIR",
    help="where the track geometry GeoJSON files will be stored")
parser.add_argument(
    "START_PAGE", default=1,
    help="specify the start page number of the tracks")
args = parser.parse_args()
OUTPUT_DIR = args.OUTPUT_DIR
START_PAGE = int(args.START_PAGE)

INVALID_TRACKS = [184, 321, 358, 369, 525, 619, 621, 686, 687, 688, 702, 716,
                  734, 741, 755, 838, 839, 878, 910, 945, 953, 954, 955, 964,
                  968, 984, 995, 998, 999, 1004, 1005, 1007, 1009, 1011, 1012,
                  1014, 1016, 1017, 1020, 1021, 1024, 1026, 1030, 1031, 1032,
                  1081, 1138, 1149, 1188, 1216, 1289, 1290, 1396, 1399, 1419,
                  1428, 1460, 1523, 1557, 1652, 1753, 1757, 1758, 1869, 1878,
                  1880, 1882, 1951, 2046, 2148, 2158, 2166, 2191, 2197, 2240,
                  2245, 2265, 2266, 2301, 2362, 2477]

trackinfo_api_url = "http://localhost:5000/api/trackinfo"
tracks_api_url = "http://localhost:5000/api/tracks"

r = requests.get(trackinfo_api_url,
                 headers={'content-type': 'application/json'})
response = json.loads(r.content)
page = int(response['page'])
total_pages = int(response['total_pages'])

for p in range(START_PAGE, total_pages+1):
    logging.info('[INFO] Fetch page %s of %s trackinfo',
                 str(p), str(total_pages))
    r = requests.get(trackinfo_api_url + '?page=' + str(p),
                     headers={'content-type': 'application/json'})
    if not r.ok:
        logging.error("[ERROR] Fetch trackinfo error: %s", str(r.status_code))
    else:
        response = json.loads(r.content)
        for ti in response['objects']:
            logging.info('[INFO] Fetch geometry of track ogc_fid=%s',
                         str(ti['ID']))
            if ti['ID'] in INVALID_TRACKS:
                continue
            track_req = requests.get(
                tracks_api_url + '/' + str(ti['ID']),
                headers={'content-type': 'application/json'})
            if not track_req.ok:
                logging.error("[ERROR] Fetch track geometry error: %s",
                              str(track_req.status_code))
                if track_req.status_code == 500:
                    logging.fatal(
                        "[FATAL] Server fault occurs! page_no: %s, ogc_fid: %s",
                        str(p), str(ti['ID']))
                    sys.exit()
            else:
                track_resp = json.loads(track_req.content)
                track_geom = track_resp['GeoJSON']
                track_geom_file = str(ti['ID']) + '_track' + '.geojson'
                logging.info('[INFO] Writing geometry to geojson file')
                with (open(os.path.join(OUTPUT_DIR, track_geom_file),
                           'w')) as track_file:
                    track_file.write(json.dumps(track_geom))
