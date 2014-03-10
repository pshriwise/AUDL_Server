#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import AUDLclasses as cls
import json

AUDL = cls.League()
AUDL.add_teams()

print "Adding players to teams..."
for t in AUDL.Teams:
    AUDL.Teams[t].add_players()


                  


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
            self.send_response(200)     #  Send 200 OK
            self.send_header("Content-type","text")
            self.end_headers()
            self.wfile.write(json.dumps(AUDL.Teams[224002].roster()))


PORT=4000
httpd = SocketServer.ThreadingTCPServer(("192.168.1.134", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
