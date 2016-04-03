import threading
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer
import pandas as pd

import getdata

FILE = 'frontend.html'
PORT = 8002


class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        """Handle a post request"""
        length = int(self.headers.getheader('content-length'))        
        data_string = self.rfile.read(length)
        print(data_string)
        if data_string == 'predict':
            try:
                result = pd.read_csv("prediction.csv")
                result = getdata.select_columns(result, columns=['Date','HomeTeam','AwayTeam','Prediction'])
                result = result.to_html()
                result = "<div style = 'display: inline-block;'>"+result+"</div><br>"
                
            except:
                result = 'error'
        else:
            try:
                result = getdata.last_six(data_string)
                result = result.to_html()
                result = "<h3>"+data_string+" Last Six Games</h3><div style = 'display: inline-block;'>"+result+"</div><br><h4> WDL: Team gets +1 for win, -1 for loss</h4>"
                #result = unicode(result)
            except:
                result = 'error'
        self.wfile.write(result)
        
"""        
    def do_GET(self):
        #length = int(self.headers.getheader('content-length'))        
        #data_string = self.rfile.read(length)
        try:
            result = pd.read_csv("prediction.csv")
            result = getdata.select_columns(result, columns=['Date','HomeTeam','AwayTeam','Prediction'])
            result = result.to_html()
        except:
            result = 'error'
            self.send_response(200)
            self.end_headers()
        self.wfile.write(result)
"""

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()