import csv
import os

import config

mapping = { "St": "Street",
            "St.": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "road": "Road",
            "Hwy": "Highway",
            "Blvd.": "Boulevard",
            "Ctr": "Center",
            "Ln": "Lane",
            "Trl": "Trail",
            "Pkwy": "Parkway"
            }

def update_name(name, mapping):
    split_name = name.split();

    for i in range(len(split_name)):
        if split_name[i] in mapping.keys():
            split_name[i] = mapping[split_name[i]]

    name = ""
    for sub_name in split_name:
        name += sub_name
        name += " "

    name = name[:-1]

    return name

file_reading = open('ways_tags.csv','rb')
file_writing = open('temp.csv','wb')

reader = csv.DictReader(file_reading)
writer = csv.writer(file_writing)

writer.writerow(['id','key','value','type'])

for row in reader:
    if row['key'] == 'street' and row['type'] == 'addr':
        if row['value'] != update_name(row['value'],mapping):
            writer.writerow([row['id'],
                            row['key'],
                            update_name(row['value'],mapping),
                            row['type']])
        else:
            writer.writerow([row['id'],
                            row['key'],
                            row['value'],
                            row['type']])
    else:
        writer.writerow([row['id'],
                        row['key'],
                        row['value'],
                        row['type']])

file_reading.close()
file_writing.close()

os.rename('temp.csv','ways_tags.csv')