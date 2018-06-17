import xml.etree.cElementTree as ET
import pprint

import config

OSM_PATH = config.osm_filename

def count_tags(filename):
        
        tag_dict={}
        tree = ET.parse(filename)
        root = tree.getroot()
        
        #print(type(root))
        
        tag_list=[]
        for child in root:
            tag_list.append(child.tag)
            for baby in child:
                tag_list.append(baby.tag)
        #print(tag_list)
        
        count=0
        tag_set=set(tag_list)
        for utag in tag_set:
            for tag in tag_list:
                if(tag==utag):
                    count+=1
            tag_dict[utag]=count
            count=0
                
        tag_dict['osm']=1
            
        #print(tag_dict)
        return tag_dict

tag_dict = count_tags(OSM_PATH)

pprint.pprint(tag_dict)