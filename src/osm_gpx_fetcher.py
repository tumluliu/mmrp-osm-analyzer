# Get public GPS tracks from OpenStreetMap via its GPX API
# The interface is like:
# http://api.openstreetmap.org/api/0.6/trackpoints?bbox=11.360796,48.061602,11.722875,48.248220&page=0
# where the bbox is the geographical bounding box of the target area, page is
# the number of page which contains at most 5000 points

import requests
import argparse
from os import path
from termcolor import colored
from datetime import datetime

# when no more GPX data in the requested page, an empty GPX file will be
# returned by OpenStreetMap GPX API, normally this empty file is 132 bytes long
EMPTY_GPX_LENGTH = 132
OSM_GPX_API = "http://api.openstreetmap.org/api/0.6/trackpoints"
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start_page_no", default=0,
                    help="Page number where the download process start from, \
                    default is 0",
                    type=int)
parser.add_argument("-b", "--bbox",
                    default="11.360796,48.061602,11.722875,48.248220",
                    help="Bounding box of the target area in the form of \
                    BOTTOM,LEFT,TOP,RIGHT \
                    which by default is Munich urban area")
parser.add_argument("GPX_DATA_DIR",
                    help="Directory where raw GPX data files are stored")
args = parser.parse_args()
PAGE_NO = args.start_page_no
# Default bbox is Munich urban area "11.360796,48.061602,11.722875,48.248220"
BBOX = args.bbox
GPX_DATA_DIR = args.GPX_DATA_DIR
chunk_size = 1024

is_download_finished = False
print "# Get GPX data from OpenStreetMap via GPX API v0.6"
print " Bounding box of the target area is : ",
print colored(BBOX, "green")
print " Start downloading GPX data..."

while not is_download_finished:
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    print "[" + timestamp + "] Downloading page " + str(PAGE_NO) + " ...",
    osm_gpx_url = OSM_GPX_API + "?bbox=" + BBOX + "&page=" + str(PAGE_NO)
    response = requests.get(osm_gpx_url, stream=True, timeout=180)
    if not response.ok:
        print colored("done with error code " + str(response.status_code),
                      "red")
    else:
        if 'content-length' in response.headers.keys() \
                and int(response.headers['content-length']) <= EMPTY_GPX_LENGTH:
            is_download_finished = True
            print colored("No GPX track data in this page.", "red")
        else:
            file_name = "tracks_munich_page_" + str(PAGE_NO) + ".gpx"
            local_file = path.join(GPX_DATA_DIR, file_name)
            with open(local_file, 'w') as f:
                for chunk in response.iter_content(chunk_size):
                    f.write(chunk)
            print colored("done with code " + str(response.status_code),
                          "green")
            PAGE_NO += 1
        if (is_download_finished):
            print " All " + str(PAGE_NO) + \
                " GPX files within the target area has been downloaded. "
