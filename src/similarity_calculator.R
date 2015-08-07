library(SimilarityMeasures)
library(rgdal)
library(data.table)

MakeTrackTuple <- function(f) {
    fid <- unlist(strsplit(tail(unlist(
        strsplit(f, "/")
    ), n = 1), "_"))[1]
    geom <-
        readOGR(f, layer = "OGRGeoJSON", require_geomType = "wkbLineString")
    return(c(fid, geom))
}

MakePathTuple <- function(f) {
    fileid <-
        unlist(strsplit(tail(unlist(
            strsplit(f, "/")
        ), n = 1), "[.]"))[1]
    fid <-
        unlist(strsplit(tail(unlist(
            strsplit(f, "/")
        ), n = 1), "_"))[1]
    geom <-
        tryCatch(
            readOGR(f, layer = "OGRGeoJSON", require_geomType = "wkbLineString"),
            error = function(e)
                NA
        )
    if (!is.na(geom))
        return(c(fileid, fid, geom))
    else
        return(NA)
}

CalculateDTW <-
    function(fileid, fid, path, track) {
        d <- SimilarityMeasures::DTW(path, track)
        return(list(
            fileid = fileid, fid = fid, dist = d,
            ratio = d / (max(nrow(path), nrow(track)) - 2)
        ))
    }

CalculateEditDist <-
    function(fileid, fid, path, track, ...) {
        d <- SimilarityMeasures::EditDist(path, track, ...)
        return(list(
            fileid = fileid, fid = fid, dist = d,
            ratio = d / (max(nrow(path), nrow(track)) - 2)
        ))
    }

CalculateLCSS <-
    function(fileid, fid, path, track, ...) {
        d <- SimilarityMeasures::LCSSCalc(path, track, ...)
        r <- SimilarityMeasures::LCSSRatioCalc(path, track, ...)
        return(list(
            fileid = fileid, fid = fid, dist = d, ratio = r
        ))
    }

CalculateFrechet <-
    function(fileid, fid, path, track) {
        d <- SimilarityMeasures::Frechet(path, track)
        return(list(
            fileid = fileid, fid = fid, dist = d
        ))
    }

# EPSG:25832
munich.srs <-
    "+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
track.filenames <-
    list.files("data/sample_tracks", pattern = "*.geojson", full.names = TRUE)
track.geom <- lapply(track.filenames, MakeTrackTuple)
tl0 <-
    lapply(track.geom, function(x)
        list(x[[1]], x[[2]]@lines[[1]]@Lines))
tl1 <-
    lapply(tl0, function(y)
        list(y[[1]], lapply(y[[2]], function(z)
            z@coords)))
track.coords <-
    lapply(tl1, function(t)
        list(fid = t[[1]], coords = do.call(rbind, t[[2]])))
track.coords.reproj <-
    lapply(track.coords, function(t)
        list(fid = t[["fid"]],
             coords = project(t[["coords"]],
                              munich.srs)))
path.filenames <-
    list.files("data/sample_paths", pattern = "*.geojson", full.names = TRUE)
path.geom <- lapply(path.filenames, MakePathTuple)
path.geom <- path.geom[(!is.na(path.geom))]
ll0 <-
    lapply(path.geom, function(x)
        list(x[[1]], x[[2]], x[[3]]@lines))
ll1 <-
    lapply(ll0, function(y)
        list(y[[1]], y[[2]], lapply(y[[3]], function(z)
            z@Lines[[1]]@coords)))
path.coords <-
    lapply(ll1, function(p)
        list(
            fileid = p[[1]], fid = p[[2]], coords = do.call(rbind, p[[3]])
        ))
path.coords.reproj <-
    lapply(path.coords, function(p)
        list(
            fileid = p[["fileid"]],
            fid = p[["fid"]],
            coords = project(p[["coords"]],
                             munich.srs)
        ))
track.path <-
    lapply(path.coords.reproj,
           function(p)
               list(
                   fileid = p[["fileid"]],
                   fid = p[["fid"]],
                   path = p[["coords"]],
                   track = track.coords.reproj[sapply(track.coords.reproj,
                                                      function(t)
                                                          t[["fid"]] == p[["fid"]])]
               ))
track.path <-
    track.path[sapply(track.path, function(tp)
        length(tp[["track"]]) > 0)]
# DTW
print("Calculating DTW distance...")
start.time <- Sys.time()
dtw <- lapply(track.path, function(tp)
    CalculateDTW(tp[["fileid"]],
                 tp[["fid"]],
                 tp[["path"]],
                 tp[["track"]][[1]][["coords"]]))
end.time <- Sys.time()
time.taken <- end.time - start.time
print("done!")
print(time.taken)
dtw.df <- do.call(rbind, dtw)
print("Writing DTW data to CSV file...")
write.csv(dtw.df, file = "data/dtw.csv", row.names = FALSE)
print("done!")
# EditDist
print("Calculating EditDist distance...")
start.time <- Sys.time()
editdist <- lapply(track.path,
                               function(tp)
                                   CalculateEditDist(tp[["fileid"]],
                                                     tp[["fid"]],
                                                     tp[["path"]],
                                                     tp[["track"]][[1]][["coords"]],
                                                     pointDistance = 100))
end.time <- Sys.time()
time.taken <- end.time - start.time
print("done!")
print(time.taken)
editdist.df <- do.call(rbind, editdist)
print("Writing EditDist data to CSV file...")
write.csv(editdist.df, file = "data/editdist.csv", row.names = FALSE)
print("done!")
# LCSS
print("Calculating LCSS distance...")
start.time <- Sys.time()
lcss <- lapply(track.path,
                           function(tp)
                               CalculateLCSS(tp[["fileid"]],
                                             tp[["fid"]],
                                             tp[["path"]],
                                             tp[["track"]][[1]][["coords"]],
                                             pointDistance = 100))
end.time <- Sys.time()
time.taken <- end.time - start.time
print("done!")
print(time.taken)
lcss.df <- do.call(rbind, lcss)
print("Writing LCSS data to CSV file...")
write.csv(lcss.df, file = "data/lcss.csv", row.names = FALSE)
print("done!")
# Frechet
# print("Calculating Frechet distance...")
# frechet <- lapply(track.path,
#                   function(tp)
#                       CalculateFrechet(tp[["fileid"]],
#                                        tp[["fid"]],
#                                        tp[["path"]],
#                                        tp[["track"]][[1]][["coords"]]))
# print("done!")
# frechet.df <- do.call(rbind, frechet)
# print("Writing Frechet data to CSV file...")
# write.csv(frechet.df, file = "data/frechet.csv", row.names = FALSE)
# print("done!")