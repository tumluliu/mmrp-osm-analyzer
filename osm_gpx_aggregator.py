import feedparser

if __name__ == "__main__":
    osm_gpx_rss_url = "http://www.openstreetmap.org/traces/rss"
    feed = feedparser.parse(osm_gpx_rss_url)
    print feed
