#!/usr/bin/env python

import socketserver
import http.server
from influxdb import InfluxDBClient

client = InfluxDBClient('influxdb', database='mydb')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):

        if (self.path != '/ping'):
          self.send_response(404)
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

httpd = socketserver.TCPServer(('', 8080), Handler)
try:
   httpd.serve_forever()
except KeyboardInterrupt:
   pass
httpd.server_close()
