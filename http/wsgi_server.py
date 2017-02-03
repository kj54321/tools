# -*- coding: utf-8 -*-

import datetime
import socket
import sys

from logger import logger


class WSGIServer(object):
    """A Simple WSGI HTTP Server"""
    socket_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 10

    def __init__(self, address, *args, **kwargs):
        super(WSGIServer, self).__init__()
        self.socket = socket.socket(self.socket_family, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(address)
        self.socket.listen(self.request_queue_size)
        host, port = self.socket.getsockname()[:2]
        self.host, self.port = host, port

    def set_application(self, application):
        self.application = application

    def serve_forever(self):
        logger.success('Serving HTTP running Port %s....' % PORT)
        while 1:
            self.client_connection, client_address = listen_socket.accept()
            self.handle_request()

    def handle_request(self):
        self.request_data = client_connection.recv(1024)
        logger.info('Client request content %s' % self.request_data)
        self.request_lines = self.request_data.splitlines()
        try:
            self.get_url_parameter()
            env = self.get_environ()
            app_data = self.application(env, self.start_response)
            self.finish_response(app_data)
        except Exception, e:
            logger.error(str(e))
            pass

    def get_url_paramter(self):
        self.request_dict = {'Path': self.request_lines[0]}
        for itm in self.request_lines[1:]:
            if ':' in itm:
                self.request_dict[itm.split(':')[0]] = itm.split(':')[1]
        self.request_method, self.path, self.request_version = self.request_dict.get('Path').split()
        logger.info('request_dict %s' % self.request_dict)

    def get_environ(self):
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO.StringIO(self.request_data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.request_method,
            'PATH_INFO': self.path,
            'SERVER_NAME': self.host,
            'SERVER_PORT': self.port,
            'USER_AGENT': self.request_dict.get('User-Agent')
        }
        return env

    def start_response(self, status, response_headers):
        headers = [
            ('Date', datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')),
            ('Server', 'CIWSGI0.1')
        ]
        self.headers = headers
        self.status = status

    def finish_response(self, app_data):
        try:
            response = 'HTTP/1.1 {status}\r\n'.format(status=self.status)
            for header in self.headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in app_data:
                response += data
            self.connection.sendall(response)
        finally:
            self.connection.close()

if __name__ == '__main__':
    port = 8888
    if len(sys.argv) < 2:
        sys.exit('请提供可用的wsgi应用程序, 格式为: 模块名.应用名 端口号')
    elif len(sys.argv) > 2:
        port = sys.argv[2]


    def generate_server(address, application):
        server = WSGIServer(address)
        server.set_application(TestMiddle(application))
        return server


    app_path = sys.argv[1]
    module, application = app_path.split('.')
    module = __import__(module)
    application = getattr(module, application)
    httpd = generate_server(('', int(port)), application)
    print 'RAPOWSGI Server Serving HTTP service on port {0}'.format(port)
    print '{0}'.format(datetime.datetime.now().
                       strftime('%a, %d %b %Y %H:%M:%S GMT'))
    httpd.serve_forever()
