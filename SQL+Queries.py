
# coding: utf-8

# In[6]:

import os
import csv
import pandas as pd
import seaborn as sns
import sqlite3 as lite

os.path.getsize("blrmed.xml")


# In[4]:




# name of the sqlite database file
sqlite_file = 'OpenStreetMapProj.db'    

# Connect to the database
conn = lite.connect(sqlite_file)

df = pd.read_sql_query("select count(user) as 'Unique Users' from (select user from nodes union select user from ways);", conn)

df


# In[5]:

df1 = pd.read_sql_query("select count((id)) as 'unique nodes'from nodes;", conn)
df1


# In[6]:

df2 = pd.read_sql_query("select count((id)) as 'unique ways'from ways;", conn)
df2


# In[54]:

df3 = pd.read_sql_query("select value as  'Amenity', count(*) as  'Number of Occurences' from  (select value, key from nodes_tags union all select value, key from ways_tags) where key = 'amenity' group by value order by count(*) desc limit 20;", conn)




x0 = df3.style.set_properties(**{'background-color': 'black',
                           'color': 'orange',
                           'border-color': 'black'})

x0


# In[12]:

df4 = pd.read_sql_query("select user, count(user) as 'Number of Contributions' from (select user from nodes union all select user from ways) group by user order by count(*) desc limit 10;", conn)

df4



# In[44]:

#Top 10 Amenities
df5 = pd.read_sql_query("select value, count(value) as 'Number' from (select key,value from nodes_tags union all select key, value from ways_tags) where key = 'amenity' group by value order by count(*) desc limit 10;", conn)

cm = sns.light_palette("yellow", as_cmap=True)

x1 = df5.style.background_gradient(cmap=cm)
x1


# In[43]:

df6 = pd.read_sql_query("select value as 'Religion', count(value) as 'Number of Practioners' from (select key,value from nodes_tags union all select key, value from ways_tags)  where key = 'religion' group by value order by count(*) desc limit 10;", conn)


cm = sns.light_palette("green", as_cmap=True)

x2 = df6.style.background_gradient(cmap=cm)
x2


# In[7]:

dfa = pd.read_sql_query("select value as 'Cuisine', count(value) as 'Number of Joints' from (select key,value from nodes_tags union all select key, value from ways_tags)  where key = 'cuisine' group by value order by count(*) desc limit 10;", conn)


cm = sns.light_palette("lightblue", as_cmap=True)

x3 = dfa.style.background_gradient(cmap=cm)
x3


# In[75]:

df9 = pd.read_sql_query("select  nodes_tags.value as 'Restaurant', count(nodes_tags.value) as 'Number of Branches' from (select id, value  from (select * from nodes_tags union all select *from ways_tags) where value = 'restaurant') rst, nodes_tags where rst.id = nodes_tags.id and nodes_tags.key = 'name' group by nodes_tags.value order by count(nodes_tags.value) desc limit 10;", conn)

x1 = df9.style.set_properties(**{'background-color': 'lightpink',
                           'color': 'black',
                           'border-color': 'white'})

x1


# In[9]:

df10 = pd.read_sql_query("SELECT value FROM nodes_tags WHERE key='street';", conn)

df10


# In[ ]:



