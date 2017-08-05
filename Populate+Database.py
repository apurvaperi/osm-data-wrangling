
# coding: utf-8

# In[1]:

import os
import csv
import pandas as pd
import sqlite3 as lite


# name of the sqlite database file
sqlite_file = 'OpenStreetMapProj.db'    

# Connect to the database
con = lite.connect(sqlite_file)

# Get a cursor object
cur = con.cursor()

cur.execute('''
    CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
)
''')

cur.execute('''CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
)
    
''')

cur.execute('''CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
)
    
''')

cur.execute('''CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
)
    
''')

cur.execute('''CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
)
    
''')

con.commit()


# In[2]:


# Read csv files into pandas
nodes = pd.read_csv('nodes.csv',encoding = 'utf8')

nodes_tags = pd.read_csv('nodes_tags.csv',encoding = 'utf8')

ways = pd.read_csv('ways.csv',encoding = 'utf8')

ways_nodes = pd.read_csv('ways_nodes.csv',encoding = 'utf8')

ways_tags = pd.read_csv('ways_tags.csv',encoding = 'utf8')


## Convert to dataframe and write to sql database.
pd.DataFrame(nodes).to_sql('nodes', con, flavor='sqlite',
                if_exists='append', index=False)

pd.DataFrame(nodes_tags).to_sql('nodes_tags', con, flavor='sqlite',
                if_exists='append', index=False)

pd.DataFrame(ways).to_sql('ways', con, flavor='sqlite',
                schema=None, if_exists='append', index=False)

pd.DataFrame(ways_nodes).to_sql('ways_nodes', con, flavor='sqlite',
                 if_exists='append', index=False)

pd.DataFrame(ways_tags).to_sql('ways_tags', con, flavor='sqlite',
                 if_exists='append', index=False)
 
## Close the SQL connection
con.close()


# In[ ]:



