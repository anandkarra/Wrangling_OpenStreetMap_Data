import csv
import sqlite3

import config

# Import the dictionaries from the files
dict_create_commands = config.create_table_commands
dict_insert_commands = config.insert_into_table_commands
dict_filenames = config.csv_filenames

# Database in which the tables will be written to
db_filename = config.db_filename

# Connection
connection = sqlite3.connect(db_filename)
 
# Cursor 
crsr = connection.cursor()

# All tables created
for table in dict_create_commands.keys():
    create_command = dict_create_commands[table]
    crsr.execute(create_command)

# Iteratively inserting all the values from CSVs to SQLite tables
for table in dict_insert_commands.keys():
    insert_command = dict_insert_commands[table]

    with open(dict_filenames[table],'rt') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_command,csv_reader)

# Commit changes
connection.commit()

# Close connection
connection.close()
