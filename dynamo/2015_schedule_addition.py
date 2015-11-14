
# In[1]:

import csv
import dynamo_conn
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import HashKey,RangeKey
from boto.dynamodb2.types import NUMBER


# In[2]:

#create connection to dynamodb
conn = dynamo_conn.get_connection()
conn.delete_table('games')


# Out[2]:

#     {u'TableDescription': {u'ItemCount': 0,
#       u'ProvisionedThroughput': {u'NumberOfDecreasesToday': 0,
#        u'ReadCapacityUnits': 10,
#        u'WriteCapacityUnits': 10},
#       u'TableArn': u'arn:aws:dynamodb:us-east-1:354836621061:table/games',
#       u'TableName': u'games',
#       u'TableSizeBytes': 0,
#       u'TableStatus': u'DELETING'}}

# In[4]:

games = Table.create('games',schema=[HashKey('Game_id',data_type=NUMBER),RangeKey('Date')],throughput={'read':10,'write':10},connection=conn)


# In[5]:

#open 2015 schedule file
reader = csv.reader(open("2015_Schedule.csv",'rb'))


# In[6]:

#trim out a few of the keys we don't want
keys = reader.next()
print keys
keys = keys[:7]
print keys


# Out[6]:

#     ['Date', 'Time', 'AM/PM', 'TimeZone', 'Week #', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Division', '', '']
#     ['Date', 'Time', 'AM/PM', 'TimeZone', 'Week #', 'Home Team', 'Away Team']
# 

# In[7]:

key_translation = [('Date','Date'),('Time','time'),('AM/PM','am/pm'),('TimeZone','timezone'),('Week #','week')]
key_translation +=[('Home Team','home_team_id'),('Away Team','away_team_id')]
assert(len(key_translation) == len(keys))


# In[8]:

#create dicts for each row in the schedule file w/ the appropriate keys
game_dicts=[]
for game in reader:
    #setup a dictionary of items
    game_dict = {}
    for i,key_pair in enumerate(key_translation):
        game_dict[key_pair[1]] = game[i].strip()
    if game_dict['Date'] is not '': 
        game_dicts.append(game_dict)
        
        


# In[9]:

#Sanity check on the number of games (should be 182)
print len(game_dicts)


# Out[9]:

#     182
# 

# In[10]:

#open AWS connection to dynamodb server and get the required table objects
games_table = Table('games',connection=conn)
meta_table = Table('team_metadata',connection=conn)


# In[11]:

#now replace the team names with the ids in our database and add to database

i=0 #SHOULD ONLY BE ZERO BECAUSE THIS IS THE FIRST TIME WE'RE ADDING GAMES
for game in game_dicts[:]:
    # find the names of the home team and the away team in the metadata
    home_team = list(meta_table.scan(comb_name__eq=game['home_team_id']))
    away_team = list(meta_table.scan(comb_name__eq=game['home_team_id']))
    if len(home_team) == 0 or len(away_team) == 0:
        bad_list.append("Not good")
        print game['home_team_id'],game['away_team_id']
    #should find exactly one value for each team
    if len(home_team) == 1 and len(away_team) == 1:
        #replace keys here
        game['home_team_id'] = home_team[0]['team_id']
        game['away_team_id'] = away_team[0]['team_id']
        #add the primary index value
        game['Game_id'] = i
        #put item in database
        print game
        games_table.put_item(data=game,overwrite=True)
        i+=1
#report number of items added
print "Number of games added: " + str(i)


# Out[11]:

