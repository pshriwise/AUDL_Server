#!/usr/bin/python

import SimpleHTTPServer, SocketServer

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/form":  # Dispatch based on the URL
            self.send_response(200)      # Send 200 OK
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("""\
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml' lang='en' xml:lang='en'>
  <head>
    <title>Demo</title>
  </head>
  <body>
    <form action='/form_response' method='POST'>
      <input type='text' name='thename' value='Buckingham U. Badger'/>
      <input type='submit' value='Submit'/>
    </form>
  </body>
</html>""")
            return 
        
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Hello Bucky!")


PORT=1234
httpd = SocketServer.ThreadingTCPServer(("", PORT), Handler) # Can also use ForkingTCPServer
print "serving at port", PORT
httpd.serve_forever()
