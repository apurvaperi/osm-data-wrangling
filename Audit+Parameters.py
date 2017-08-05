
# coding: utf-8

# In[1]:

### AUDIT AND CLEAN STREET NAMES ###

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

from pprint import pprint



# Expected street types in Bengaluru
EXPECTED = ['Road', 'Nagar', 'Street', 'Cross', 'Main', 'Avenue', 'Block','Veedhi']

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

global mapping 
mapping = {}
result=[]


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
            
# Function to return a list of all street names            
def audit_street_name(filename):
    for element in get_element(filename, tags=('node', 'way')):
        for elem in element.iter('tag'):     
            if elem.attrib["k"] == "addr:street":
                street_name = elem.get('v')
                # Avoid counting pincodes and city/state names (if any) in the mapping
                x = unicode(street_name.rsplit(None,1)[-1])
                if x.isnumeric() or x in ["bangalore", "karnataka", "bengaluru", "Karnataka", "Bangalore", "Bengaluru"]:
                    street_name = street_name.rsplit(None,1)[0]
                m = street_type_re.search(street_name)
                if m:
                    street_type = m.group()
                    result.append(street_type)
    return result

#Function to create a mapping against expected street anmes using difflib's sequence matcher 
def street_mapping(street_types, EXPECTED):
    count = 0
    for b in street_types:
        for a in EXPECTED:
            seq = difflib.SequenceMatcher(None,a,b)
            if seq.ratio() >= 0.6:
                mapping[b] = a
                count += 1
    return count, mapping

# Function to update the street name based on the mapping dictionary
def update_street_name(street_type, MAPPING):
#take a text and replace words that match a key in a dictionary with the associated value, return the changed text
    rc = re.compile('|'.join(map(re.escape, MAPPING)))
    def translate(match):
        return MAPPING[match.group(0)]
    return rc.sub(translate, street_type)

    
audit_list =  audit_street_name("blrmed.xml")

print set(audit_list)


count, MAPPING = street_mapping (audit_list, EXPECTED)

print "Number of changes to be made  = ", count

pprint (MAPPING)




# In[54]:

### AUDIT AND CLEAN PHONE NUMBERS ###
raw_phone_numbers = []


## Function to audit phone numbers and create a list of all the numbers

def audit_phone_number(filename):
    for element in get_element(filename, tags=('node', 'way')):
        for elem in element.iter('tag'):     
            if elem.attrib["k"] == "phone":
                raw_phone_numbers.append(elem.get('v'))
    return raw_phone_numbers
    

## Function to update the phone numbers using  python's phone number library
def update_phone_number(value):
    global val
    val = None
    
    test = value.split(";")[0]
    # remove unwanted characters and spaces
    test =''.join(x for x in test if x.isdigit())
    # Add the City code of 80
    if len(test) == 8:
        test = '80'.join(test)
    #  For valid 10 digit phone numbers, parse and update the format using the phonenumbers library    
    if len(test) == 10:
        y = phonenumbers.parse(test, "IN")
        val = phonenumbers.format_number(y, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    else:
        val = "Unknown"
    return val


number = audit_phone_number("blrmed.xml")

print (number)


# In[14]:

### AUDIT BUILDING TYPES AND NAMES ###

building_names= []

## Function to audit building names and create a list of all the names

def audit_building(filename):
    for element in get_element(filename, tags=('node', 'way')):
        for elem in element.iter('tag'):     
            if elem.attrib["k"] == "building":
                building_names.append(elem.get('v'))
    return building_names

## Function to clean and update the building names 
def update_building(value):
    val = re.sub("yes", "Unknown", value)
    val = re.sub("_", " ", val)
    return val

building = audit_building("blrmed.xml")

print set(building)



# In[13]:

city_name = []

## Function to obtain a list of all city names in order to audit it
def audit_city_name(filename):
    for element in get_element(filename, tags=('node', 'way')):
        for elem in element.iter('tag'):     
            if elem.attrib["k"] == "addr:city":
                city_name.append(elem.get('v'))
    return city_name

## Function to clean and update the city name 

def update_city(value):
    val = value.replace(value, "Bengaluru")
    return val
    

city = audit_city_name("blrmed.xml")

print set(city)


# In[ ]:



