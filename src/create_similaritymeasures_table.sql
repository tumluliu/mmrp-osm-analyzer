-- scripts for creating similaritymeasures tables
DROP TABLE IF EXISTS dtw;

CREATE TABLE dtw
(
    fileid character varying,
    fid integer NOT NULL,
    dist double precision,
    ratio double precision
)
WITH (
    OIDS=FALSE
);

ALTER TABLE dtw
OWNER TO liulu;

\COPY dtw FROM '../data/dtw.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS editdist;

CREATE TABLE editdist
(
    fileid character varying,
    fid integer NOT NULL,
    dist double precision,
    ratio double precision
)
WITH (
    OIDS=FALSE
);

ALTER TABLE editdist
OWNER TO liulu;

\COPY editdist FROM '../data/editdist.csv' WITH CSV HEADER;

DROP TABLE IF EXISTS lcss;

CREATE TABLE lcss
(
    fileid character varying,
    fid integer NOT NULL,
    dist double precision,
    ratio double precision
)
WITH (
    OIDS=FALSE
);

ALTER TABLE lcss
OWNER TO liulu;

\COPY lcss FROM '../data/lcss.csv' WITH CSV HEADER;
