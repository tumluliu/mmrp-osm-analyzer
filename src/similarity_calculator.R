library(SimilarityMeasures)
library(rgdal)
library(data.table)

MakeTrackTuple <- function(f) {
    fid <- unlist(strsplit(tail(unlist(strsplit(f, "/")), n=1), "_"))[1]
    geom <- readOGR(f, layer="OGRGeoJSON", require_geomType="wkbLineString")
    return(c(fid, geom))
}

MakePathTuple <- function(f) {
    fileid <- unlist(strsplit(tail(unlist(strsplit(f, "/")), n=1), "[.]"))[1]
    fid <- unlist(strsplit(tail(unlist(strsplit(f, "/")), n=1), "_"))[1]
    geom <- tryCatch(readOGR(f, layer="OGRGeoJSON", require_geomType="wkbLineString"), 
                     error=function(e) NA) 
    if (!is.na(geom)) return(c(fileid, fid, geom)) else return(NA)
}

CalculateSimilarity <- function(track.coords, path.coords, FUN=SimilarityMeasures::Frechet, ...) {
    track.path <- lapply(path.coords, function(p) list(fileid=p[["fileid"]],
                                                       fid=p[["fid"]], 
                                                       path=p[["coords"]], 
                                                       track=track.coords[sapply(track.coords, function(t) t[["fid"]]==p[["fid"]])] 
                                                       ))
    track.path <- track.path[sapply(track.path, function(tp) length(tp[["track"]]) > 0)]
    return(lapply(track.path, function(tp) list(fileid=tp[["fileid"]], 
                                                fid=tp[["fid"]], 
                                                dist=FUN(tp[["path"]], tp[["track"]][[1]][["coords"]], ...))))
}

track.filenames <- list.files("data/sample_tracks", pattern="*.geojson", full.names=TRUE)
track.geom <- lapply(track.filenames, MakeTrackTuple)
track.coords <- lapply(track.geom, function(t) list(fid=t[[1]], coords=t[[2]]@lines[[1]]@Lines[[1]]@coords))
path.filenames <- list.files("data/sample_paths", pattern = "*.geojson", full.names = TRUE)
path.geom <- lapply(path.filenames, MakePathTuple)
path.geom <- path.geom[(!is.na(path.geom))]
ll0 <- lapply(path.geom, function(x) list(x[[1]], x[[2]], x[[3]]@lines))
ll1 <- lapply(ll0, function(y) list(y[[1]], y[[2]], lapply(y[[3]], function(z) z@Lines[[1]]@coords)))
path.coords <- lapply(ll1, function(p) list(fileid=p[[1]], fid=p[[2]], coords=do.call(rbind, p[[3]])))
dtw <- CalculateSimilarity(track.coords, path.coords, FUN=SimilarityMeasures::DTW)
editdist <- CalculateSimilarity(track.coords, path.coords, FUN=SimilarityMeasures::EditDist, pointDistance=0.001)
#frechet <- CalculateSimilarity(track.coords, path.coords, FUN=SimilarityMeasures::Frechet)