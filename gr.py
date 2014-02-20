import urllib2 
import json

req = urllib2.Request('http://www.ultimate-numbers.com/rest/view/team/224002/stats/player')
response = urllib2.urlopen(req)
the_page = response.read()


data = json.loads(the_page)


for player in data:
    if( player['playerName'] == "Pat S" ):
        print player['playerName']
        for stat in player:
            print stat
            print player[stat]
