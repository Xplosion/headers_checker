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
        client_ip = ':'.join(str(i) for i in self.client_address)
        logging.info(client_ip + ' Trying... ')
        counter = 0
        for header in self.headers.values():
            if header_ip in str(header): counter += 1
        logging.info(client_ip + ' Bad!' if counter else ' Well.')
        if not counter:
            with open('trusted_proxies.txt', 'a') as file:
                try
                    file.write('\n'+client_ip)
                except: print('Запись не удалась')

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


logging.info('Starting...')
Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

httpd.serve_forever()

