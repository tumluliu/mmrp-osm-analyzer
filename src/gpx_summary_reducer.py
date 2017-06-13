# Reduce the GPX summary into a well-structured CSV file
# Created by Lu Liu
# 2015-05-09

from os import listdir
from os.path import isfile, join, splitext
from collections import OrderedDict
import json
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="reducer_conf.json",
                    help="JSON format config file for GPX summary reducer")
parser.add_argument("GPX_SUMMARY_DIR",
                    help="Directory where GPX summary files are stored")
args = parser.parse_args()
CONFIG_FILE = args.config
GPX_SUMMARY_DIR = args.GPX_SUMMARY_DIR

with open(CONFIG_FILE) as colname_file:
    colnames = json.load(colname_file, object_pairs_hook=OrderedDict)

gpx_sum_files = [f for f in listdir(GPX_SUMMARY_DIR) if isfile(join(GPX_SUMMARY_DIR, f))]
# There are normally 12 lines of summary info for each Track Segment
track_seg_info_lines = 16
track_seg_info = OrderedDict()
na_string_list = ["n/a", "None", "none", "N/A", "NA"]

for gpx_sum_file in gpx_sum_files:
    f = open(join(GPX_SUMMARY_DIR, gpx_sum_file))
    file_name, extension = splitext(gpx_sum_file)
    # summary file name is like this:
    # tracks_munich_page_88_with_elevations.gpx.summary
    gpx_id = file_name.split('.')[0].split('_')[0]
    condensed_gpx_sum_file = file_name + ".csv"
    csv_f = open(join(GPX_SUMMARY_DIR, "csv", condensed_gpx_sum_file), 'w')
    # write header line to CSV
    csv_f.write("gpx_id," + str(",".join(colnames.values())) + "\n")
    print "Reducing GPX summary file " + gpx_sum_file + \
        " to CSV file " + file_name + ".csv ...",
    #print str(",".join(colnames.values()))
    track_cursor = 0
    is_track_recorder_on = False
    for line in f.readlines():
        #print line
        if re.match(r".*Track.*Segment.*", line):
            #print "processing " + line.strip() + " ..."
            # start assembling a CSV row for each track segment
            # info block
            is_track_recorder_on = True
            for s in line.strip().split(','):
                track_seg_info[colnames[s.split()[0]]] = s.split()[1][1:]
            track_cursor += 2
        elif (is_track_recorder_on) and (track_cursor <= track_seg_info_lines):
            key = colnames[line.strip().split(':')[0]]
            if re.match(r".*Length 2D.*", line):
                track_seg_info[key] = \
                    str(float(line.strip().split(':')[1][1:-2]) * 1000.)
                track_cursor += 1
            if re.match(r".*Length 3D.*", line):
                track_seg_info[key] = \
                    str(float(line.strip().split(':')[1][1:-2]) * 1000.)
                track_cursor += 1
            if re.match(r".*Moving time.*", line):
                if line.strip().split(':')[1][1:] in na_string_list:
                    track_seg_info[key] = "NA"
                else:
                    track_seg_info[key] = line.strip().split(':', 1)[1][1:]
                track_cursor += 1
            if re.match(r".*Stopped time.*", line):
                if line.strip().split(':')[1][1:] in na_string_list:
                    track_seg_info[key] = "NA"
                else:
                    track_seg_info[key] = line.strip().split(':', 1)[1][1:]
                track_cursor += 1
            if re.match(r".*Max speed.*", line):
                track_seg_info[key] = line.strip().split(':')[1].split('=')[0][1:-4]
                track_cursor += 1
            if re.match(r".*Total uphill.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:-1]
                track_cursor += 1
            if re.match(r".*Total downhill.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:-1]
                track_cursor += 1
            if re.match(r".*Started.*", line):
                if line.strip().split(':', 1)[1][1:] in na_string_list:
                    track_seg_info[key] = "NA"
                else:
                    track_seg_info[key] = line.strip().split(':', 1)[1][1:]
                track_cursor += 1
            if re.match(r".*Ended.*", line):
                if line.strip().split(':', 1)[1][1:] in na_string_list:
                    track_seg_info[key] = "NA"
                else:
                    track_seg_info[key] = line.strip().split(':', 1)[1][1:]
                track_cursor += 1
            if re.match(r".*Points.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:]
                track_cursor += 1
            if re.match(r".*Start location longitude.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:]
                track_cursor += 1
            if re.match(r".*Start location latitude.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:]
                track_cursor += 1
            if re.match(r".*End location longitude.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:]
                track_cursor += 1
            if re.match(r".*End location latitude.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:]
                track_cursor += 1
            if re.match(r".*Avg distance between points.*", line):
                track_seg_info[key] = line.strip().split(':')[1][1:-1]
                track_cursor += 1
        if (is_track_recorder_on) and (track_cursor == track_seg_info_lines + 1):
            #print " A track segment has been processed!"
            #print str(",".join(track_seg_info.values()))
            csv_f.write(str(gpx_id) + "," + \
                        str(",".join(track_seg_info.values())) + "\n")
            #print track_seg_info.values()
            is_track_recorder_on = False
            track_cursor = 0
            track_seg_info.clear()
    csv_f.close()
    f.close()
    print " done!"
