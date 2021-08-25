#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./main_server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# local libs:
import XnorSerialHost
XSH = XnorSerialHost.XnorSerialHost(pPort='/dev/ttyUSB0', pBautrate=38400)
#XSH = XnorSerialHost.XnorSerialHost(pPort='COM19', pBautrate=38400)
#XSH = XnorSerialHost.XnorSerialHost(pPort='COM20', pBautrate=38400)
#XSH = XnorSerialHost.XnorSerialHost(pPort='COM23', pBautrate=38400)

DEV_MODE = False

class Srv(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        get_data = self.rfile.read(content_length)  # <--- Gets the data itself
        if(DEV_MODE):
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), get_data.decode('utf-8'))

        rcv = XSH._communication(str(self.path), eval(get_data.decode('ascii')))

        self._set_response()
        self.wfile.write(format(rcv).encode('ascii'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        if(DEV_MODE):
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))

        rcv = XSH._communication(str(self.path), eval(post_data.decode('ascii')))

        self._set_response()
        self.wfile.write(format(rcv).encode('ascii'))

def run(server_class=HTTPServer, handler_class=Srv, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')