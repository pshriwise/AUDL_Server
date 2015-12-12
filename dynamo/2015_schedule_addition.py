
# coding: utf-8

# In[1]:

import csv
from dynamo_conn import get_connection
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import RangeKey,HashKey
import urllib2
import json


# In[2]:

#open 2015 schedule file
reader = csv.reader(open("../2015_Schedule.csv",'rb'))


# In[3]:

#trim out a few of the keys we don't want
keys = reader.next()
print keys
keys = keys[:7]
print keys


# In[4]:

#correct key formatting
new_keys=[]
for key in keys: 
    key = key.lower().strip().replace(' ','_')
    #exceptions
    if key == 'week_#':
        key ='week'
    if key[-4:] == 'team':
        key+='_id'
    new_keys.append(key)

keys = new_keys
print keys


# In[5]:

#create dicts for each row in the schedule file w/ the appropriate keys
game_dicts=[]
for game in reader:
    #setup a dictionary of items
    game_dict = {}
    for i,key in enumerate(keys):
        game_dict[key] = game[i].strip()
    if game_dict['date'] is not '': 
        game_dicts.append(game_dict)
        
        


# In[6]:

#Sanity check on the number of games (should be 182)
print len(game_dicts)


# In[7]:

#open AWS connection to dynamodb server and get the required table objects
conn = get_connection()

schedule_table = Table('schedule',connection=conn)
meta_table = Table('team_metadata',connection=conn)


# In[8]:

#now replace the team names with the ids in our database and add to database

i=0 #SHOUDL ONLY BE ZERO BECAUSE THIS IS THE FIRST TIME WE'RE ADDING GAMES
for game in game_dicts[:]:
    # find the names of the home team and the away team in the metadata
    home_team = list(meta_table.scan(comb_name__eq=game['home_team_id']))
    away_team = list(meta_table.scan(comb_name__eq=game['away_team_id']))
    if len(home_team) != 1 or len(away_team) != 1:
        bad_list.append("Not good")
        print game['home_team_id'],game['away_team_id']
    else:
        #replace keys here
        game['home_team_id'] = home_team[0]['team_id']
        game['away_team_id'] = away_team[0]['team_id']
        #add the primary index value
        game['game_id'] = i
        #put item in database
        schedule_table.put_item(data=game,overwrite=True)
        i+=1
#report number of items added
print "Number of games added: " + str(i)


# In[ ]:



