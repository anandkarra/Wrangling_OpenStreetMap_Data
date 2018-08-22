# Wrangling and Exploring OpenStreetMap Data

Maps in addition to being of geographic importance also contain a lot of information about the people and communities living in a region. Analysing the map data allows us to uncover many of these interesting insights.

The first step was to get hands on the map data. As the Google Maps API license does not permit scraping [Google Maps Platform Terms of Service](https://cloud.google.com/maps-platform/terms/#10-license-restrictions). I had to turn to [OpenStreetMap](https://www.openstreetmap.org), which is a community-driven mapping serivce. Also, OpenStreetMap publishes OSM files of regions, states and countries which is perfect for this project.

## Map Area

**Delaware, US**

* OpenStreetMap file (compressed) (.osm.bz2) : [geofabrik.de](https://download.geofabrik.de/north-america/us/delaware.html) | **14.7 MB**
* OpenStreetMap file (uncompressed) (.osm) : `delaware-latest.osm` | **171 MB**
* Test data file (subset of the full uncompressed .osm file) : `test_data.osm` | **29.9 KB**

I was initially interested in the map data for New York City but after downloading the corresponding OSM file and performing some preliminary exploration, I quickly realized that the I was short of computation resources as execution of any kind of operation took a long time for such a large dataset (~2 GB).

Hence, I went back to the Open Street Map website and downloaded the map data for some other regions and finally settled for the state of **Delaware, US**.

> The parsing, auditing and other steps can however be used for the map data of other regions as well with minor modifications.

## Process overview
* Preliminary exploration to assess the inconsistencies in the data.
* Cleaning the data as per the requirement.
* Parsing the data into CSV files.
* Inserting the data from CSV files to an SQLite database.
* Exploration of the data using SQL queries.

> **The process of cleaning, parsing and exploration of the data is detailed in the report (Report.pdf) file.**

# Files

* **config.py** : Configuration file containing various parameters like location of .osm file, sqlite database (.db) file and CSV files.
* **mapparser.py** : Prints the number of times each of the tags appear in the map data (.osm) file
* **tags.py** : Outputs the number of times the `k` attribute falls into the lower, lower_colon, other and problemchars categories.
* **data.py** : Converts the map data from the .osm format to individual csv files based on the schema defined in schema.py.
* **schema.py** : Gives the schema of the csv files for each of the tags.
* **view_unexpected_street_types.py** : Outputs the last word of each of the street names.
* **update_street_names.py** : Updates the street names using the mappings dictionary.
* **view_street_types.py** : Outputs the last word of each street name. Can be used to check the cleaning done by the update_street_names.py file.
* **csv_to_sql.py** : Writes all of the cleaned CSV files to sqlite3 database as per the schema of the tables given in config.py. This file may need to be run in Python 3.6 due to problems with handling of UTF-8 characters in Python 2.7.

* **test_data.osm** : Subset of the full map data for testing purposes.
* **format.md** : Gives the schema for the processing of the individual tags in the map data.
* **CSV files** : CSV files obtained after cleaning for the full map data.
* **delaware.db** : sqlite3 database with all the tables for the tags.
* **Report.pdf** : Report answering the Rubric questions and documenting the wrangling process