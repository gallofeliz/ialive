#!/usr/bin/env python

import socketserver
import http.server
from influxdb import InfluxDBClient
import os

client = InfluxDBClient('influxdb', database='mydb')

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print('Receive request')

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
