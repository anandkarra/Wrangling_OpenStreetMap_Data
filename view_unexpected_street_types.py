import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

import config

OSMFILE = config.osm_filename

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = config.expected_street_types

print("Expected : ",expected)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def printed_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys,key=lambda s:s.lower())
    for k in keys:
        v = d[k]
        print("%s: %d" % (k,v))

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))

audit(OSMFILE)