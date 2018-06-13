osm_filename = 'delaware-latest.osm'

db_filename = 'delaware.db'

create_table_commands = {
    'nodes' : 'CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,version INTEGER,changeset INTEGER,timestamp TEXT);',
    'nodes_tags':'CREATE TABLE nodes_tags (id INTEGER,key TEXT,value TEXT,type TEXT,FOREIGN KEY (id) REFERENCES nodes(id));',
    'ways':'CREATE TABLE ways (id INTEGER PRIMARY KEY NOT NULL,version TEXT,changeset INTEGER,timestamp TEXT);',
    'ways_tags':'CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id));',
    'ways_nodes':'CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id));',
}

insert_into_table_commands = {
    'nodes' : 'INSERT INTO nodes (id,lat,lon,version,changeset,timestamp) VALUES (:id,:lat,:lon,:version,:changeset,:timestamp);',
    'nodes_tags' : 'INSERT INTO nodes_tags (id,key,value,type) VALUES (:id,:key,:value,:type);',
    'ways' : 'INSERT INTO ways (id,version,changeset,timestamp) VALUES (:id,:version,:changeset,:timestamp);',
    'ways_tags' : 'INSERT INTO ways_tags (id,key,value,type) VALUES (:id,:key,:value,:type);',
    'ways_nodes' : 'INSERT INTO ways_nodes (id,node_id,position) VALUES (:id,:node_id,:position);'
}

csv_filenames = {
    'nodes' : 'nodes.csv',
    'nodes_tags' : 'nodes_tags.csv',
    'ways' : 'ways.csv',
    'ways_nodes' : 'ways_nodes.csv',
    'ways_tags' : 'ways_tags.csv'
}

expected_street_types = ["Street",
        "Avenue",
        "Boulevard",
        "Drive",
        "Court",
        "Place",
        "Square",
        "Lane",
        "Road",
        "Trail",
        "Parkway",
        "Commons",
        "Academy",
        "Alley",
        "Center",
        "Circle",
        "Corner",
        "Crossing",
        "Extended",
        "Extension",
        "Highway",
        "Pike",
        "Plaza",
        "Run",
        "Terrace",
        "Turnpike",
        "Way"]