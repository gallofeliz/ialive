#!/usr/bin/env python

import socketserver
import http.server
from influxdb import InfluxDBClient
from base64 import b64encode
import os

client = InfluxDBClient('influxdb', database='mydb')

basic_value = b64encode(bytes('%s:%s' % (os.environ['USERNAME'], os.environ['PASSWORD']), 'utf-8')).decode('ascii')

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print('Receive request')

        if self.headers.get('Authorization') != 'Basic ' + basic_value:

            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="I alive"')
            self.end_headers()
            return

        if self.path != '/ping':
            self.send_response(404)
            self.end_headers()
            return

        print('ping !')

        client.write_points([
          {
            'measurement': 'ialive',
            'fields': {
              'ping': 1
            }
          }
        ])

        self.send_response(201)
        self.end_headers()

httpd = socketserver.TCPServer(('', int(os.environ.get('PORT', 80))), Handler)
try:
   httpd.serve_forever()
except KeyboardInterrupt:
   pass
httpd.server_close()
