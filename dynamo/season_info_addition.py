# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import dynamo_conn
import csv
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2.fields import HashKey,RangeKey

# <codecell>

#Create connection to dynamodb
conn = dynamo_conn.get_connection()

# <codecell>

#Create a new table (commented, don't want to do this every time)
#table = Table.create('seasonal_team_info',schema=[HashKey('team_id',data_type=NUMBER),RangeKey('season',data_type=NUMBER)],throughput={'read':25,'write':25},connection=conn)
#conn.delete_table('seasonal_team_info')

# <codecell>

#Grab the team_metadata table from db
metadata = Table('team_metadata',connection=conn)
#Grab the season info table from db (assume we aren't creating it in this instance)
seasonal_data = Table('seasonal_team_info',connection=conn)

# <codecell>

#Get the google doc for the 2015 season
season = '2015'
reader = csv.reader(open('2015_Team_Info.csv','rb'))
keys = reader.next()
print keys

# <codecell>

#For every team in the .csv, find its corresponding team_id using it's name and create an entry for it in the season table
for row in reader:
    dict = { key:row[i] for i,key in enumerate(keys)}
    result = list(metadata.scan(name__eq=dict['Team Names']))
    if len(result) == 1:
        #Create a new entry for the team using that item's team_id and the row's UA id and Division
        if dict['Team ID'] is not '':
            data = {'team_id': result[0]['team_id'], 'season':int(season), 'division':dict['Divison'],'ua_id':int(dict['Team ID'])}
            print data
            #seasonal_data.put_item(data=data,overwrite=True)
    else:
        print "Error, could not find team"
        print dict['Combined Names']
        break

# <codecell>

#Now do the same for the 2014 season
season = '2014'
reader = csv.reader(open('2014_Team_Info.csv','rb'))
keys = reader.next()
print keys

# <codecell>

#For every team in the .csv, find its corresponding team_id using it's name and create an entry for it in the season table
for row in reader:
    dict = { key:row[i] for i,key in enumerate(keys)}
    result = list(metadata.scan(name__eq=dict['Team Names']))
    if len(result) == 1:
        #Create a new entry for the team using that item's team_id and the row's UA id and Division
        if dict['Team ID'] is not '':
            data = {'team_id': result[0]['team_id'], 'season':int(season), 'division':dict['Divison'],'ua_id':int(dict['Team ID'])}
            print data
            seasonal_data.put_item(data=data,overwrite=True)
    else:
        print "Error, could not find team"
        print dict['Combined Names']
        break

# <codecell>


