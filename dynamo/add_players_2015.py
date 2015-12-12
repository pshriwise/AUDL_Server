
# coding: utf-8

# In[1]:

from subprocess import call
import csv
import urllib2
import json
from dynamo_conn import get_connection
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import RangeKey,HashKey
from boto.dynamodb2.types import NUMBER


# In[2]:

base_url = 'https://docs.google.com/spreadsheets/d/'
spreadsheet_key = '1Qkup3uHxKgsuLgOJQ-L9S-YoTa5zNp3mu4SPk9abvKY'
Rosters_gid = '1948201024'
Rosters_filename = '2015_Players.csv'

#get the csv of the sheet
call(["wget" , '-O' , Rosters_filename, base_url+spreadsheet_key+ '/export?format=csv&gid=' + Rosters_gid])
    
#open the csv file
players = csv.reader(open(Rosters_filename, 'rb'))

#Establish keys
keys = players.next()


# In[3]:

#Format keys properly
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


# In[4]:

#Construct data for each player
players_data = []
for player in players:
    player_data ={}
    for i,key in enumerate(new_keys):
        player_data[key] = player[i]
    if player_data['player_first_name'] is not '':
        players_data.append(player_data)


# In[5]:

#create dynamodb connection
conn = get_connection()


# In[6]:

#Check to see if our table already exists
if 'players' not in conn.list_tables()['TableNames']:
    print "Players table not in database. Creating...."
    player_table = Table.create('players', schema=[HashKey('player_id',data_type=NUMBER)],throughput={'read':25,'write':25},connection=conn)
    print "Done"
else:
    player_table = Table('players',connection=conn)


# In[8]:

#Find out what player id to start at
all_players = list(player_table.scan())
#if we have no entries, start at 0
if len(all_players) == 0 :
    start_id = 0
else:
    seq = [x['player_id'] for x in all_players]
    start_id = max(seq)

#Get the teams table for team id lookups
team_table = Table('team_metadata',connection=conn)
all_teams = list(team_table.scan())
    
    
players_added = 0
#Now add all players in our list
for player_data in players_data: 
    #Make sure we don't already have this player
    skip = False
    candidate_players = [x for x in all_players if x['player_last_name'] == player_data['player_last_name']]
    if len(candidate_players) > 0:
       for item in candidate_players:
            del item['player_id']
            if item == player_data:
                skip = True
    #add player id to player data
    player_data['player_id'] = start_id
    start_id+=1
    
    #Add player if appropriate
    if not skip:
        team_ids = [x['team_id'] for x in all_teams if x['comb_name'] == player_data['team_name']]
        assert len(team_ids) == 1 #if not true our player data is corrupt
        del player_data['team_name'] 
        player_data['team_id'] = team_ids[0]
        player_table.put_item(data=player_data)
        players_added+=1
    
        
        


# In[9]:

print players_added


# In[ ]:



