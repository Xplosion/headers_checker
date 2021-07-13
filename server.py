#!/usr/bin/env python3

import http.server as SimpleHTTPServer
import socketserver as SocketServer
import logging
import logging.handlers
import os


header_ip = os.getenv('header_ip')
PORT = 5375

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        logging.handlers.RotatingFileHandler('server.log',
                            maxBytes=1024*10,
                            backupCount=15),
        logging.StreamHandler()
    ]
)

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.info('Trying... ' + self.headers)
        if header_ip in self.headers:
            logging.info('Bad!')
        else:
            logging.info('Well.')

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


logging.info('Starting...')
Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

httpd.serve_forever()
