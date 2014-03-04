#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import logging
import json

from threading import Thread
from queue import Queue

# Handle WebSocket clients
clients = []


### Handler -------------------------------------------------------------------
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """ Handle default WebSocket connections """
    # Logging settings
    logger = logging.getLogger("WebSocketHandler")
    logger.setLevel(logging.INFO)

    def open(self):
        """ New connection has been established """
        clients.append(self)
        self.logger.info("New connection")

    def on_message(self, message):
        """ Data income event callback """
        self.write_message(u"%s" % message)

    def on_close(self):
        """ Connection was closed """
        clients.remove(self)
        self.logger.info("Connection removed")


class IndexPageHandler(tornado.web.RequestHandler):
    """ Default index page handler. Not implemented yet. """
    def get(self):
        pass


### Classes -------------------------------------------------------------------
class Application(tornado.web.Application):
    def __init__(self):
        # Add here several handlers
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]

        # Application settings
        settings = {
            'template_path': 'templates'
        }

        # Call parents constructor
        tornado.web.Application.__init__(self, handlers, **settings)


class HTTPServer():
    """ Create tornado HTTP server serving our application """
    def __init__(self, host, port, in_queue=Queue()):
        # Settings
        self.application = Application()
        self.server = tornado.httpserver.HTTPServer(self.application)
        self.host = host
        self.port = port
        self.in_queue = in_queue

        # Listen to ..
        self.server.listen(self.port, self.host)

        # Logging settings
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("HTTPServer")
        self.logger.setLevel(logging.INFO)

    def start_server(self):
        """ Start HTTP server """
        self.logger.info("Starting HTTP server on port %d" % self.port)
        http_server = Thread(target=tornado.ioloop.IOLoop.instance().start)
        http_server.start()

    def start_collector(self):
        """ Start collector server """
        self.logger.info("Start collector server")
        collector_server = Thread(target=self.collect_data)
        collector_server.start()

    def collector_process_data(self, data):
        """ Process incoming data and send it to all available clients """
        for c in clients:
            c.on_message(json.dumps(data))

    def collect_data(self):
        """ Wait for data  in individual thread """
        self.logger.info("Waiting for incoming data ...")
        while True:
            item = self.in_queue.get()
            self.logger.info("Received data!")
            self.collector_process_data(item)

    def start(self):
        """ Start server """
        # Start HTTP server
        self.start_server()

        # Start data collector
        self.start_collector()
