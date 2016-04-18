#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import json
import notification_handler
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
            if 'ios' in path_ents:
                notification_handler.register_ios_token(path_ents)
                self.send_header("Content-type","text")
                self.end_headers()                
                return
            elif 'android' in path_ents:
                notification_handler.register_android_token(path_ents)
                self.send_header("Content-type","text")
                self.end_headers()                
                return
                

def parse_args():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--IP', dest = 'IP', required=False, type=str, default="")
    parser.add_argument('--PORT', dest = 'PORT', required=False, type=int, default=4000)
    return parser.parse_args()

def main():
    
    args = parse_args()
    # Start broadcasting the server
    httpd = SocketServer.ThreadingTCPServer((args.IP, args.PORT),Handler) # Can also use ForkingTCPServer
    httpd.request_queue_size = 30
    print "serving at" , args.IP, "port", args.PORT
    httpd.serve_forever()



if __name__ == "__main__":
    main()
