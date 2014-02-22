#!/usr/bin/python

import SimpleHTTPServer, SocketServer
from  statget import *
top_three_assists = top_three(name_to_id('Madison Radicals'), 'assists')
top_three_goals = top_three(name_to_id('Madison Radicals'), 'goals')

team_rosters= rosters()

def get_team_roster(team_id, rosters):
    for team, number, roster in team_rosters:
        if (number == team_id):
            return [team, number, roster]

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):


    def path_data(self):
        paths=self.path.split('/')
        paths.remove('')
        if (paths[0] == 'teams') & (len(paths) == 1):
            return team_dict()
        elif paths[0] == 'teams':
            get_team_roster(paths[1],team_rosters)
                  



    def do_GET(self):
        if self.path == "/goals":
            self.send_response(200)     #  Send 200 OK
            self.send_header("Content-type","text")
            self.end_headers()
            self.wfile.write(top_three_goals)
        elif self.path == "/assists":
            self.send_response(200)     #  Send 200 OK
            self.send_header("Content-type","text")
            self.end_headers()
            self.wfile.write(top_three_assists)


PORT=4000
httpd = SocketServer.ThreadingTCPServer(("192.168.1.134", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
