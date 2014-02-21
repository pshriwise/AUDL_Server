#!/usr/bin/python

import SimpleHTTPServer, SocketServer
from statget import top_three,name_to_id
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)     #  Send 200 OK
        # Uncomment this line to pretend the response is a JPG image
        # self.send_header("Content-type", "image/jpg")
        a = top_three(name_to_id('Madison Radicals'), 'goals')
        self.end_headers()
        self.wfile.write(a)


PORT=1234
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
