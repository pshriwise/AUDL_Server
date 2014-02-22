#!/usr/bin/python

import SimpleHTTPServer, SocketServer
from statget import top_three,name_to_id

top_three_assists = top_three(name_to_id('Madison Radicals'), 'assists')
top_three_goals = top_three(name_to_id('Madison Radicals'), 'goals')

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):



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
