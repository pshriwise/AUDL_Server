#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import AUDLclasses
import json
import image_get as ig
import youtube as yt
import threading
import sheet_reader as sr
import argparse

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
                   'AllGames'  : League.return_all_games_by_div(),
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
    elif len(path_ents) > 1 and path_ents[0] == "Web":
        return web_data(path_ents, League)
    elif len(path_ents) == 1 and "gameupdate" in path_ents[0] :
        return update_game(path_ents, League)
    else:
        return "Not a valid path"


def update_game( path_ents, League ):

    key, params = parse_callback( path_ents[-1] )

    #update the game indicated by the path 
    team = League.Teams[int(params['team'])]
    for key, game in team.Games.items():
        home_hash = None if not hasattr(game, 'home_id') else game.home_id.split('/')[-1] 
        away_hash = None if not hasattr(game, 'away_id') else game.away_id.split('/')[-1]
        if params['game'] == home_hash or params['game'] == away_hash:
            game.update()            
            return "Updated game on " + game.date + " for team " + team.Name

    #if we're still in the function, we did not find this game for the given team
    #have the team update all games in case this is a new game
    team.get_games_info()
    return "Could not find this game for the team, checking for new games..."
                                            
    
                                        
#intended for use with AUDL widgets/webpages
def web_data( path_ents, League ):

    # dictionary of functions this endpoint will be able to call
    widgets = { 'Standings' : League.web_standings,
                'Scores'    : League.score_ticker,
                'Score'     : League.latest_game }

    key, params = parse_callback( path_ents[-1] )
    
    return params['callback'] + "('" + json.dumps(widgets[key](params))  + "')"

#ef teams_latest_game( League, 

def parse_callback( web_params ):

    path_ents = web_params.split('?')
    # for the local function to call should be right before the ?
    key = path_ents[0]

    param_dict={}
    # now split the remaining path on ampersands to get the sets of key/values
    # from the path
    param_pairs = path_ents[1].split('&')

    for param_pair in param_pairs:
        
        temp = param_pair.split('=')
        param_dict[temp[0]] = temp[1]

                           
    return key, param_dict
           

                       
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
        return [game.home_team,game.away_team,game.home_score,game.away_score,[game.Home_stats,game.Away_stats],game.status]
    else:
       return  [game.home_team,game.away_team,0,0,[game.Home_stats,game.Away_stats],game.status]
    
    
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
        
        #use the typical request handler for icons
        if self.path.endswith((".png", ".css", ".js", ".html")):

            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        else:
            
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
sr.get_csv( sr.spreadsheet_key, sr.Team_Info_gid, sr.Team_Info_Filename )
sr.get_csv( sr.spreadsheet_key, sr.Schedule_gid, sr.Schedule_Filename )
sr.get_csv( sr.spreadsheet_key, sr.Rosters_gid, sr.Rosters_filename )
AUDL.add_teams()
# Get news articles for the team
AUDL.get_news()

def parse_args():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--IP', dest = 'IP', required=False, type=str, default="")
    parser.add_argument('--PORT', dest = 'PORT', required=False, type=int, default=4000)
    parser.add_argument('--refresh-int', dest= 'interval', required=False, type=int, default=600)

    return parser.parse_args()

def main():
    
    args = parse_args()
    # Start broadcasting the server
    httpd = SocketServer.ThreadingTCPServer((args.IP, args.PORT), Handler) # Can also use ForkingTCPServer
    httpd.request_queue_size = 30
    print "serving at" , args.IP, "port", args.PORT
    httpd.serve_forever()

def refresh():
    print "refreshing server...",
    #set interval to one day

    args = parse_args()
    interval = args.interval
    threading.Timer(interval,refresh).start()
    AUDL.update_games()
    AUDL.get_news()
    sr.get_csv( sr.spreadsheet_key, sr.Team_Info_gid, sr.Team_Info_Filename )
    sr.get_csv( sr.spreadsheet_key, sr.Schedule_gid, sr.Schedule_Filename )
    sr.get_csv( sr.spreadsheet_key, sr.Rosters_gid, sr.Rosters_filename )
    for ID,team in AUDL.Teams.items():
        team.add_player_stats()
        team.populate_team_stats()
    print "done"

if __name__ == "__main__":
    refresh()
    main()
