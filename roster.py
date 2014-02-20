import urllib2 
import json

req = urllib2.Request('http://www.ultimate-numbers.com/rest/view/team/224002/players')
response = urllib2.urlopen(req)
the_page = response.read()


data = json.loads(the_page)


print "Madison Radicals Roster:"


for player in data:
    deets = json.loads(player['leaguevinePlayer'])
    #print ( deets['player']['first_name'], deets ['player']['last_name'], deets['number'])
    print ( "%s %s %s" % ( deets['player']['first_name'], deets ['player']['last_name'], deets['number']))




