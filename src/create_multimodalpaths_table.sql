-- scripts for creating multimodalpathinfo table
DROP TABLE IF EXISTS multimodalpathinfo;

CREATE TABLE multimodalpathinfo
(
    ogc_fid integer NOT NULL,
    page_no integer,
    track_id integer,
    summary character varying, 
    distance double precision,
    duration double precision,
    walking_distance double precision,
    walking_duration double precision,
    geojson character varying,
    switch_points integer,
    existence boolean
)
WITH (
    OIDS=FALSE
);

ALTER TABLE multimodalpathinfo
OWNER TO liulu;

\COPY multimodalpathinfo FROM '../data/multimodal_routing_results.csv' WITH CSV HEADER;
