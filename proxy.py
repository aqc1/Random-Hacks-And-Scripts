#!/usr/bin/env python3

# Script acts as a simple web proxy
# Default socket localhost:8080

import socketserver
import http.server
from urllib.request import urlopen

port = 8080

class ProxyServer(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		url = self.path[1:]
		self.send_response(200)
		self.end_headers()
		self.copyfile(urlopen(url), self.wfile)

httpd = socketserver.ForkingTCPServer(('', port), ProxyServer)
print(f"Now serving at port: {port}")
httpd.serve_forever()
