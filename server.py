#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import AUDLclasses as cls
import json


AUDL = cls.League()
AUDL.add_teams()
AUDL.get_news()

# Parse a given input path to the server
def path_parse(path):

    if path == '': return ''
    if path[-1] == '/': path = path[:-1]

    path_ents = path.split("/")
    for ent in path_ents:
        print ent

    return path_ents[1:]
    pass

                  
def path_data(path, League):

    # Dummy info for the Standings Page
    Stand_list = [["Midwest Division", ('Madison Radicals', '10-3'),('Chicago Wildfire', '9-4')],["Eastern Division",("DC Breeze", '10-3'),("New York Empire",'9-4')]]
 
    # Dummy info for the schedule Page
    Sched_list = []
    Sched_list.append(["Midwest Division", League.Teams[224002].return_schedule(), League.Teams[207003].return_schedule()])
    Sched_list.append(["Eastern Division", League.Teams[208003].return_schedule(), League.Teams[206001].return_schedule()])


    #Create dictionary for main information:
    main_pages = { 'Teams'     : League.team_list(),
                   'News'      : League.news_page_info(),
                   'Standings' : Stand_list,
                   'Scores'    : "Coming soon",
                   'Schedule'  : Sched_list,
                   'Videos'    : "Coming soon",
                   'Stats'     : "Coming soon",
                   'FAQ'       : "Coming soon",
                   'Terms_and_Info' : "Coming soon"}


    path_ents = path_parse(path)
    # If the length of path_ents is one and the page requested exists
    # then return the info for that page
    if len(path_ents) == 1 and path_ents[0] in main_pages.keys():
        return main_pages[path_ents[0]]
    elif len(path_ents) > 1 and path_ents[0] in main_pages.keys():
        return subpage_data(path_ents, League)
    else:
        return "Not a valid path"


def subpage_data(path_ents, League):
    """
    Function for returning the correct set of subpage data.

    This function expects that len(path_ents) is 3.
    """
    #if len(path_ents) != 3: return "Not a valid path"

    if path_ents[0] == "Teams":
        team_id = int(path_ents[1])
        if team_id in League.Teams.keys():
            team = League.Teams[team_id]
        return team_subpage_data(path_ents[2], team)
    elif path_ents[0] == "Standings":
        return standings_subpage_data(path_ents[1], League)
    elif path_ents[0] == "Scores":
        return "Coming soon"
    elif path_ents[0] == "Schedule":
        return schedule_subpage_data(path_ents[1], League)
    else:
        return "Not a valid path"

def team_subpage_data(subpage, team):
    """
    Returns a subpage for a given team class instance. 

    
    """
    # Right now this assumes these attributes exist. 
    # Should be updated at some point. 
    
    subpages ={ 'Roster'   : team.roster(),
                'Schedule' : team.return_schedule(),
                'Stats'    : team.Top_Fives
              }
    if subpage in subpages.keys():
        return subpages[subpage]
    else:
        return "Not a valid path"

def schedule_subpage_data(division, League):

    if division == "Midwest":
        return ["Midwest Division", League.Teams[224002].return_schedule(), League.Teams[207003].return_schedule()]
    elif division == "Eastern":
        return ["Eastern Division", League.Teams[208003].return_schedule(), League.Teams[206001].return_schedule()]
    else: 
        return "Not a valid path"

def standings_subpage_data(division, League):

    if division == "Midwest":
        return ["Midwest Division", ('Madison Radicals', '10-3'),('Chicago Wildfire', '9-4')]
    elif division == "Eastern":
        return ["Eastern Division",("DC Breeze", '10-3'),("New York Empire",'9-4')]
    else:
        return "Not a valid path"

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
            #We can always respond with json code
            self.send_response(200)     #  Send 200 OK
            self.send_header("Content-type","json")
            self.end_headers()
            #Function for path handling goes here:
            path_ents = path_parse(self.path)
            self.wfile.write(json.dumps(path_data(self.path,AUDL)))


PORT=4001
httpd = SocketServer.ThreadingTCPServer(("192.168.1.134", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()






 

    
