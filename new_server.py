

import SimpleHTTPServer, SocketServer
import requests
from threading import Thread

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):

        # handle some file calls
        if self.path.endswith((".png", ".css", ".js", ".html")):
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        # forward all database calls
        else:
            resp = requests.get("https://audl-stat-server.herokuapp.com/aa/" + self.path)
            self.send_response(200)
            self.send_header("Content-type", "json")
            self.end_headers()
            self.wfile.write(resp.content)

ports = [4001, 4002, 4003]

def start_on_port(port):
    print("Starting server on port " + str(port))
    server = SocketServer.ThreadingTCPServer(("",port), Handler)
    server.request_queue_size = 100
    server.serve_forever()
 
for port in ports:
    Thread(target=start_on_port, args=[port]).start()
