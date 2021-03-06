-- scripts for trackseginfo
DROP TABLE IF EXISTS trackseginfo;

CREATE TABLE trackseginfo(
    page_no            integer,
    track_id           integer,
    segment_id         integer,
    length_2d          double precision,
    length_3d          double precision,
    moving_time        interval,
    stopped_time       interval,
    max_speed          double precision,
    uphill             double precision,
    downhill           double precision,
    started            timestamp,
    ended              timestamp,
    points             integer,
    start_lon          double precision,
    start_lat          double precision,
    end_lon            double precision,
    end_lat            double precision,
    avg_point_distance double precision
);

\COPY trackseginfo FROM '../data/munich_gpx_info.csv' WITH CSV HEADER;

SELECT AddGeometryColumn('public', 'trackseginfo', 'start_geom', 4326, 'POINT', 2);

SELECT AddGeometryColumn('public', 'trackseginfo', 'end_geom', 4326, 'POINT', 2);

UPDATE trackseginfo SET start_geom = ST_SetSRID(ST_MakePoint(start_lon, start_lat), 4326);

UPDATE trackseginfo SET end_geom = ST_SetSRID(ST_MakePoint(end_lon, end_lat), 4326);

CREATE INDEX trackseginfo_start_geom ON trackseginfo USING GIST (start_geom);

CREATE INDEX trackseginfo_end_geom ON trackseginfo USING GIST (end_geom);

-- scripts for trackinfo
DROP TABLE IF EXISTS trackinfo;

CREATE TABLE trackinfo(
    page_no            integer,
    track_id           integer,
    segments           integer,
    length_2d          double precision,
    length_3d          double precision,
    moving_time        interval,
    stopped_time       interval,
    max_speed          double precision,
    uphill             double precision,
    downhill           double precision,
    started            timestamp,
    ended              timestamp,
    points             integer,
    start_lon          double precision,
    start_lat          double precision,
    end_lon            double precision,
    end_lat            double precision,
    avg_point_distance double precision
);

\COPY trackinfo (end_lon,length_3d,downhill,start_lon,started,avg_point_distance,segments,moving_time,track_id,uphill,ended,max_speed,end_lat,start_lat,length_2d,stopped_time,page_no,points) FROM '../data/munich_track_info.csv' WITH CSV HEADER;

SELECT AddGeometryColumn('public', 'trackinfo', 'start_geom', 4326, 'POINT', 2);

SELECT AddGeometryColumn('public', 'trackinfo', 'end_geom', 4326, 'POINT', 2);

UPDATE trackinfo SET start_geom = ST_SetSRID(ST_MakePoint(start_lon, start_lat), 4326);

UPDATE trackinfo SET end_geom = ST_SetSRID(ST_MakePoint(end_lon, end_lat), 4326);

CREATE INDEX trackinfo_start_geom ON trackinfo USING GIST (start_geom);

CREATE INDEX trackinfo_end_geom ON trackinfo USING GIST (end_geom);

ALTER TABLE "trackinfo" ADD COLUMN "ogc_fid" INTEGER;
UPDATE trackinfo SET ogc_fid = tracks.ogc_fid FROM tracks WHERE trackinfo.page_no = tracks.page_no AND trackinfo.track_id = tracks.track_id;
ALTER TABLE "trackinfo"
  ALTER COLUMN "ogc_fid" SET NOT NULL;
ALTER TABLE "trackinfo" ADD UNIQUE ("ogc_fid");
ALTER TABLE "trackinfo" ADD PRIMARY KEY ("ogc_fid");