#     {'week': '1', 'home_team_id': Decimal('2'), 'Game_id': 0, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '4/11/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('8'), 'Game_id': 1, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '12:00', 'Date': '4/12/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('9'), 'Game_id': 2, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '1:00', 'Date': '4/12/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('1'), 'Game_id': 3, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '7:30', 'Date': '4/11/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('4'), 'Game_id': 4, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '7:30', 'Date': '4/11/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('24'), 'Game_id': 5, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '7:00', 'Date': '4/11/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('18'), 'Game_id': 6, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '1:00', 'Date': '4/12/2015', 'timezone': 'EST'}
#     {'week': '1', 'home_team_id': Decimal('20'), 'Game_id': 7, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '7:30', 'Date': '4/11/2015', 'timezone': 'PST'}
#     {'week': '1', 'home_team_id': Decimal('12'), 'Game_id': 8, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '6:00', 'Date': '4/11/2015', 'timezone': 'PST'}
#     {'week': '1', 'home_team_id': Decimal('26'), 'Game_id': 9, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '1:00', 'Date': '4/12/2015', 'timezone': 'PST'}
#     {'week': '1', 'home_team_id': Decimal('13'), 'Game_id': 10, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '1:00', 'Date': '4/12/2015', 'timezone': 'PST'}
#     {'week': '2', 'home_team_id': Decimal('2'), 'Game_id': 11, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '4/18/2015', 'timezone': 'EST'}
#     {'week': '2', 'home_team_id': Decimal('9'), 'Game_id': 12, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '1:00', 'Date': '4/19/2015', 'timezone': 'EST'}
#     {'week': '2', 'home_team_id': Decimal('4'), 'Game_id': 13, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '7:30', 'Date': '4/18/2015', 'timezone': 'EST'}
#     {'week': '2', 'home_team_id': Decimal('1'), 'Game_id': 14, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '5:00', 'Date': '4/19/2015', 'timezone': 'EST'}
#     {'week': '2', 'home_team_id': Decimal('21'), 'Game_id': 15, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '6:00', 'Date': '4/18/2015', 'timezone': 'CST'}
#     {'week': '2', 'home_team_id': Decimal('24'), 'Game_id': 16, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '3:00', 'Date': '4/18/2015', 'timezone': 'EST'}
#     {'week': '2', 'home_team_id': Decimal('18'), 'Game_id': 17, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '1:00', 'Date': '4/19/2015', 'timezone': 'EST'}
#     {'week': '2', 'home_team_id': Decimal('26'), 'Game_id': 18, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '7:00', 'Date': '4/18/2015', 'timezone': 'PST'}
#     {'week': '2', 'home_team_id': Decimal('13'), 'Game_id': 19, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '7:00', 'Date': '4/18/2015', 'timezone': 'PST'}
#     {'week': '2', 'home_team_id': Decimal('25'), 'Game_id': 20, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '7:30', 'Date': '4/18/2015', 'timezone': 'PST'}
#     {'week': '3', 'home_team_id': Decimal('8'), 'Game_id': 21, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '5:00', 'Date': '4/25/2015', 'timezone': 'EST'}
#     {'week': '3', 'home_team_id': Decimal('22'), 'Game_id': 22, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '5:00', 'Date': '4/25/2015', 'timezone': 'EST'}
#     {'week': '3', 'home_team_id': Decimal('7'), 'Game_id': 23, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '4:00', 'Date': '4/26/2015', 'timezone': 'EST'}
#     {'week': '3', 'home_team_id': Decimal('4'), 'Game_id': 24, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '7:30', 'Date': '4/24/2015', 'timezone': 'EST'}
#     {'week': '3', 'home_team_id': Decimal('0'), 'Game_id': 25, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '3:00', 'Date': '4/25/2015', 'timezone': 'CST'}
#     {'week': '3', 'home_team_id': Decimal('5'), 'Game_id': 26, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '7:00', 'Date': '4/25/2015', 'timezone': 'CST'}
#     {'week': '3', 'home_team_id': Decimal('23'), 'Game_id': 27, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '7:00', 'Date': '4/25/2015', 'timezone': 'EST'}
#     {'week': '3', 'home_team_id': Decimal('21'), 'Game_id': 28, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '6:00', 'Date': '4/25/2015', 'timezone': 'CST'}
#     {'week': '3', 'home_team_id': Decimal('17'), 'Game_id': 29, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '5:30', 'Date': '4/26/2015', 'timezone': 'EST'}
#     {'week': '3', 'home_team_id': Decimal('12'), 'Game_id': 30, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '6:00', 'Date': '4/25/2015', 'timezone': 'PST'}
#     {'week': '3', 'home_team_id': Decimal('16'), 'Game_id': 31, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '6:00', 'Date': '4/25/2015', 'timezone': 'PST'}
#     {'week': '3', 'home_team_id': Decimal('13'), 'Game_id': 32, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '1:00', 'Date': '4/26/2015', 'timezone': 'PST'}
#     {'week': '4', 'home_team_id': Decimal('9'), 'Game_id': 33, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '6:30', 'Date': '5/2/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('10'), 'Game_id': 34, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '6:30', 'Date': '5/2/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('2'), 'Game_id': 35, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '4:30', 'Date': '5/3/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('8'), 'Game_id': 36, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '12:00', 'Date': '5/3/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('4'), 'Game_id': 37, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '7:30', 'Date': '5/1/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('1'), 'Game_id': 38, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '7:30', 'Date': '5/2/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('3'), 'Game_id': 39, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '7:00', 'Date': '5/2/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('5'), 'Game_id': 40, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '6:00', 'Date': '5/2/2015', 'timezone': 'CST'}
#     {'week': '4', 'home_team_id': Decimal('6'), 'Game_id': 41, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '2:00', 'Date': '5/3/2015', 'timezone': 'CST'}
#     {'week': '4', 'home_team_id': Decimal('19'), 'Game_id': 42, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '5/2/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('24'), 'Game_id': 43, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '7:00', 'Date': '5/2/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('17'), 'Game_id': 44, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '3:00', 'Date': '5/3/2015', 'timezone': 'EST'}
#     {'week': '4', 'home_team_id': Decimal('26'), 'Game_id': 45, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '7:00', 'Date': '5/2/2015', 'timezone': 'PST'}
#     {'week': '4', 'home_team_id': Decimal('20'), 'Game_id': 46, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '1:30', 'Date': '5/3/2015', 'timezone': 'PST'}
#     {'week': '5', 'home_team_id': Decimal('9'), 'Game_id': 47, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '6:30', 'Date': '5/9/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('10'), 'Game_id': 48, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '6:30', 'Date': '6/22/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('15'), 'Game_id': 49, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '7:00', 'Date': '5/9/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('1'), 'Game_id': 50, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '8:00', 'Date': '5/8/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('0'), 'Game_id': 51, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '7:30', 'Date': '5/9/2015', 'timezone': 'CST'}
#     {'week': '5', 'home_team_id': Decimal('23'), 'Game_id': 52, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '7:00', 'Date': '5/9/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('3'), 'Game_id': 53, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '8:00', 'Date': '5/10/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('19'), 'Game_id': 54, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '5/9/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('17'), 'Game_id': 55, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '6:00', 'Date': '5/9/2015', 'timezone': 'EST'}
#     {'week': '5', 'home_team_id': Decimal('21'), 'Game_id': 56, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '2:00', 'Date': '5/10/2015', 'timezone': 'CST'}
#     {'week': '5', 'home_team_id': Decimal('12'), 'Game_id': 57, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '6:00', 'Date': '5/9/2015', 'timezone': 'PST'}
#     {'week': '5', 'home_team_id': Decimal('25'), 'Game_id': 58, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '7:30', 'Date': '5/9/2015', 'timezone': 'PST'}
#     {'week': '5', 'home_team_id': Decimal('20'), 'Game_id': 59, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '1:30', 'Date': '5/10/2015', 'timezone': 'PST'}
#     {'week': '5', 'home_team_id': Decimal('16'), 'Game_id': 60, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '1:00', 'Date': '5/10/2015', 'timezone': 'PST'}
#     {'week': '6', 'home_team_id': Decimal('2'), 'Game_id': 61, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '5/16/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('22'), 'Game_id': 62, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '4:00', 'Date': '5/16/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('10'), 'Game_id': 63, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '6:30', 'Date': '5/16/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('3'), 'Game_id': 64, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '7:30', 'Date': '5/15/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('5'), 'Game_id': 65, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '7:00', 'Date': '5/15/2015', 'timezone': 'CST'}
#     {'week': '6', 'home_team_id': Decimal('4'), 'Game_id': 66, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '7:30', 'Date': '5/16/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('6'), 'Game_id': 67, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '7:00', 'Date': '5/16/2015', 'timezone': 'CST'}
#     {'week': '6', 'home_team_id': Decimal('18'), 'Game_id': 68, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '7:00', 'Date': '5/16/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('19'), 'Game_id': 69, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '5/16/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('24'), 'Game_id': 70, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '3:00', 'Date': '5/17/2015', 'timezone': 'EST'}
#     {'week': '6', 'home_team_id': Decimal('13'), 'Game_id': 71, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '7:30', 'Date': '5/15/2015', 'timezone': 'PST'}
#     {'week': '6', 'home_team_id': Decimal('12'), 'Game_id': 72, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '6:00', 'Date': '5/16/2015', 'timezone': 'PST'}
#     {'week': '6', 'home_team_id': Decimal('16'), 'Game_id': 73, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '6:00', 'Date': '5/16/2015', 'timezone': 'PST'}
#     {'week': '6', 'home_team_id': Decimal('25'), 'Game_id': 74, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '1:00', 'Date': '5/17/2015', 'timezone': 'PST'}
#     {'week': '7', 'home_team_id': Decimal('7'), 'Game_id': 75, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '4:00', 'Date': '5/23/2015', 'timezone': 'EST'}
#     {'week': '7', 'home_team_id': Decimal('10'), 'Game_id': 76, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '3:00', 'Date': '5/24/2015', 'timezone': 'EST'}
#     {'week': '7', 'home_team_id': Decimal('22'), 'Game_id': 77, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '2:00', 'Date': '5/24/2015', 'timezone': 'EST'}
#     {'week': '7', 'home_team_id': Decimal('15'), 'Game_id': 78, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '6:00', 'Date': '5/23/2015', 'timezone': 'EST'}
#     {'week': '7', 'home_team_id': Decimal('5'), 'Game_id': 79, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '7:00', 'Date': '5/22/2015', 'timezone': 'CST'}
#     {'week': '7', 'home_team_id': Decimal('0'), 'Game_id': 80, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '7:00', 'Date': '5/23/2015', 'timezone': 'CST'}
#     {'week': '7', 'home_team_id': Decimal('3'), 'Game_id': 81, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '7:00', 'Date': '5/23/2015', 'timezone': 'EST'}
#     {'week': '7', 'home_team_id': Decimal('18'), 'Game_id': 82, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '7:00', 'Date': '5/23/2015', 'timezone': 'EST'}
#     {'week': '7', 'home_team_id': Decimal('26'), 'Game_id': 83, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '6:00', 'Date': '5/23/2015', 'timezone': 'PST'}
#     {'week': '7', 'home_team_id': Decimal('25'), 'Game_id': 84, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '6:00', 'Date': '5/23/2015', 'timezone': 'PST'}
#     {'week': '7', 'home_team_id': Decimal('20'), 'Game_id': 85, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '1:30', 'Date': '5/24/2015', 'timezone': 'PST'}
#     {'week': '7', 'home_team_id': Decimal('16'), 'Game_id': 86, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '4:00', 'Date': '5/24/2015', 'timezone': 'PST'}
#     {'week': '8', 'home_team_id': Decimal('8'), 'Game_id': 87, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '5:00', 'Date': '5/30/2015', 'timezone': 'EST'}
#     {'week': '8', 'home_team_id': Decimal('22'), 'Game_id': 88, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '4:00', 'Date': '5/30/2015', 'timezone': 'EST'}
#     {'week': '8', 'home_team_id': Decimal('7'), 'Game_id': 89, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '12:00', 'Date': '5/31/2015', 'timezone': 'EST'}
#     {'week': '8', 'home_team_id': Decimal('6'), 'Game_id': 90, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '7:00', 'Date': '5/30/2015', 'timezone': 'CST'}
#     {'week': '8', 'home_team_id': Decimal('23'), 'Game_id': 91, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '7:00', 'Date': '5/30/2015', 'timezone': 'EST'}
#     {'week': '8', 'home_team_id': Decimal('17'), 'Game_id': 92, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '8:00', 'Date': '5/29/2015', 'timezone': 'EST'}
#     {'week': '8', 'home_team_id': Decimal('19'), 'Game_id': 93, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '5/30/2015', 'timezone': 'EST'}
#     {'week': '8', 'home_team_id': Decimal('21'), 'Game_id': 94, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '7:00', 'Date': '5/30/2015', 'timezone': 'CST'}
#     {'week': '8', 'home_team_id': Decimal('13'), 'Game_id': 95, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '7:00', 'Date': '5/30/2015', 'timezone': 'PST'}
#     {'week': '8', 'home_team_id': Decimal('12'), 'Game_id': 96, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '1:00', 'Date': '5/31/2015', 'timezone': 'PST'}
#     {'week': '9', 'home_team_id': Decimal('7'), 'Game_id': 97, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '4:00', 'Date': '6/6/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('8'), 'Game_id': 98, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '5:00', 'Date': '6/6/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('9'), 'Game_id': 99, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '6:30', 'Date': '6/6/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('22'), 'Game_id': 100, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '2:00', 'Date': '6/7/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('0'), 'Game_id': 101, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '7:00', 'Date': '6/5/2015', 'timezone': 'CST'}
#     {'week': '9', 'home_team_id': Decimal('4'), 'Game_id': 102, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '7:30', 'Date': '6/6/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('6'), 'Game_id': 103, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '7:00', 'Date': '6/6/2015', 'timezone': 'CST'}
#     {'week': '9', 'home_team_id': Decimal('23'), 'Game_id': 104, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '7:00', 'Date': '6/6/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('3'), 'Game_id': 105, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '1:00', 'Date': '6/7/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('17'), 'Game_id': 106, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '8:00', 'Date': '6/5/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('19'), 'Game_id': 107, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '6/6/2015', 'timezone': 'EST'}
#     {'week': '9', 'home_team_id': Decimal('21'), 'Game_id': 108, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '6:00', 'Date': '6/6/2015', 'timezone': 'CST'}
#     {'week': '9', 'home_team_id': Decimal('20'), 'Game_id': 109, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '7:30', 'Date': '6/6/2015', 'timezone': 'PST'}
#     {'week': '9', 'home_team_id': Decimal('13'), 'Game_id': 110, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '7:00', 'Date': '6/6/2015', 'timezone': 'PST'}
#     {'week': '10', 'home_team_id': Decimal('7'), 'Game_id': 111, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '7:00', 'Date': '6/13/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('8'), 'Game_id': 112, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '2:00', 'Date': '6/21/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('15'), 'Game_id': 113, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '6:00', 'Date': '6/13/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('10'), 'Game_id': 114, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '3:00', 'Date': '6/14/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('0'), 'Game_id': 115, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '7:00', 'Date': '6/12/2015', 'timezone': 'CST'}
#     {'week': '10', 'home_team_id': Decimal('3'), 'Game_id': 116, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '4:00', 'Date': '6/13/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('6'), 'Game_id': 117, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '7:00', 'Date': '6/12/2015', 'timezone': 'CST'}
#     {'week': '10', 'home_team_id': Decimal('24'), 'Game_id': 118, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '3:00', 'Date': '6/14/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('18'), 'Game_id': 119, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '7:00', 'Date': '6/13/2015', 'timezone': 'EST'}
#     {'week': '10', 'home_team_id': Decimal('21'), 'Game_id': 120, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '2:00', 'Date': '6/14/2015', 'timezone': 'CST'}
#     {'week': '10', 'home_team_id': Decimal('16'), 'Game_id': 121, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '6:00', 'Date': '6/13/2015', 'timezone': 'PST'}
#     {'week': '10', 'home_team_id': Decimal('25'), 'Game_id': 122, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '1:00', 'Date': '6/14/2015', 'timezone': 'PST'}
#     {'week': '11', 'home_team_id': Decimal('2'), 'Game_id': 123, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '6/20/2015', 'timezone': 'EST'}
#     {'week': '11', 'home_team_id': Decimal('15'), 'Game_id': 124, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '6:00', 'Date': '6/20/2015', 'timezone': 'EST'}
#     {'week': '11', 'home_team_id': Decimal('10'), 'Game_id': 125, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '3:00', 'Date': '6/21/2015', 'timezone': 'EST'}
#     {'week': '11', 'home_team_id': Decimal('0'), 'Game_id': 126, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '7:00', 'Date': '6/19/2015', 'timezone': 'CST'}
#     {'week': '11', 'home_team_id': Decimal('1'), 'Game_id': 127, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '7:30', 'Date': '6/20/2015', 'timezone': 'EST'}
#     {'week': '11', 'home_team_id': Decimal('5'), 'Game_id': 128, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '6:00', 'Date': '6/20/2015', 'timezone': 'CST'}
#     {'week': '11', 'home_team_id': Decimal('18'), 'Game_id': 129, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '7:00', 'Date': '6/20/2015', 'timezone': 'EST'}
#     {'week': '11', 'home_team_id': Decimal('19'), 'Game_id': 130, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '6/20/2015', 'timezone': 'EST'}
#     {'week': '11', 'home_team_id': Decimal('26'), 'Game_id': 131, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '6:00', 'Date': '6/20/2015', 'timezone': 'PST'}
#     {'week': '11', 'home_team_id': Decimal('13'), 'Game_id': 132, 'am/pm': 'PM', 'away_team_id': Decimal('13'), 'time': '7:00', 'Date': '6/20/2015', 'timezone': 'PST'}
#     {'week': '11', 'home_team_id': Decimal('20'), 'Game_id': 133, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '1:30', 'Date': '6/21/2015', 'timezone': 'PST'}
#     {'week': '11', 'home_team_id': Decimal('12'), 'Game_id': 134, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '1:00', 'Date': '6/21/2015', 'timezone': 'PST'}
#     {'week': '12', 'home_team_id': Decimal('7'), 'Game_id': 135, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '7:00', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('2'), 'Game_id': 136, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('15'), 'Game_id': 137, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '6:00', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('8'), 'Game_id': 138, 'am/pm': 'PM', 'away_team_id': Decimal('8'), 'time': '12:00', 'Date': '6/28/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('1'), 'Game_id': 139, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '7:30', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('3'), 'Game_id': 140, 'am/pm': 'PM', 'away_team_id': Decimal('3'), 'time': '4:00', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('4'), 'Game_id': 141, 'am/pm': 'PM', 'away_team_id': Decimal('4'), 'time': '3:30', 'Date': '6/28/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('23'), 'Game_id': 142, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '2:00', 'Date': '6/28/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('18'), 'Game_id': 143, 'am/pm': 'PM', 'away_team_id': Decimal('18'), 'time': '7:00', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('24'), 'Game_id': 144, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '7:00', 'Date': '6/27/2015', 'timezone': 'EST'}
#     {'week': '12', 'home_team_id': Decimal('16'), 'Game_id': 145, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '6:00', 'Date': '6/27/2015', 'timezone': 'PST'}
#     {'week': '12', 'home_team_id': Decimal('25'), 'Game_id': 146, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '2:00', 'Date': '6/28/2015', 'timezone': 'PST'}
#     {'week': '13', 'home_team_id': Decimal('10'), 'Game_id': 147, 'am/pm': 'PM', 'away_team_id': Decimal('10'), 'time': '7:00', 'Date': '7/3/2015', 'timezone': 'EST'}
#     {'week': '13', 'home_team_id': Decimal('22'), 'Game_id': 148, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '4:00', 'Date': '7/4/2015', 'timezone': 'EST'}
#     {'week': '13', 'home_team_id': Decimal('7'), 'Game_id': 149, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '12:00', 'Date': '7/5/2015', 'timezone': 'EST'}
#     {'week': '13', 'home_team_id': Decimal('17'), 'Game_id': 150, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '7:00', 'Date': '7/4/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('2'), 'Game_id': 151, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '7/11/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('2'), 'Game_id': 152, 'am/pm': 'PM', 'away_team_id': Decimal('2'), 'time': '6:30', 'Date': '7/10/2015', 'timezone': 'EST'}
#     {'week': '15', 'home_team_id': Decimal('22'), 'Game_id': 153, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '7:30', 'Date': '7/18/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('9'), 'Game_id': 154, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '1:00', 'Date': '7/12/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('23'), 'Game_id': 155, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '7:00', 'Date': '7/10/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('1'), 'Game_id': 156, 'am/pm': 'PM', 'away_team_id': Decimal('1'), 'time': '7:30', 'Date': '7/11/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('6'), 'Game_id': 157, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '7:00', 'Date': '7/11/2015', 'timezone': 'CST'}
#     {'week': '14', 'home_team_id': Decimal('5'), 'Game_id': 158, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '12:00', 'Date': '7/12/2015', 'timezone': 'CST'}
#     {'week': '14', 'home_team_id': Decimal('19'), 'Game_id': 159, 'am/pm': 'PM', 'away_team_id': Decimal('19'), 'time': '6:00', 'Date': '7/11/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('24'), 'Game_id': 160, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '7:00', 'Date': '7/11/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('17'), 'Game_id': 161, 'am/pm': 'PM', 'away_team_id': Decimal('17'), 'time': '3:00', 'Date': '7/12/2015', 'timezone': 'EST'}
#     {'week': '14', 'home_team_id': Decimal('26'), 'Game_id': 162, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '6:00', 'Date': '7/11/2015', 'timezone': 'PST'}
#     {'week': '15', 'home_team_id': Decimal('15'), 'Game_id': 163, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '8:00', 'Date': '7/16/2015', 'timezone': 'EST'}
#     {'week': '15', 'home_team_id': Decimal('9'), 'Game_id': 164, 'am/pm': 'PM', 'away_team_id': Decimal('9'), 'time': '6:30', 'Date': '7/18/2015', 'timezone': 'EST'}
#     {'week': '15', 'home_team_id': Decimal('22'), 'Game_id': 165, 'am/pm': 'PM', 'away_team_id': Decimal('22'), 'time': '7:30', 'Date': '7/18/2015', 'timezone': 'EST'}
#     {'week': '15', 'home_team_id': Decimal('15'), 'Game_id': 166, 'am/pm': 'PM', 'away_team_id': Decimal('15'), 'time': '2:30', 'Date': '7/19/2015', 'timezone': 'EST'}
#     {'week': '15', 'home_team_id': Decimal('6'), 'Game_id': 167, 'am/pm': 'PM', 'away_team_id': Decimal('6'), 'time': '7:00', 'Date': '7/17/2015', 'timezone': 'CST'}
#     {'week': '15', 'home_team_id': Decimal('5'), 'Game_id': 168, 'am/pm': 'PM', 'away_team_id': Decimal('5'), 'time': '7:00', 'Date': '7/17/2015', 'timezone': 'CST'}
#     {'week': '15', 'home_team_id': Decimal('23'), 'Game_id': 169, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '7:00', 'Date': '7/18/2015', 'timezone': 'EST'}
#     {'week': '15', 'home_team_id': Decimal('0'), 'Game_id': 170, 'am/pm': 'PM', 'away_team_id': Decimal('0'), 'time': '1:00', 'Date': '7/19/2015', 'timezone': 'CST'}
#     {'week': '15', 'home_team_id': Decimal('21'), 'Game_id': 171, 'am/pm': 'PM', 'away_team_id': Decimal('21'), 'time': '7:00', 'Date': '7/18/2015', 'timezone': 'CST'}
#     {'week': '15', 'home_team_id': Decimal('26'), 'Game_id': 172, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '6:00', 'Date': '7/17/2015', 'timezone': 'PST'}
#     {'week': '15', 'home_team_id': Decimal('20'), 'Game_id': 173, 'am/pm': 'PM', 'away_team_id': Decimal('20'), 'time': '7:30', 'Date': '7/18/2015', 'timezone': 'PST'}
#     {'week': '15', 'home_team_id': Decimal('12'), 'Game_id': 174, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '6:00', 'Date': '7/18/2015', 'timezone': 'PST'}
#     {'week': '15', 'home_team_id': Decimal('25'), 'Game_id': 175, 'am/pm': 'PM', 'away_team_id': Decimal('25'), 'time': '6:00', 'Date': '7/18/2015', 'timezone': 'PST'}
#     {'week': '15', 'home_team_id': Decimal('16'), 'Game_id': 176, 'am/pm': 'PM', 'away_team_id': Decimal('16'), 'time': '1:00', 'Date': '7/19/2015', 'timezone': 'PST'}
#     {'week': '15', 'home_team_id': Decimal('26'), 'Game_id': 177, 'am/pm': 'PM', 'away_team_id': Decimal('26'), 'time': '6:00', 'Date': '7/19/2015', 'timezone': 'PST'}
#     {'week': '16', 'home_team_id': Decimal('7'), 'Game_id': 178, 'am/pm': 'PM', 'away_team_id': Decimal('7'), 'time': '7:30', 'Date': '7/24/2015', 'timezone': 'EST'}
#     {'week': '16', 'home_team_id': Decimal('23'), 'Game_id': 179, 'am/pm': 'PM', 'away_team_id': Decimal('23'), 'time': '1:00', 'Date': '7/25/2015', 'timezone': 'CST'}
#     {'week': '16', 'home_team_id': Decimal('24'), 'Game_id': 180, 'am/pm': 'PM', 'away_team_id': Decimal('24'), 'time': '7:00', 'Date': '7/25/2015', 'timezone': 'EST'}
#     {'week': '16', 'home_team_id': Decimal('12'), 'Game_id': 181, 'am/pm': 'PM', 'away_team_id': Decimal('12'), 'time': '6:00', 'Date': '7/25/2015', 'timezone': 'PST'}
#     Number of games added: 182
# 

# In[ ]:



