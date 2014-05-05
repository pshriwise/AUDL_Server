#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import AUDLclasses
import json
import image_get as ig
import youtube as yt
import threading

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

    #Create dictionary for main information:
    main_pages = { 'Teams'     : League.team_list(),
                   'News'      : League.news_page_info(),
                   'Standings' : League.standings(),
                   'Scores'    : League.return_scores_page(),
                   'Schedule'  : League.return_schedules(),
                   'Videos'    : League.get_videos(),
                   'Stats'     : League.get_top_fives(),
                   'FAQ'       : "Coming soon",
                   'Terms_and_Info' : "Coming soon",
                   'Home'      : (League.news_page_info(),League.get_videos(),League.return_upcoming())}


    path_ents = path_parse(path)
    # If the length of path_ents is one and the page requested exists
    # then return the info for that page
    if len(path_ents) == 1 and path_ents[0] in main_pages.keys():
        return json.dumps(main_pages[path_ents[0]])
    elif len(path_ents) > 1 and path_ents[0] in main_pages.keys():
        return json.dumps(subpage_data(path_ents, League))
    elif len(path_ents) > 1 and path_ents[0] == "Icons":
        return subpage_data(path_ents, League)
    elif len(path_ents) > 1 and path_ents[0] == "Game":
        return subpage_data(path_ents, League)
    else:
        return "Not a valid path"


def subpage_data(path_ents, League):
    """
    Function for returning the correct set of subpage data.

    This function expects that len(path_ents) is greater than 1.
    """
    if len(path_ents) < 2 or len(path_ents) > 6: return "Not a valid path"

    # We expect the second entry of this path to be a team_id
    team_id = int(path_ents[1]) 
    # Corner case for the Montreal Royal Logo
    if path_ents[0] == "Icons" and path_ents[1] == "1234":
        return ig.AUDLlogo("Royal")
    if team_id in League.Teams.keys():
        team = League.Teams[team_id]
    
    if path_ents[0] == "Teams":
        return team_subpage_data(team_id, team)
    elif path_ents[0] == "Icons":
        # the true case is a corner statement 
        # only the false case will be needed after 2014 games begin
        #return ig.AUDLlogo('Phoenix') if team_id == 208004 else ig.AUDLlogo(team.Name)
        return ig.AUDLlogo(team.Name)
    elif path_ents[0] == "Game":
        #return the detailed game info
        return json.dumps(game_page_data(team,path_ents[2:])) if path_ents[-1] != "graph" else json.dumps(game_graph(team,path_ents[1:]))
    else:
        return "Not a valid path"

def team_subpage_data(subpage, team):
    """
    Returns a subpage for a given team class instance. 
    """
    return [team.roster(), team.return_schedule(), team.Top_Fives, AUDL.return_games([team.ID],scores=True,all=True)]

def schedule_page_data(League):

    data_out = []

    if hasattr(League, 'Divisions'):
        for div in League.Divisions:
            div_sched = [div]
            for team in League.Divisions[div]:
                div_sched.append(League.Teams[team].return_schedule())
            data_out.append(div_sched)
        return data_out
    else:
        return "This League does not contain divisions"

def game_page_data(team, path_ents):
    """
    Tells the team's game to generate stat info from its endpoint.
    """
    if len(path_ents) !=3: return "Not a valid game date"

    #create date string from the remaining path ents
    date=path_ents[0]+"/"+path_ents[1]+"/"+path_ents[2]

    game = team.Games[date]
    if hasattr(game, "home_score") and hasattr(game, "away_score"):
        return [game.home_team,game.away_team,game.home_score,game.away_score,game.stat_info(),game.status]
    else:
       return  [game.home_team,game.away_team,0,0,game.stat_info(),game.status]
    
    
def game_graph(team,path_ents):
  
    if path_ents[-1] != "graph" : return "Not a valid path"
    #get game class
    game = team.Games["/".join(path_ents[1:4])]

    if hasattr(game,"graph_pnts"):
        return game.graph_pnts
    else:
        return "No graph available for this game"

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
            #We can always respond with json code
            self.send_response(200) # Send 200 OK

            #Function for path handling goes here:
            path_ents = path_parse(self.path)
            if path_ents[0] == "Icons" or path_ents[0] == "Game":
                self.send_header("Content-type","png")
                self.end_headers()
            else:
                self.send_header("Content-type","json")
                self.end_headers()

            self.wfile.write(path_data(self.path,AUDL))

# Initialize the league class
AUDL = AUDLclasses.League()
# Add teams from local files and populate
# their information from the ultimate-numbers 
# server
AUDL.add_teams('Teams_Info')
# Get news articles for the team
AUDL.get_news()


def main():
    

    # Start broadcasting the server
    PORT=4000
    IP = ""
    httpd = SocketServer.ThreadingTCPServer((IP, PORT), Handler) # Can also use ForkingTCPServer
    print "serving at" , IP, "port", PORT
    httpd.serve_forever()

def refresh():
    print "refreshing server...",
    threading.Timer(60,refresh).start()
    AUDL.update_games()
    AUDL.get_news()
    for ID,team in AUDL.Teams.items():
        team.add_player_stats()
        team.populate_team_stats()
    print "done"

if __name__ == "__main__":
    refresh()
    main()
