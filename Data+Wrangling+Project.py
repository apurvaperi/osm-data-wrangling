
# coding: utf-8

# In[2]:

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import difflib
from collections import defaultdict 
import phonenumbers
import pandas as pd



# Expected street types in Bengaluru
EXPECTED = ['Road', 'Nagar', 'Street', 'Cross', 'Main', 'Avenue', 'Block','Veedhi']
MAPPING = {'block': 'Block', 'Cross': 'Cross', 'Rd': 'Road', 'street': 'Street', 'Crossroad': 'Cross', 'Road)': 'Road', 'Main': 'Main', u'Road,': 'Road', 'Nagar,': 'Nagar', 'cross': 'Cross', 'Cross,': 'Cross', 'Street,': 'Street', 'Road': 'Road', 'road,': 'Road', 'Veedhi': 'Veedhi', 'Block': 'Block', 'Nagar,,': 'Nagar', 'Nagar': 'Nagar', 'Street': 'Street', 'ROad': 'Road', 'Naga': 'Nagar', 'Block,': 'Block', 'Avenue': 'Avenue', 'road': 'Road'}


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


def update_street_name(street_type, MAPPING):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, MAPPING)))
    def translate(match):
        return MAPPING[match.group(0)]
    return rc.sub(translate, street_type)
    


# In[7]:

## Function to update the phone numbers using  python's phone number library
def update_phone_number(value):
    global val
    val = None
    
    test = value.split(";")[0]
    # remove unwanted characters and spaces
    test =''.join(x for x in test if x.isdigit())
    # Add the City code of 80
    if len(test) == 8:
        test = '80' + (test)
    #  For valid 10 digit phone numbers, parse and update the format using the phonenumbers library    
    if len(test) == 10:
        y = phonenumbers.parse(test, "IN")
        val = phonenumbers.format_number(y, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    else:
        val = "Unknown"
    return val


# In[8]:

## Function to clean and update the building names 
def update_building(value):
    val = re.sub("yes", "Unknown", value)
    val = re.sub("_", " ", val)
    return val


# In[9]:

## Function to clean and update the city name 

def update_city(value):
    val = value.replace(value, "Bengaluru")
    return val


# In[10]:

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import difflib
from collections import defaultdict 
import phonenumbers
import pandas as pd

mapping ={}
mapping = { } 
expected = []
unexpected= []
result = []

tags=[]
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_types = defaultdict(set)


#import cerberus

#import schema

OSM_PATH = "example.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
building_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
PINCODE = re.compile(r'^\d{6}$')


#SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def tag_key(k):
    if PROBLEMCHARS.search(k):
        return
    if LOWER_COLON.search(k):
        t = k.split(":",1)[0]
        key = k.split(":",1)[1]
    else:
        t = 'regular'
        key = k
    return t,key

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

   
    ## Parse tags --> common for nodes and ways
    for elem in element.iter('tag'):
        k = elem.get('k')
        t,key = tag_key(k)
        
        if elem.attrib["k"] == "addr:street":
            value = update_street_name(elem.get('v'), MAPPING)
            #value = re.sub(street_type_re, ap, elem.attrib['v'])
        elif elem.attrib["k"] == "phone":
            value = update_phone_number(elem.get('v'))
        elif elem.attrib["k"] == "phone_1":
            value = update_phone_number(elem.get('v'))
        elif elem.attrib["k"] == "phone_2":
            value = update_phone_number(elem.get('v'))
        elif elem.attrib["k"] == "building":
            value =  update_building(elem.get('v'))
        elif elem.attrib["k"] == "addr:city":
            value = update_city(elem.get('v'))
        else:
            value = elem.get('v')
        
                      
        z = {'id': element.get("id"), 'key':key , 'value': value, 'type': t }
            
        tags.append(z)
        
    ## Parse way_nodes and way_tags for ways
    if element.tag == 'way':
        x = 0
        for name, val in  element.items():
            if name in WAY_FIELDS:
                way_attribs[name]= val
                
        for elem in element.iter('nd'):
            y = {'node_id': elem.get('ref'), 'id': element.get("id"), 'position': x}
            way_nodes.append(y)
            x+=1
    if element.tag == 'node':
        x = 0
        for name, val in  element.items():
            if name in NODE_FIELDS:
                node_attribs[name]= val
    
            
            
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
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

    with codecs.open(NODES_PATH, 'w') as nodes_file,             codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,             codecs.open(WAYS_PATH, 'w') as ways_file,             codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,             codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

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

        #validator = cerberus.Validator()

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
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map("blrmed.xml", validate=False)


# # References
# 
# https://www.python.org/dev/peps/pep-0249/
# 
# http://www.mapzen.com/data/metro-extracts/
# 
# https://pypi.python.org/pypi/phonenumbers
# 
# https://github.com/daviddrysdale/python-phonenumbers
# 
# https://docs.python.org/2/library/difflib.html
# 
# https://www.tutorialspoint.com/python/python_database_access.htm
# 
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
# 
# https://simply-python.com/2015/01/16/rapid-input-data-from-list-of-files-to-sqlite-db/
# 

# In[ ]:



