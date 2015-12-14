
# coding: utf-8

# In[1]:

base_url = "http://www.ultianalytics.com/rest/view/"
import sys
sys.path.insert(0,'..')
import urllib2
import json
from ast import literal_eval
from datetime import datetime
from dynamo_conn import get_connection
from boto.dynamodb2.table import Table


# In[2]:

def update_game(ua_team_id,game_hash):
    """Updates the raw game data for a team. If the game doesn't exist in our database it will be created."""

    timestamp_format = '%Y-%m-%d %H:%M'
    conn = get_connection()
    game_table = Table('raw_game_data', connection = conn)
    query = list(game_table.query(game_id__eq = game_hash))

    if len(query) != 1: 
        print "Multiple games found for " + game_hash + " for team " + str(ua_team_id) + ". Aborting update for this game."
        #return

    db_game_data = literal_eval(query[0]['data'])
    db_timestamp = datetime.strptime(db_game_data['timestamp'],timestamp_format)


    req = urllib2.Request('http://www.ultianalytics.com/rest/view/team/' + str(ua_team_id) + '/game/' + game_hash)
    response = urllib2.urlopen(req,timeout=10)
    game_data = json.loads(response.read())
    game_data_timestamp = datetime.strptime(game_data['timestamp'],timestamp_format)    


    if (game_data_timestamp - db_timestamp).total_seconds() > 0:
        print "Updating game."
        game_table.put_item(data = {'game_id':game_hash, 'data':str(game_data)},overwrite = True)
    else:
        print "Retrieved game data is older than existing data. Doing nothing."


# In[3]:

update_game(5674069752020992,'game-53abaaef-07d2-4e51-a9de-ae1791b2ef0e')


# In[ ]:



