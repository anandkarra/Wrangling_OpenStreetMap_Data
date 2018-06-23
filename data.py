from __future__ import division
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

import config

OSM_PATH = config.osm_filename

NODES_PATH = config.csv_filenames['nodes']
NODE_TAGS_PATH = config.csv_filenames['nodes_tags']
WAYS_PATH = config.csv_filenames['ways']
WAY_NODES_PATH = config.csv_filenames['ways_nodes']
WAY_TAGS_PATH = config.csv_filenames['ways_tags']

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

position = 0

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    global position

    for e in element.iter():
        
        #For "node" tags
        if e.tag == 'node':

            percent_complete = (position/996917)*100
            print("Current tag= ",e.tag)
            print("id of tag= ",e.attrib['id'])
            print("Position= ",position)
            print("Percent complete= ","%.3f" % percent_complete)
            print("------")
            position += 1

            #For "node" field
            for i in node_attr_fields:
                node_attribs[i] = e.attrib[i]

            #For "node_tags" field
            for sube in e:
                if sube.tag == 'tag':
                    ignore_tag = problem_chars.search(sube.attrib['k'])
                    if ignore_tag:
                        break
                    else:
                        sube_tag_dict = {}
                        sube_tag_dict['id'] = e.attrib['id']
                        #print(e.attrib['id'])
                    
                        k_string = (sube.attrib['k']).split(':')
                        #print("k_string = ",k_string,k_string[0],type(k_string[0]))

                        if len(k_string)==1:
                            sube_tag_dict['key'] = [sube.attrib['k']][0]
                            sube_tag_dict['value'] = sube.attrib['v']
                            sube_tag_dict['type'] = default_tag_type
                            #print(sube.attrib['k'],sube.attrib['v'],default_tag_type)
                        else:
                            rem_k_string = ""
                            for k in k_string[1:]:
                                rem_k_string+=k
                                rem_k_string+=':'
                            rem_k_string = rem_k_string[:-1]
                            sube_tag_dict['key'] = rem_k_string
                            sube_tag_dict['value'] = sube.attrib['v']
                            sube_tag_dict['type'] = k_string[0]
                            #print(k_string[1:],sube.attrib['v'],k_string[0])

                        tags.append(sube_tag_dict)

            return {'node': node_attribs, 'node_tags': tags}

        #For "way" tags
        elif e.tag == 'way':

            percent_complete = (position-996917/101231)*100
            print("Current tag= ",e.tag)
            print("id of tag= ",e.attrib['id'])
            print("Position= ",position)
            print("Percent complete= ","%.3f" % percent_complete)
            print("------")
            position += 1

            #For "way" field
            for i in way_attr_fields:
                way_attribs[i] = e.attrib[i]

            #For "way_tags" field
            tags = []
            for sube in e:
                if sube.tag == 'tag':
                    ignore_tag = problem_chars.search(sube.attrib['k'])
                    if ignore_tag:
                        break
                    else:
                        sube_way_tags_dict = {}
                        sube_way_tags_dict['id'] = e.attrib['id']
                        #print(e.attrib['id'])
                    
                        k_string = (sube.attrib['k']).split(':')
                        #print("k_string = ",k_string,k_string[0],type(k_string[0]))

                        if len(k_string)==1:
                            sube_way_tags_dict['key'] = [sube.attrib['k']][0]
                            sube_way_tags_dict['value'] = sube.attrib['v']
                            sube_way_tags_dict['type'] = default_tag_type
                            #print(sube.attrib['k'],sube.attrib['v'],default_tag_type)
                        else:
                            rem_k_string = ""
                            for k in k_string[1:]:
                                rem_k_string+=k
                                rem_k_string+=':'
                            rem_k_string = rem_k_string[:-1]
                            sube_way_tags_dict['key'] = rem_k_string
                            sube_way_tags_dict['value'] = sube.attrib['v']
                            sube_way_tags_dict['type'] = k_string[0]
                            #print(k_string[1:],sube.attrib['v'],k_string[0])

                        tags.append(sube_way_tags_dict)
            
            #For "way_nodes" field
            position_int = 0
            for sube in e:
                if sube.tag == 'nd':
                    sube_way_nodes_dict = {}
                    
                    sube_way_nodes_dict['id'] = e.attrib['id']
                    sube_way_nodes_dict['node_id'] = sube.attrib['ref']
                    sube_way_nodes_dict['position'] = position_int
                    
                    position_int += 1

                    way_nodes.append(sube_way_nodes_dict)

            return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(OSM_PATH, validate=True)