# Append elevations to GPX files
# 2015-05-08
# Lu LIU
#

from os import listdir
from os.path import isfile, join
import srtm
import gpxpy

gpx_file_dir = "/Users/user/Research/data/GPX/Munich"
gpx_files = [f for f in listdir(gpx_file_dir) if isfile(join(gpx_file_dir, f))]
for gpx_file in gpx_files:
    print "add elevations for " + gpx_file + "...",
    gpx = gpxpy.parse(open(join(gpx_file_dir, gpx_file)))
    elev_data = srtm.get_data()
    elev_data.add_elevations(gpx, smooth=True)
    print " done!"
