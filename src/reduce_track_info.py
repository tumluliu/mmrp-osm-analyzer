#!/usr/bin/python
# Reduce the GPX track segments summary for each track
# Created by Lu Liu
# 2015-07-15

from os import listdir
from os.path import isfile, join, splitext
from itertools import groupby
from datetime import datetime, timedelta
import json
import re
import argparse
import csv
import operator

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--tracksegfile",
                    help="Input CSV file of GPX track segment infomation")
parser.add_argument("-o", "--trackfile",
                    help="Output CSV file of GPX track information")
args = parser.parse_args()
TRACK_SEG_FILE = args.tracksegfile
TRACK_FILE = args.trackfile

def _get_timedelta(timespanstr):
    if not timespanstr:
        # empty string
        return ''
    unzipped_timespan = timespanstr.split(':')
    return timedelta(hours=int(unzipped_timespan[0]),
                     minutes=int(unzipped_timespan[1]),
                     seconds=int(unzipped_timespan[2]))

def _get_datetime(timestr):
    if not timestr:
        return ''
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

def _normalize(r):
    r['page_no'] = int(r['page_no'])
    r['track_id'] = int(r['track_id'])
    r['segment_id'] = int(r['segment_id'])
    return r

track_segs = []
with open(TRACK_SEG_FILE) as track_seg_file:
    track_seg_reader = csv.DictReader(track_seg_file)
    for row in track_seg_reader:
        track_segs.append(_normalize(row))

print 'There are ' + str(len(track_segs)) + ' track segments'
track_segs.sort(key=operator.itemgetter('segment_id'))
track_segs.sort(key=operator.itemgetter('track_id'))
track_segs.sort(key=operator.itemgetter('page_no'))
#print 'First lines of track_segs: '
#for t in track_segs[0:15]:
    #print 'page_no: ' + str(t['page_no']) + 'track_id: ' + str(t['track_id']) + 'seg_id: ' + str(t['segment_id'])
grouped_seg_info = []
page_track_key = []
for k, g in groupby(track_segs, lambda seg: str(seg['page_no']) + str(seg['track_id'])):
    grouped_seg_info.append(list(g))
    page_track_key.append(k)

track_info_list = []
print 'There are ' + str(len(grouped_seg_info)) + ' tracks aggregated from segemnts'
#print 'First lines of grouped_seg_info: '
#for t in grouped_seg_info[0:15]:
    #print 'page_no: ' + str(t[0]['page_no']) + 'track_id: ' + str(t[0]['track_id']) + 'seg_id: ' + str(t[0]['segment_id'])
for tr in grouped_seg_info:
    track_info = {}
    track_info['page_no'] = tr[0]['page_no']
    track_info['track_id'] = tr[0]['track_id']
    track_info['segments'] = len(tr)
    track_info['length_2d'] = sum([float(seg['length_2d']) for seg in tr])
    track_info['length_3d'] = sum([float(seg['length_3d']) for seg in tr])
    moving_time_list = [_get_timedelta(seg['moving_time']) for seg in tr]
    track_info['moving_time'] = '' if '' in moving_time_list else str(sum(moving_time_list, timedelta()))
    stopped_time_list = [_get_timedelta(seg['stopped_time']) for seg in tr]
    track_info['stopped_time'] = '' if '' in stopped_time_list else str(sum(stopped_time_list, timedelta()))
    track_info['max_speed'] = max([float(seg['max_speed']) for seg in tr])
    track_info['uphill'] = sum([float(seg['uphill']) for seg in tr])
    track_info['downhill'] = sum([float(seg['downhill']) for seg in tr])
    started_list = [_get_datetime(seg['started']) for seg in tr]
    track_info['started'] = '' if '' in started_list else str(min(started_list))
    ended_list = [_get_datetime(seg['ended']) for seg in tr]
    track_info['ended'] = '' if '' in ended_list else str(max(ended_list))
    track_info['points'] = sum([int(seg['points']) for seg in tr])
    track_info['start_lon'] = tr[0]['start_lon']
    track_info['start_lat'] = tr[0]['start_lat']
    track_info['end_lon'] = tr[-1]['end_lon']
    track_info['end_lat'] = tr[-1]['end_lat']
    track_info['avg_point_distance'] = sum(
        [float(seg['avg_point_distance']) * int(seg['points']) for seg in tr]) / float(track_info['points'])
    track_info_list.append(track_info)

with open(TRACK_FILE, 'w') as track_file:
    colnames = track_info_list[0].keys()
    track_info_writer = csv.DictWriter(track_file, fieldnames=colnames)
    track_info_writer.writeheader()
    for tr in track_info_list:
        track_info_writer.writerow(tr)
