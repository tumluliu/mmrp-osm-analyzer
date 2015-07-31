library(SimilarityMeasures)
library(rgdal)

mp <- read.csv("data/multimodal_routing_results.csv")
i <- sapply(mp, is.factor)
mp[i] <- lapply(mp[i], as.character)
geojson_file <- "data/sample_response.json"
rawlines <- readOGR(geojson_file, 'OGRGeoJSON', require_geomType = 'wkbLineString')
coords <- rawlines@lines[[1]]@Lines[[1]]@coords
# Let's see what is the distance between two identical lines
frechet <- Frechet(coords, coords)
editdist <- EditDist(coords, coords, pointDistance = 0.001)
dtw <- DTW(coords, coords)
#lcss <- LCSS(coords, coords, pointSpacing = -1, pointDistance = 0.001, errorMarg = 0.5, TRUE)