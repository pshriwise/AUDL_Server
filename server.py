#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import AUDLclasses as cls
import json


AUDL = cls.League()
AUDL.add_teams()

print "Adding players to teams..."
for t in AUDL.Teams:
    AUDL.Teams[t].add_players()


# Parse a given input path to the server
def path_parse(path):

    if path == '': return ''

    path_ents = path.split("/")
    for ent in path_ents:
        print ent

    return path_ents[1:]
    pass

# Directs the path to the correct data-gathering function
def direct_path(path_ents):

    if type(path_ents) is not list: return "Not a valid path"    
    possible_paths = ["Teams","Scores","Standings","Schedule","Videos","Stats","News"]
    # Make sure the first path entity matches something we expect
    print possible_paths.count(path_ents[0])
    if possible_paths.count(path_ents[0]) == 0:
        return ""

    if path_ents[0] == "Teams" and len(path_ents) != 1:

        Team_ID = int(path_ents[1])
        Team = AUDL.Teams[Team_ID]
        if path_ents[2] == "Roster":
            return Team.roster()
        elif path_ehts[2] == "Stats":
            return Team.stats
        #Enter Schedue info here when ready
    else:
        return AUDL.team_list()

    if path_ents[0] == "Standings" and len(path_ents) != 1:
    
        Div_ID = int(path_ents[1])
        return "Division-specific standings info"
            
    else: 
        return "League-wide standings information"

    if path_ents[0] == "Scores" and len(path_ents) != 1:

        Div_ID = int(path_ents[1])
        return "Division - specific scores for the past week"

    else:
        return "League-wide scores for the past week"

    if path_ents[0] == "Schedule" and len(path_ents) != 1:
        
        Div_ID=int(path_ents[1])
        return "Division - specific schedule for  the upcoming weekend"

    else:
        return "League-wide schedule for the upcoming week"

    if path_ents[0] == "Stats":
    
        return "League-wide stat leaders"

    if path_ents[0] == "Videos":

        return AUDL.Videos

    if path_ents[0] == "News":

        return AUDL.News
                  


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
            #We can always respond with json code
            self.send_response(200)     #  Send 200 OK
            self.send_header("Content-type","json")
            self.end_headers()
            #Function for path handling goes here:
            path_ents = path_parse(self.path)
            self.wfile.write(json.dumps(direct_path(path_ents)))


PORT=4000
httpd = SocketServer.ThreadingTCPServer(("192.168.1.134", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()


def data_for_path(path):
    path_ents = path.split("/")
    if path_ents == []:
        pass


