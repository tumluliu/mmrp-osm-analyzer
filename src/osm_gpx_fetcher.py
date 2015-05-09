# Get public GPS tracks from OpenStreetMap via its GPX API
# The interface is like:
# http://api.openstreetmap.org/api/0.6/trackpoints?bbox=11.360796,48.061602,11.722875,48.248220&page=0
# where the bbox is the geographical bounding box of the target area, page is
# the number of page which contains at most 5000 points

import requests
from os import path
from termcolor import colored

osm_gpx_api = "http://api.openstreetmap.org/api/0.6/trackpoints?bbox="
munich_bbox = "11.360796,48.061602,11.722875,48.248220"
gpx_data_dir = "/Users/user/Research/data/GPX/Munich"
page_no = 0
chunk_size = 1024

#while (True):
print "# Get GPX data for Munich area from OpenStreetMap"
print " Bounding box of the target area is : ",
print colored("(11.360796,48.061602,11.722875,48.248220).", "green")
print " Fetch 20 pages of GPX data. Here we go..."
while (page_no < 20):
    print "fetching page " + str(page_no) + " ...",
    osm_gpx_url = osm_gpx_api + munich_bbox + "&page=" + str(page_no)
    response = requests.get(osm_gpx_url, stream=True)
    if not response.ok:
        print colored("done with error code " + str(response.status_code), "red")
    else:
        print colored("done with code " + str(response.status_code), "green")
    file_name = "tracks_munich_page_" + str(page_no) + ".gpx"
    local_file = path.join(gpx_data_dir, file_name)
    with open(local_file, 'w') as f:
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)
    page_no += 1
