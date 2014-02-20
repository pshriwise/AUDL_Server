#!/usr/bin/python

import urllib2 
import json

req = urllib2.Request('http://www.ultimate-numbers.com/rest/view/team/224002/stats/player')
response = urllib2.urlopen(req)
the_page = response.read()

data = json.loads(the_page)
data.sort(key = lambda player_asst: player_asst['assists'], reverse= True )

top_three = data[0:3]
for player in top_three[:]:
    print player['playerName'], player['assists']

#for player in data:
#    print ( "%s %s" % (player['playerName'], player['assists']))
