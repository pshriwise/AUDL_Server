#!/usr/bin/python

import SimpleHTTPServer, SocketServer
import json
import notification_handler
import argparse
import urlparse

# Parse a given input path to the server
def path_parse(path):

    if path == '': return ''
    if path[-1] == '/': path = path[:-1]

    path_ents = path.split("/")
    for ent in path_ents:
        print ent

    return path_ents[1:]
    pass

def extract_data(handler,data_key):
    try:
        print post_data[data_key][0]
        return post_data[data_key][0]
    except:
        return ""
    
def extract_token(handler):
    return extract_data(handler,'token')

def extract_team(handler):
    return extract_data(handler,'team')

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
                notification_handler.register_ios_token_from_path(path_ents)
                self.send_header("Content-type","text")
                self.end_headers()                
                return
            elif 'android' in path_ents:
                notification_handler.register_android_token_from_path(path_ents)
                self.send_header("Content-type","text")
                self.end_headers()                
                return
                

    def do_POST(self):
            #We can always respond with json code
            self.send_response(200) # Send 200 OK
            #Function for path handling goes here:
            length = int(self.headers['Content-Length'])
            post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
            token = post_data['token'][0]
            note_type = post_data['note_type'][0]
            platform = post_data['platform'][0]
            print platform
            if 'ios' == platform:
                if 'general' == note_type:
                    notification_handler.register_general_ios_token(token)
                else:
                    team = note_type
                    notification_handler.register_team_ios_token(team,token)
            elif 'android' == platform:
                if 'general' == note_type:
                    notification_handler.register_general_android_token(token)
                else:
                    team = note_type
                    notification_handler.register_team_android_token(team,token)
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
