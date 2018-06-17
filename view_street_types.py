import csv

import config

with open('ways_tags.csv','r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    next(csv_reader)

    street_types = {}
    street_types_list = []

    for row in csv_reader:
        if row['key'] == 'street' and row['type'] == 'addr':
            street_name_split = row['value'].split()
            if street_name_split[-1] not in street_types_list:
                street_types_list.append(street_name_split[-1])
    
    print(street_types_list)
