
# coding: utf-8

# In[1]:

import csv
from dynamo_conn import get_connection
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item


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

#create dicts for each row in the schedule file w/ the appropriate keys
game_dicts=[]
for game in reader:
    #setup a dictionary of items
    game_dict = {}
    for i,key in enumerate(keys):
        game_dict[key] = game[i].strip()
    if game_dict['Date'] is not '': 
        game_dicts.append(game_dict)
        
        


# In[5]:

#Sanity check on the number of games (should be 182)
print len(game_dicts)


# In[6]:

#open AWS connection to dynamodb server and get the required table objects
conn = get_connection()
games_table = Table('games',connection=conn)
meta_table = Table('team_metadata',connection=conn)


# In[7]:

#now replace the team names with the ids in our database and add to database

i=0 #SHOUDL ONLY BE ZERO BECAUSE THIS IS THE FIRST TIME WE'RE ADDING GAMES
for game in game_dicts[:]:
    # find the names of the home team and the away team in the metadata
    home_team = list(meta_table.scan(comb_name__eq=game['Home Team']))
    away_team = list(meta_table.scan(comb_name__eq=game['Away Team']))
    if len(home_team) == 0 or len(away_team) == 0:
        bad_list.append("Not good")
        print game['Home Team'],game['Away Team']
    #should find exactly one value for each team
    if len(home_team) == 1 and len(away_team) == 1:
        #replace keys here
        game['Home Team'] = home_team[0]['team_id']
        game['Away Team'] = away_team[0]['team_id']
        #add the primary index value
        game['game_id'] = i
        #put item in database
        games_table.put_item(data=game,overwrite=True)
        i+=1
#report number of items added
print "Number of games added: " + str(i)


# In[ ]:



