# -*- coding: utf-8 -*-

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
import socket
import sys

from logger import logger


class Handler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        logger.info("%s - %s" % (self.address_string(), format % args))


class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multiple threaded http server"""
    pass


class Server(object):

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__()
        self.server = None

    def run_server(self, server_bind='0.0.0.0', server_port=8888):
        """run server binding to port 8888"""
        server_config = (server_bind, server_port)
        try:
            self.server = MultiThreadedHTTPServer(server_config, Handler)
        except socket.error, e:  # failed to bind port
            logger.error(str(e))
            sys.exit(1)

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.error('^C received, shutting down server.')
            self.shutdown_server()

    def shutdown_server(self):
        self.server.shutdown()
        self.server.socket.close()

    def run(self, bind='0.0.0.0',  port=8888):
        """run server"""
        self.run_server(bind, port)


server = Server()

if __name__ == '__main__':
    server.run()
