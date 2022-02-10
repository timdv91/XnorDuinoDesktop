#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from SerialServer.XnorSerialHost import XnorSerialHost

XSH = XnorSerialHost(pPort='', pBautrate=0)   # holds the XnorSerialHost object, overwritten in the run function
DEV_MODE = False

class Srv(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if(XSH.getHWConnectionState() == False):
            XSH._connectionInit()

        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        get_data = self.rfile.read(content_length)  # <--- Gets the data itself
        if(DEV_MODE):
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), get_data.decode('utf-8'))

        rcv = XSH._communication(str(self.path), eval(get_data.decode('ascii')))

        self._set_response()
        self.wfile.write(format(rcv).encode('ascii'))

    def do_POST(self):
        if (XSH.getHWConnectionState() == False):
            XSH._connectionInit()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        if(DEV_MODE):
            logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))

        rcv = XSH._communication(str(self.path), eval(post_data.decode('ascii')))

        self._set_response()
        self.wfile.write(format(rcv).encode('ascii'))


def run(pHWport, pHWbautrate=38400, pSrvPort=8080, server_class=HTTPServer, handler_class=Srv):
    global XSH
    XSH = XnorSerialHost(pPort=pHWport, pBautrate=pHWbautrate)
    #XSH = XnorSerialHost.XnorSerialHost(pPort=pHWport, pBautrate=pHWbautrate)

    logging.basicConfig(level=logging.INFO)
    server_address = ('', pSrvPort)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')