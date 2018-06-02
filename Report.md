# Wrangling and Exploring OpenStreetMap Data

## Map Area

**Delaware, US**

* OpenStreetMap file (compressed) (.osm.bz2) : [geofabrik.de](https://download.geofabrik.de/north-america/us/delaware.html) | **14.7 MB**
* OpenStreetMap file (uncompressed) (.osm) : `delaware-latest.osm` | **171 MB**
* Test data file (subset of the full uncompressed .osm file) : `test_data.osm` | **29.9 KB**

I was initially interested in the map data for New York City but after downloading the corresponding OSM file and performing some preliminary exploration quickly realized that the I was short of computation resources as execution of any kind of function took a long time for such a large dataset.

Consequently, I went back to the Open Street Map website and downloaded the map data for some other regions and finally settled for the state of **Delaware**. The parsing, auditing and other steps can however be used for the map data of other regions with minor modifications.