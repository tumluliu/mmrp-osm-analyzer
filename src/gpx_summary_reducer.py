# Reduce the GPX summary into well-structured CSV files

from os import listdir
from os.path import isfile, join

gpx_summary_dir = "/Users/user/Research/data/GPX/Munich/summary"
gpx_sum_files = [f for f in listdir(gpx_summary_dir) if isfile(join(gpx_summary_dir, f))]
for gpx_sum in gpx_sum_files:
    with open(gpx_sum) as f:
        for line in f.readlines():
            # do stuff
            print line
