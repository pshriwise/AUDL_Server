
# coding: utf-8

# In[1]:

import urllib2
import json
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import RangeKey,HashKey
from dynamo_conn import get_connection
import csv


# In[2]:

#Establish dynamo db connection
conn = get_connection()


# In[3]:

#Check for a table called raw_game_data
if 'raw_game_data' not in conn.list_tables()['TableNames']:
    print "Table not in database. Creating..."
    rgd_table = Table.create('raw_game_data', schema=[HashKey('game_id')],throughput={'read':25,'write':25},connection=conn)
    print "Done"
else:
    rgd_table = Table('raw_game_data',connection=conn)


# In[4]:

#Get a list of UA team ids from local .csv
reader = csv.reader(open('2014_Team_Info.csv','rb'))
keys = reader.next()
team_ids = []
for line in reader: 
    if line[4] is not '':
        team_ids.append(line[4])
print team_ids


# In[5]:

#For each game in the list of ids, get the game hashes
id_hash_list = []
for team in team_ids:
    #Get a list of game hashes for a given team id
    team_id = team
    req = urllib2.Request('http://www.ultianalytics.com/rest/view/team/' + str(team_id) + '/games/')
    response = urllib2.urlopen(req,timeout=10)
    team_games = json.loads(response.read())
    #Now package up the game ids and game hashes
    all_game_hashes = []
    for game in team_games:
        all_game_hashes.append(game['gameId'])
    #when we're done, associate the hashes with the UA id
    id_hash_list.append((team_id,all_game_hashes))


# In[6]:

i=0
for entry in id_hash_list:
    i+=len(entry[1])
print i


# In[7]:

#For every game, add an item to the table
i=0
for entry in id_hash_list:
    team = entry[0]
    for game_hash in entry[1]:
        #Setup a request for a game's data
        req = urllib2.Request('http://www.ultianalytics.com/rest/view/team/' + str(team) + '/game/' + game_hash)
        response = urllib2.urlopen(req,timeout=10)
        raw_game_data = json.loads(response.read())
        rgd_table.put_item(data={'game_id': raw_game_data['gameId'], 'data':str(raw_game_data)})
        i+=1
print "Added " + str(i) + " games."


# In[8]:

print len(list(rgd_table.scan()))

