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