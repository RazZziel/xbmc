#!/usr/bin/env python
#
# Copyright (c) 2014 Ismael Barros² <ismael@barros2.org>
#
# This script lets you play any video file on any remote XBMC
# It will set up a mini HTTP server only to make the video available for XBMC

import SimpleHTTPServer
import SocketServer
import threading
import time
import sys
import os

if len(sys.argv) < 3:
    print "Usage:",sys.argv[0],"<video file> <XBMC ip address>"
    exit(1)

filename = sys.argv[1]
serveraddr = sys.argv[2]

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = filename
        print "Serving HTTP request of",self.path
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

os.chdir("/")
Handler = MyRequestHandler

#TODO: Find correct local address http://stackoverflow.com/questions/7334349/python-get-local-ip-address-used-to-send-ip-data-to-a-specific-remote-ip-addres
localaddress="127.0.0.1"

# Find an available port
localport=8000
server = SocketServer.TCPServer(('', localport), Handler)
#while 1:
#    try:
#        server = SocketServer.TCPServer(('', localport), Handler)
#    except:
#        if localport > 9000:
#            print "Giving up trying to find an available port"
#            exit(1)
#        localport += 1

print "Playing file",'"'+filename+'"',"from",localaddress+":"+str(localport),"on",serveraddr

# Run HTTP server
def serveFile():
    server.serve_forever()

t = threading.Thread(target=serveFile)
t.start()

# Tell XBMC to play the video we're serving
import urllib2
request="{%22jsonrpc%22:%222.0%22,%22id%22:1,%22method%22:%22Player.Open%22,%22params%22:{%22item%22:{%22file%22:%22http://"+localaddress+":"+str(localport)+"/%22}}}"
url="http://"+serveraddr+"/jsonrpc?request="+request
urllib2.urlopen(url).read()

try:
    print "Press Ctrl+C to stop"
    while threading.active_count() > 0:
        time.sleep(0.1)
except KeyboardInterrupt:
    print "Terminated"

server.shutdown()
