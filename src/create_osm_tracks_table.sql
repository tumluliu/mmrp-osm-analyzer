DROP TABLE IF EXISTS trackinfo;

CREATE TABLE trackinfo(
    page_no integer,
    track_id integer,
    segment_id integer,
    length_2d double precision,
    length_3d double precision,
    moving_time interval,
    stopped_time interval,
    max_speed double precision,
    uphill double precision,
    downhill double precision,
    started timestamp,
    ended timestamp,
    points integer,
    start_lon double precision,
    start_lat double precision,
    end_lon double precision,
    end_lat double precision,
    avg_point_distance double precision
);

\COPY trackinfo FROM '../data/munich_gpx_info.csv' WITH CSV HEADER;
