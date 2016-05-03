from notifications_report import favorite_teams_table
import SocketServer, SimpleHTTPServer
from threading import Thread

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        favorite_teams_table()
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def serve():        
    server = SocketServer.ThreadingTCPServer(("",5000), Handler)
    server.serve_forever()

Thread(target=serve, args=[]).start()

