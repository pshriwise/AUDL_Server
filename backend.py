#!/usr/bin/python

import SimpleHTTPServer, SocketServer
from statget import top_three,name_to_id
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    top_three_assists = top_three(name_to_id('Madison Radicals'), 'assists')

    def do_GET(self):
        self.send_response(200)     #  Send 200 OK
        self.send_header("Content-type","text")
        self.end_headers()
        self.wfile.write(self.top_three_assists)


PORT=4000
httpd = SocketServer.ThreadingTCPServer(("192.168.1.134", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
