from notifications_report import favorite_teams_table
from hit_report import generate_hit_report
import SocketServer, SimpleHTTPServer
from threading import Thread

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        favorite_teams_table()
        generate_hit_report()
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def serve():        
    server = SocketServer.ThreadingTCPServer(("",5000), Handler)
    server.serve_forever()

Thread(target=serve, args=[]).start()

